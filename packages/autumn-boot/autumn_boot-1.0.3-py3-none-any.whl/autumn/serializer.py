import json
from copy import deepcopy
from datetime import datetime

from .events.request import Request


def get_correlation_id(obj, correlation_id):
    correlation_id = obj['correlation_id'] if 'correlation_id' in obj else correlation_id
    correlation_id = obj['correlationId'] if 'correlationId' in obj else correlation_id

    return correlation_id


def deserialize(string, correlation_id, client_id):
    obj = json.loads(string)

    if 'type' not in obj:
        raise Exception('This request format was not recognized by the system')

    type_ = obj['type']
    payload = obj['payload'] if 'payload' in obj else {}
    headers = obj['headers'] if 'headers' in obj else {}

    request = Request(type_, payload=payload, headers=headers)
    request.correlation_id = get_correlation_id(obj, correlation_id)
    request.client_id = client_id
    request.system_entry = str(datetime.now())

    return request


def serialize(obj):
    dct = _recursive_clear_none(deepcopy(obj.__dict__))
    dct['type'] = obj.get_type()

    return json.dumps(dct, indent=4)


def _recursive_clear_none(obj):
    if type(obj) == dict:
        new_obj = {}
        for key in obj.keys():
            result = _recursive_clear_none(obj[key])
            if result is not None:
                new_obj[transform_to_camel_case(key)] = result
        return new_obj

    return obj


def transform_to_camel_case(key):
    chunks = key.split('_')
    return chunks[0] + ''.join([chunk.capitalize() for chunk in chunks[1:]])
