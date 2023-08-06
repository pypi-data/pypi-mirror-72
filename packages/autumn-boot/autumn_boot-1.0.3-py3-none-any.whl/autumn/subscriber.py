from enum import Enum


class Subscriber:
    def __init__(self, subscriber_type: 'SubscriberType', address):
        self.type = subscriber_type
        self.address: str = address

    def __str__(self):
        s = ''
        for prop, value in vars(self).items():
            s += f'{str(prop)}={str(value)} '

        return f'<{self.__class__.__name__} {s} />'

    def __eq__(self, other: 'Subscriber'):
        return self.type == other.type and self.address == other.address

    def __hash__(self):
        return self.type.__hash__() + self.address.__hash__()

    @classmethod
    def client_from_id(cls, client_id):
        return cls(SubscriberType.CLIENT, f'remote://websocket/{client_id}')


class SubscriberType(Enum):
    CLIENT = 1
    SERVICE = 2
