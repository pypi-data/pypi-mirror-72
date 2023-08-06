from datetime import datetime


class Client:
    def __init__(self, client_id, websocket):
        self.client_id = client_id
        self.websocket = websocket
        self.connected_at = datetime.now()
        self.last_heartbeat = datetime.now()
