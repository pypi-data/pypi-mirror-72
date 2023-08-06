from uuid import uuid4


class Storable:
    def __init__(self):
        self.id = str(uuid4())

    def get_id(self):
        return self.id

    def to_dict(self):
        raise NotImplementedError()

    def __eq__(self, that):
        return self.get_id() == that.get_id()

    def __str__(self):
        s = ''
        for prop, value in vars(self).items():
            s += f'{str(prop)}={str(value)} '

        return f'<{self.__class__.__name__} {s} />'
