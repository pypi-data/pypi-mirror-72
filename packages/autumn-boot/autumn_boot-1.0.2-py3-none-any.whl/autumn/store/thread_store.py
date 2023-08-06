from .store import Store


class ThreadStore(Store):
    def __init__(self):
        super().__init__()
        self.map = {}

    def _add(self, client_id, correlation_id, executor_thread):
        if client_id in self.map:
            self.map[client_id][correlation_id] = executor_thread
        else:
            self.map[client_id] = {}
            self.map[client_id][correlation_id] = executor_thread

    def _get(self, client_id):
        return self.map[client_id] if client_id in self.map else {}

    def _contains(self, client_id, correlation_id=None):
        if not correlation_id:
            return client_id in self.map
        else:
            return client_id in self.map and correlation_id in self.map[client_id]

    def _remove(self, client_id, correlation_id=None):
        if client_id in self.map:
            if correlation_id and correlation_id in self.map[client_id]:
                del self.map[client_id][correlation_id]
            elif not correlation_id:
                del self.map[client_id]
