from .notification import Notification


class ClientDisconnectedNotification(Notification):
    def __init__(self, client_id: str):
        super().__init__(payload={
            'client_id': client_id,
        })

    @staticmethod
    def get_type():
        return 'notification.client_disconnected'
