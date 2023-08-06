from ..repository.storable import Storable


class AbstractRepository:
    def __init__(self, for_class):
        assert issubclass(
            for_class, Storable), 'for_class must extend Storable type'
        self._class = for_class

    def create(self, *args, **kwargs):
        self.check_type(args[0])
        return self._create(*args, **kwargs)

    def read(self, *args, **kwargs):
        return self._read(*args, **kwargs)

    def update(self, *args, **kwargs):
        self.check_type(args[0])
        return self._update(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self._delete(*args, **kwargs)

    def read_all(self, *args, **kwargs):
        return self._read_all(*args, **kwargs)

    def delete_all(self, *args, **kwargs):
        return self._delete_all(*args, **kwargs)

    def _create(self, *args, **kwargs):
        raise NotImplementedError()

    def _read(self, *args, **kwargs):
        raise NotImplementedError()

    def _update(self, *args, **kwargs):
        raise NotImplementedError()

    def _delete(self, *args, **kwargs):
        raise NotImplementedError()

    def _read_all(self, *args, **kwargs):
        raise NotImplementedError()

    def _delete_all(self, *args, **kwargs):
        raise NotImplementedError()

    def check_type(self, item):
        assert issubclass(
            type(item), self._class), f'Item must be of type {self._class}'
