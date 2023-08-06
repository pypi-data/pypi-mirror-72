from ..repository.repository_extension.extension_bootstapper import ExtensionBootstrapper
from ..repository.mongo_repository import MongoRepository
from ..repository.repository_factory import AbstractRepositoryFactory


class MongoRepositoryFactory(AbstractRepositoryFactory):
    def __init__(self, mongo_client, extension_bootstrapper, mongo_database="emcai_database"):
        super().__init__()
        self.client = mongo_client
        self.extension_bootstrapper: ExtensionBootstrapper = extension_bootstrapper
        self.database = mongo_client[mongo_database]
        self.database_name = mongo_database
        self.repositories = {}

    def _get_repository(self, for_class):
        if for_class in self.repositories:
            return self.repositories[for_class]

        collection_name = for_class.__name__.lower() + '_collection'
        collection = self.database[collection_name]

        repository = MongoRepository(for_class, collection)

        for extension in self.extension_bootstrapper.get_extensions():
            if getattr(extension, 'extension_for') == for_class:
                for _, method in extension.__dict__.items():
                    if hasattr(method, 'include_into_extension'):
                        self._bind(repository, method)

        self.repositories[for_class] = repository

        return repository

    def _bind(self, instance, func):
        bound_method = func.__get__(instance, instance.__class__)
        setattr(instance, func.__name__, bound_method)

        return bound_method
