from .store import Store


class CorrelationStore(Store):
    def __init__(self):
        super().__init__()
        self.map = {}

    def _add(self, correlation_id, client_id):
        self.map[correlation_id] = client_id

    def _get(self, correlation_id):
        return self.map[correlation_id] if correlation_id in self.map else None

    def _remove(self, correlation_id):
        if correlation_id in self.map:
            del self.map[correlation_id]

    def _contains(self, correlation_id):
        return correlation_id in self.map
