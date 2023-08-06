from copy import deepcopy

from ..repository.repository import AbstractRepository


class MemoryRepository(AbstractRepository):
    def __init__(self, for_class):
        super().__init__(for_class)
        self.storage = {}

    def _read_all(self):
        return list(self.storage.values())

    def _create(self, item):
        self.storage[item.get_id()] = item
        return item

    def _read(self, _id):
        if _id in self.storage:
            return self.storage[_id]

    def _update(self, item, insert=False):
        if item.get_id() not in self.storage:
            if insert:
                self.storage[item.get_id()] = item
        else:
            self.storage[item.get_id()] = item

    def _delete(self, _id):
        if _id in self.storage:
            copied_item = deepcopy(self.storage[_id])
            del self.storage[_id]
            return copied_item

    def _delete_all(self, *args, **kwargs):
        pass

