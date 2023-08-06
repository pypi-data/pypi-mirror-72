from .notification import Notification


class ShutdownRequestedNotification(Notification):
    def __init__(self):
        super().__init__(payload={})

    @staticmethod
    def get_type():
        return 'notification.shutdown_requested'
