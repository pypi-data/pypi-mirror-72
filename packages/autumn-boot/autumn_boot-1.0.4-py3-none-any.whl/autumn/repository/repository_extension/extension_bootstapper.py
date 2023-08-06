from copy import deepcopy
from typing import Type, List

from ...repository.repository_extension.extension import RepositoryExtension


class ExtensionBootstrapper:
    extension_list: 'List[Type[RepositoryExtension]]'

    def __init__(self, extension_list: 'List[Type[RepositoryExtension]]'):
        self.extension_list = deepcopy(extension_list)

    def get_extensions(self) -> 'List[Type[RepositoryExtension]]':
        return deepcopy(self.extension_list)
