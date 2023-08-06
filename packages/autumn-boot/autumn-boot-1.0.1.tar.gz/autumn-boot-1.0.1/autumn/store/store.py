from threading import Lock


class Store:
    def __init__(self):
        self.lock = Lock()

    def add(self, *args, **kwargs):
        with self.lock:
            return self._add(*args, **kwargs)

    def remove(self, *args, **kwargs):
        with self.lock:
            return self._remove(*args, **kwargs)

    def get(self, *args, **kwargs):
        with self.lock:
            return self._get(*args, **kwargs)

    def contains(self, *args, **kwargs):
        with self.lock:
            return self._contains(*args, **kwargs)

    def _add(self, *args, **kwargs):
        raise NotImplementedError()

    def _remove(self, *args, **kwargs):
        raise NotImplementedError()

    def _get(self, *args, **kwargs):
        raise NotImplementedError()

    def _contains(self, *args, **kwargs):
        raise NotImplementedError()
