import datetime
import threading
from uuid import uuid4

from .event import Event


class DomainEvent(Event):
    def __init__(self, payload):
        super().__init__()
        self.payload = payload

    @staticmethod
    def get_type():
        raise NotImplementedError()

    def raise_event(self):
        current_thread = threading.current_thread()
        self.system_entry = str(datetime.datetime.now())
        self.correlation_id = str(uuid4())
        current_thread.event_queue.add_event(self)
