class Event:
    def __init__(self):
        self.event_id = str(__import__('uuid').uuid4())
        self.correlation_id = None
        self.destination = None
        self.return_address = None
        self.system_entry = None
        self.system_leave = None
        self.retry_count = 0
