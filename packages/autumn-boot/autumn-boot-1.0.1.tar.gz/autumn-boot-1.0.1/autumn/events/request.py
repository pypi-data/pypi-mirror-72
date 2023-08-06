from .event import Event


class Request(Event):
    def __init__(self, event_type, payload=None, headers=None):
        super().__init__()

        if headers is None:
            headers = {}
        if payload is None:
            payload = {}

        self.payload = payload
        self.headers = headers
        self.type = event_type
        self.client_id = None

    def get_type(self):
        return self.type
