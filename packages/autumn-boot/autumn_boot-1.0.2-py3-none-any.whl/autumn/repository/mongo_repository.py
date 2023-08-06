from datetime import datetime

from pymongo.collection import Collection

from ..repository.repository import AbstractRepository


class MongoRepository(AbstractRepository):
    def __init__(self, for_class, collection):
        super().__init__(for_class)
        self.for_class = for_class
        self.collection: Collection = collection

    def _create(self, item):
        return self.collection.insert_one(self.create_storable_format(item), {"last_modified": datetime.utcnow()})

    def _read(self, item_id):
        return self.create_from_storable_format(self.collection.find_one({'_id': item_id}))

    def _update(self, item, insert=False):
        return self.collection.update({'_id': item.get_id()}, self.create_storable_format(item), insert)

    def _delete(self, item_id):
        return self.collection.delete_one({'_id': item_id})

    def _read_all(self, *args, **kwargs):
        return list(map(lambda item: self.create_from_storable_format(item), self.collection.find({})))

    def _delete_all(self, *args, **kwargs):
        return self.collection.delete_many({})

    def create_storable_format(self, item):
        return dict(
            type=self.fullname(),
            payload=item.to_dict(),
            _id=item.get_id()
        )

    def create_from_storable_format(self, dct):
        if not dct:
            return None

        payload = dct['payload']
        item = self.for_class.from_dict(payload)
        if item.id == item.get_id() and item.get_id() != dct['_id']:
            item.id = dct['_id']

        return item

    def fullname(self):
        module = self.for_class.__module__

        if not module or module == str.__class__.__module__:
            return self.for_class.__name__
        else:
            return f'{module}.{self.for_class.__name__}'
