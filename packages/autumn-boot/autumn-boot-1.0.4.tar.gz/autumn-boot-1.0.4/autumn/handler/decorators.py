def event_handler(event_to_handle):
    def sub_decorator(method):
        assert type(event_to_handle) == str, "Event to handle must be of type string"
        method.handles = event_to_handle
        return method

    return sub_decorator


def starts_handler(method):
    method.starts_handler = True

    return method


def tear_down(method):
    method.is_teardown = True

    return method


def protected(method):
    method.protected = True
    return method


def only_public(method):
    method.only_public = True
    return method
