def repository_extension(for_class):
    def sub_decorator(actual_class):
        actual_class.extension_for = for_class

        return actual_class

    return sub_decorator


def include_method(method):
    method.include_into_extension = True
    return method
