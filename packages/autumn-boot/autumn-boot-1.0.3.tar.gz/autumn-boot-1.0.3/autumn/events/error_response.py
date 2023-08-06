from ..events import Response


class ErrorResponse(Response):
    def __init__(self, message='', status=500):
        super().__init__(status=status, message=message)

    @staticmethod
    def get_type():
        return 'response.error'
