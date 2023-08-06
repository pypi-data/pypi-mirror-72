from ..repository.memory_repository import MemoryRepository
from ..repository.repository_factory import AbstractRepositoryFactory


class MemoryRepositoryFactory(AbstractRepositoryFactory):
    def __init__(self):
        super().__init__()
        self.repositories = {}

    def _get_repository(self, for_class):
        if for_class in self.repositories:
            return self.repositories[for_class]

        repository = MemoryRepository(for_class)
        self.repositories[for_class] = repository

        return repository
