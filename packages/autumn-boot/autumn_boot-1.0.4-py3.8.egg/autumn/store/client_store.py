from .store import Store


class ClientStore(Store):
    def __init__(self):
        super().__init__()
        self.map = {}

    def _add(self, client_id, client):
        self.map[client_id] = client

    def _get(self, client_id):
        return self.map[client_id] if client_id in self.map.keys() else None

    def _remove(self, client_id):
        if client_id in self.map:
            del self.map[client_id]

    def _contains(self, client_id):
        return client_id in self.map

    def keys(self):
        with self.lock:
            return self.map.keys()
