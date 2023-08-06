from .notification import Notification


class DisconnectedNotification(Notification):
    def __init__(self, reason='Server shutdown!'):
        super().__init__(payload={
            'reason': reason
        })

    @staticmethod
    def get_type():
        return 'notification.disconnected'
