from datetime import datetime

from ..events.domain_event import DomainEvent
from ..events.error_response import ErrorResponse


class ExceptionHandler:
    def __init__(self, event_queue):
        self.event_queue = event_queue

    def handle_exception(self, exception, event, status=500, use_return=False):
        try:
            message = f'{type(exception).__name__}: {exception}'
            if not event.destination and not use_return and not event.return_address:
                raise Exception('Event of type:', event.get_type(), 'has no destination')
            print(message)
            error_response = ErrorResponse(message=message, status=status)
            error_response.destination = event.return_address if use_return else event.destination
            error_response.system_entry = event.system_entry
            error_response.started_handling = event.started_handling if hasattr(event, 'started_handling') else str(
                datetime.now())
            error_response.stopped_handling = event.stopped_handling if hasattr(event, 'stopped_handling') else str(
                datetime.now())
            error_response.correlation_id = event.correlation_id
            if not issubclass(type(event), DomainEvent):
                self.event_queue.add_event(error_response)
        except Exception as e:
            print('Error building exception', e)
