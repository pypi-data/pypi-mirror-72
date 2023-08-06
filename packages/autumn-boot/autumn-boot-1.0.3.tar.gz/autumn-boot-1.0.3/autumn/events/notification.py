from .event import Event


class Notification(Event):
    def __init__(self, payload):
        super().__init__()
        self.payload = payload
        self.client_id = None

    @staticmethod
    def get_type():
        raise NotImplementedError()
