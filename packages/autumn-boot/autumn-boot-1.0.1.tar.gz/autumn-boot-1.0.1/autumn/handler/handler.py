from datetime import datetime
from typing import List, Callable

from ..event_queue import EventQueue
from ..events import DomainEvent
from ..events import Request
from ..events.error_response import ErrorResponse
from ..events.event import Event
from ..repository.repository_factory import AbstractRepositoryFactory
from ..topic.topic_factory import TopicFactory


class Handler:
    correlation_id: str
    event_queue: EventQueue
    topic_factory: TopicFactory
    repository_factory: AbstractRepositoryFactory
    return_address: str
    name: str
    current_event: Event
    initial_event: Event
    should_deactivate: bool

    def __init__(self, correlation_id):
        self.correlation_id = correlation_id
        self.running: bool = True
        self.key_readers = []
        self.initial_event = None
        self.should_deactivate = True

    @classmethod
    def handles(cls):
        return dict([(getattr(method, 'handles'), method) for method in cls.__dict__.values() if
                     hasattr(method, 'handles')])

    @classmethod
    def started_by(cls) -> List[str]:
        return list(map(lambda method: method.handles, filter(lambda method: hasattr(method, 'starts_handler'),
                                                              filter(lambda method: hasattr(method, 'handles'),
                                                                     list(cls.__dict__.values())))))

    @classmethod
    def get_teardown_method(cls) -> Callable:
        for method in cls.__dict__.values():
            if hasattr(method, 'is_teardown'):
                return method

        return None

    @staticmethod
    def subscribes_for():
        return []

    def send(self, event):
        if issubclass(type(event), Request):
            event.return_address = f'isc://{self.name}'
            event.system_entry = str(datetime.now())
            event.correlation_id = self.correlation_id
        elif issubclass(type(event), DomainEvent):
            event.system_entry = str(datetime.utcnow())
            event.correlation_id = self.correlation_id
            event.return_address = f'isc://{self.name}'
            event.origin = f'isc://{self.name}'

        self.event_queue.add_event(event)

    def respond_with_success(self, event, correlation_id=None):
        event.destination = self.return_address
        event.origin = f'isc://{self.name}'
        event.system_entry = self.current_event.system_entry
        event.started_handling = self.current_event.started_handling
        event.handling_stopped = str(datetime.now())
        event.correlation_id = self.current_event.correlation_id if not correlation_id else correlation_id
        self.event_queue.add_event(event)

    def stop_with_success(self, event, correlation_id=None):
        self.respond_with_success(event, correlation_id=correlation_id)
        self.running = False

    def respond_with_error(self, event, message=None, status=500):
        event.status = status
        event.message = message
        event.destination = self.return_address
        event.origin = f'isc://{self.name}'
        event.system_entry = self.current_event.system_entry
        event.started_handling = self.current_event.started_handling
        event.handling_stopped = str(datetime.now())
        event.correlation_id = self.current_event.correlation_id
        self.event_queue.add_event(event)

    def stop_with_error(self, event, message=None, status=500):
        self.respond_with_error(event, message, status=status)
        self.running = False

    def respond_with_success_to_initial_event(self, response):
        response.destination = self.initial_event.return_address
        response.correlation_id = self.initial_event.correlation_id
        response.system_entry = self.current_event.system_entry
        response.started_handling = self.current_event.started_handling
        response.handling_stopped = str(datetime.now())
        response.origin = f'isc://{self.name}'
        self.event_queue.add_event(response)

    def respond_with_error_to_initial_event(self, message='', status=''):
        response = ErrorResponse()
        response.status = status
        response.message = message
        response.payload = None
        response.destination = self.initial_event.return_address
        response.origin = f'isc://{self.name}'
        response.system_entry = self.current_event.system_entry
        response.started_handling = self.current_event.started_handling
        response.handling_stopped = str(datetime.now())
        response.correlation_id = self.initial_event.correlation_id
        self.event_queue.add_event(response)

    def stop(self):
        self.running = False
