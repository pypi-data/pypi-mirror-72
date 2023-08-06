import asyncio
import datetime
import re
from typing import List, Callable
from uuid import uuid4

from . import serializer
from .event_queue import EventQueue
from .events.error_response import ErrorResponse
from .events.event import Event
from .executor import ExecutorThread
from .exit_state import ExitState
from .handler.error_handler import ExceptionHandler
from .handler.handler_bootstrapper import HandlerBootstrapper
from .repository.repository_factory import AbstractRepositoryFactory
from .subscriber import Subscriber, SubscriberType
from .topic.topic_factory import TopicFactory


class EventDispatcher:
    def __init__(self, event_queue: EventQueue,
                 correlation_store,
                 thread_store,
                 client_store,
                 exception_handler: ExceptionHandler,
                 topic_factory: TopicFactory,
                 repository_factory: AbstractRepositoryFactory,
                 handler_bootstrapper: HandlerBootstrapper,
                 exit_state: ExitState,
                 handler_map=None,
                 protected_check: 'Callable[[Event], bool]' = None,
                 public_check: 'Callable[[Event], bool]' = None):
        self.event_queue = event_queue
        self.correlation_store = correlation_store
        self.thread_store = thread_store
        self.client_store = client_store
        self.exception_handler = exception_handler
        self.topic_factory = topic_factory
        self.repository_factory = repository_factory
        self.handler_map = handler_map if handler_map is not None else {}
        self.halted_for = 0
        self.handler_bootstrapper = handler_bootstrapper
        self.exit_state = exit_state
        self.protected_check = protected_check
        self.public_check = public_check
        self._init_handler_subscriptions()
        self.number_of_handled_events = 0
        self.number_of_outgoing_events = 0
        self.handle_times = []

    def _init_handler_subscriptions(self):
        handlers = self.handler_bootstrapper.get_handlers()
        for handler in handlers:
            if handler.subscribes_for():
                service_address = f"isc://{'-'.join(re.findall(r'[A-Z][a-z]+', handler.__name__)).lower()}"
                subscriber = Subscriber(
                    SubscriberType.SERVICE, service_address)
                for topic_name in handler.subscribes_for():
                    topic = self.topic_factory.get_topic(topic_name)
                    topic.add_subscriber(subscriber)

    def execute_on_existing_instance(self, event, service_name):
        actual_service_name = re.findall('(.*)-\d+$', service_name)[0]
        assert actual_service_name in self.handler_map, f'Actual service not found: {actual_service_name}'
        assert service_name in self.handler_map[
            actual_service_name], f'Service instance not found {service_name}'

        self.handler_map[actual_service_name][service_name].process_event(
            event)

    def thread_stopped(self, service_name, handler_name):
        actual_service_name = service_name
        assert actual_service_name in self.handler_map, f'Such service was never instansiated {actual_service_name}'
        assert handler_name in self.handler_map[
            actual_service_name], f'Service instance not found {handler_name}'
        assert self.handler_map[actual_service_name][
                   handler_name].handler_instance.running is False, f'Service still running, cannot stop {handler_name}'
        del self.handler_map[actual_service_name][handler_name]

    def instantiate_new_handler_and_execute(self, service_name, event, client_id):
        if service_name not in self.handler_map:
            self.handler_map[service_name] = {}

        instance_count = str(uuid4())
        handler_name = f'{service_name}-{instance_count}'

        handler_class = self.handler_bootstrapper.get_handler_class_by_service_name(service_name)

        if handler_class:
            executor_thread = ExecutorThread(
                handler_class,
                event.correlation_id,
                self.event_queue,
                self.exception_handler,
                self.topic_factory,
                self.repository_factory,
                handler_name,
                service_name,
                self.thread_stopped,
                public_check=self.public_check,
                protected_check=self.protected_check)

            self.thread_store.add(
                client_id,
                event.correlation_id,
                executor_thread)
            self.handler_map[service_name][handler_name] = executor_thread

            executor_thread.process_event(event)
            executor_thread.start()
        else:
            self.exception_handler.handle_exception(
                Exception(f'No handler for type {event.get_type()}'), event)

    async def dispatch(self):
        while not self.exit_state.should_exit:
            try:
                if len(self.event_queue) == 0:
                    await asyncio.sleep(0)
                else:
                    event = self.event_queue.get_event()
                    self.number_of_handled_events += 1

                    correlation_id = event.correlation_id
                    client_id = self.correlation_store.get(correlation_id)
                    destination = event.destination

                    if not destination:
                        # it's an incoming events from the client  => it should have a type,
                        # and should be a notification or request
                        # => destination can be deducted from request/notification type
                        # => it's should be directed to a service => isc://

                        handler_class = self.handler_bootstrapper.get_handler_for(event.get_type())
                        if not handler_class:
                            if issubclass(type(event), ErrorResponse):
                                print('Failed to dispatch ErrorResponse:', event)
                                continue
                            self.exception_handler.handle_exception(
                                Exception(f'> No handler for type {event.get_type()}'), event, use_return=True)
                            continue

                        service_name = self.handler_bootstrapper.get_service_name_from_class(
                            handler_class).strip()
                        destination = f'isc://{service_name}'
                        event.destination = destination

                        await self.dispatch_event_to_handler(client_id, event, handler_class, service_name)

                        continue
                    if destination.startswith('isc://'):
                        service_name = destination.split('//')[1].strip()

                        handler_class = self.handler_bootstrapper.get_handler_class_by_service_name(service_name)

                        await self.dispatch_event_to_handler(client_id, event, handler_class, service_name)

                    elif destination.startswith('remote://websocket/'):
                        client_id = re.findall(
                            r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}', destination)[0]
                        client = self.client_store.get(client_id)
                        
                        await client.websocket.send(serializer.serialize(event))
                        self.number_of_outgoing_events += 1
                        handling_time = (datetime.datetime.now() - datetime.datetime.fromisoformat(
                            event.system_entry)).microseconds / 1000
                        self.handle_times.append(handling_time)
                        self.handle_times = self.handle_times[-1000:]
            except Exception as dispatcher_e:
                print(dispatcher_e)

    async def dispatch_event_to_handler(self, client_id, event, handler_class, service_name):
        if handler_class:
            active_handlers = list(
                self.handler_map[service_name].values() if service_name in self.handler_map.keys() else [])
            available_handlers: List[ExecutorThread] = []
            for active_handler in active_handlers:
                key_readers = active_handler.handler_instance.key_readers
                for key_reader in key_readers:
                    try:
                        if key_reader(event):
                            available_handlers.append(active_handler)
                    except KeyError as key_exception:
                        print(
                            f'KeyReader exception: {key_exception} for keyreader in '
                            f'{active_handler.service_name}')
            if len(available_handlers) != 0:
                for available_handler in available_handlers:
                    available_handler.process_event(event)
            else:
                if event.get_type() in handler_class.started_by():
                    self.instantiate_new_handler_and_execute(service_name, event, client_id)
                else:
                    if event.retry_count < 5 and hasattr(event, 'get_type'):
                        if event.get_type().startswith('domain.'):
                            event.retry_count += 1
                            self.event_queue.add_event(event)
                            return

                    self.exception_handler.handle_exception(
                        Exception(
                            f'Handler type is found for {event.get_type()}, '
                            f'but there is no instance running, and the handler isn\'t started by it'),
                        event, use_return=True)
        else:
            self.exception_handler.handle_exception(
                Exception(f'No handler for type {event.get_type()}'), event, use_return=True)
