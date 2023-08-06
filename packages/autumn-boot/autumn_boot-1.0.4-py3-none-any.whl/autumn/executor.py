import datetime
from queue import Queue, Empty
from threading import Thread
from time import sleep
from typing import Callable

from .handler.handler import Handler
from .repository.repository_factory import AbstractRepositoryFactory

from .event_queue import EventQueue
from .events.event import Event


class ExecutorThread(Thread):
    def __init__(self, handler_class, correlation_id, event_queue, exception_handler, topic_factory, repository_factory,
                 name, service_name, stopped, protected_check: 'Callable[[Event], bool]' = None,
                 public_check: 'Callable[[Event], bool]' = None):
        super().__init__()

        self.handler_class = handler_class
        self.correlation_id = correlation_id
        self.started_at = None
        self.event_queue: EventQueue = event_queue
        self.topic_factory = topic_factory
        self.exception_handler = exception_handler
        self.repository_factory = repository_factory
        self.execute_queue = Queue()
        self.name = name
        self.service_name = service_name
        self.stopped = stopped
        self.inactive_for = 0
        self._init_handler()

        def pass_all_event(_, __, ___):
            return True

        self.protected_check: 'Callable[[Event, Callable, AbstractRepositoryFactory], bool]' = protected_check if protected_check else pass_all_event
        self.public_check: 'Callable[[Event, Callable, AbstractRepositoryFactory], bool]' = public_check if public_check else pass_all_event

    def _init_handler(self):
        self.handler_instance: Handler = object.__new__(self.handler_class)
        self.handler_instance.event_queue = self.event_queue
        self.handler_instance.repository_factory = self.repository_factory
        self.handler_instance.topic_factory = self.topic_factory
        self.handler_instance.correlation_id = self.correlation_id
        self.handler_instance.key_readers = []
        self.handler_instance.running = True
        self.handler_instance.name = self.name
        self.handler_instance.initial_event = None
        self.handler_instance.should_deactivate = True

        self.handler_instance.__init__()

    def run(self):
        self.started_at = datetime.datetime.now()

        while self.handler_instance.running:
            try:
                method, args = self.execute_queue.get_nowait()
                event = args[0]
                if not self.handler_instance.initial_event:
                    self.handler_instance.initial_event = event
                event.started_handling = str(datetime.datetime.now())
                self.handler_instance.current_event = event
                self.handler_instance.return_address = event.return_address
                try:
                    method(self.handler_instance, *args)
                    self.inactive_for = 0
                except Exception as exception:
                    self.exception_handler.handle_exception(
                        exception, event, use_return=True)
                    print(exception)
                    self.handler_instance.running = False
                    break
            except Empty as e:
                sleep(0.1)
                self.inactive_for += 0.1

                if self.inactive_for >= 10 and self.handler_instance.should_deactivate:
                    tear_down_method = self.handler_instance.get_teardown_method()
                    if tear_down_method:
                        bound_method = tear_down_method.__get__(self.handler_instance, self.handler_instance.__class__)
                        bound_method()

                    self.handler_instance.running = False
                    print(f'Stopping {self.service_name} due to belonged inactivity!')
                pass

        self.stopped(self.service_name, self.name)

    def running_for(self):
        return datetime.datetime.now() - self.started_at

    def process_event(self, *args):
        event = args[0]
        assert event, 'events must be of type events, not none'
        if event.get_type() in self.handler_instance.handles():
            handler_method = self.handler_instance.handles()[event.get_type()]
            if not self.__check_protected(handler_method, event) or not self.__check_only_public(handler_method, event):
                self.exception_handler.handle_exception(
                    Exception('Unauthorized access!'), event, status=400, use_return=True)
                self.handler_instance.running = False

            else:
                self.handler_instance.correlation_id = event.correlation_id
                self.execute_queue.put([handler_method, [*args]])

        else:
            raise Exception(f'This handler does not handle {event.get_type()}')

    def __check_protected(self, handler_method, event):
        if hasattr(handler_method, 'protected') and getattr(handler_method, 'protected'):
            return self.protected_check(event, handler_method, self.repository_factory)

        return True

    def __check_only_public(self, handler_method, event):
        return self.public_check(event, handler_method, self.repository_factory)

    def __str__(self):
        return f'<ExecutorThread started_at={self.started_at} service_name={self.service_name} />'
