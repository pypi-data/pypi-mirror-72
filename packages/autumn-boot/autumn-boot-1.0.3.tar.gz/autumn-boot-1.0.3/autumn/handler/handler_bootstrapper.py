import re
from copy import deepcopy
from typing import List, Type, Dict

from ..events.event import Event
from .handler import Handler


class HandlerBootstrapper:
    event_to_handler_map: 'Dict[Type[Event], List[Type[Handler]]]'
    handler_list: 'List[Type[Handler]]'
    service_name_to_class_map: 'Dict[str, Type[Handler]]'

    def __init__(self, handler_list: List[Type[Handler]]):
        self.handler_list = handler_list
        self.event_to_handler_map = {}
        self.service_name_to_class_map = dict([(self.get_service_name_from_class(
            handler_class), handler_class) for handler_class in self.handler_list])

        for handler in self.handler_list:
            for key, value in handler.__dict__.items():
                if hasattr(value, 'handles'):
                    event_type = getattr(value, 'handles')
                    if event_type in self.event_to_handler_map:
                        self.event_to_handler_map[event_type].append(handler)
                    else:
                        self.event_to_handler_map[event_type] = [handler]

    @staticmethod
    def get_service_name_from_class(handler_class: 'Type[Handler]') -> str:
        return '-'.join(re.findall(r'[A-Z][a-z]+', handler_class.__name__)).lower()

    def get_handlers(self) -> 'List[Type[Handler]]':
        return deepcopy(self.handler_list)

    def get_handler_for(self, event_type: 'Type[Event]') -> 'Type[Handler]':
        return self.event_to_handler_map[event_type][0] if event_type in self.event_to_handler_map else None

    def get_handlers_for_notification(self, notification_type) -> 'List[Type[Handler]]':
        handlers = list(
            filter(
                lambda handler: notification_type in handler.handles().keys(), self.handler_list
            )
        )
        return handlers

    def get_handler_class_by_service_name(self, service_name) -> 'Type[Handler]':
        return self.service_name_to_class_map[service_name] if service_name in self.service_name_to_class_map else None
