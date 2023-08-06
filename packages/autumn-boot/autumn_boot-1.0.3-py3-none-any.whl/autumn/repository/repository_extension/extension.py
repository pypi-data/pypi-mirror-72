from typing import Type

from pymongo.collection import Collection


class RepositoryExtension:
    for_class: Type
    collection: Collection

    def create_storable_format(self, item):
        pass

    def create_from_storable_format(self, dct):
        pass
