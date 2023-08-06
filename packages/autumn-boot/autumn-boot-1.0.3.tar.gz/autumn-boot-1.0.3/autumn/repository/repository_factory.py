from ..repository.repository import AbstractRepository


class AbstractRepositoryFactory:
    def get_repository(self, *args: object, **kwargs: object) -> AbstractRepository:
        self.check_type(args[0])
        return self._get_repository(*args, **kwargs)

    @staticmethod
    def check_type(_class):
        pass

    def _get_repository(self, *args, **kwargs):
        raise NotImplementedError()
