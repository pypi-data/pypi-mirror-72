from .event import Event


class Response(Event):
    def __init__(self, status=200, message='OK', payload=None):
        super().__init__()
        self.status = status
        self.message = message
        self.payload = payload
        self.origin = None

    @staticmethod
    def get_type() -> str:
        raise NotImplementedError()
