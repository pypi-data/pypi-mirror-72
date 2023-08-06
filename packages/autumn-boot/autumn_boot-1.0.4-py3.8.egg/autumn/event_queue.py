from threading import Lock

from .events.event import Event


class EventQueue:
    def __init__(self):
        self.queue = []
        self.lock = Lock()

    def add_event(self, event):
        assert issubclass(type(event), Event), 'Only events shall be submitted to queue'

        with self.lock:
            self.queue.append(event)

    def get_event(self):
        return_value = None

        if len(self) != 0:
            with self.lock:
                return_value = self.queue[0]
                self.queue = self.queue[1:]

        return return_value

    def __len__(self):
        return len(self.queue)
