import datetime
from copy import deepcopy

from ..subscriber import Subscriber


class Topic:
    def __init__(self, event_queue, topic_identifier):
        self.subscribers = set()
        self.event_queue = event_queue
        self.name: str = topic_identifier

    def add_subscriber(self, subscriber):
        self.subscribers.add(subscriber)

    def remove_subscriber_by_client_id(self, client_id):
        self.remove_subscriber(Subscriber.client_from_id(client_id))

    def remove_subscribers(self):
        subs = list(self.subscribers)
        for subscriber in subs:
            self.remove_subscriber(subscriber)

    def remove_subscriber(self, subscriber):
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)

    def publish(self, notification, correlation_id):
        if len(self.subscribers) == 0:
            print(
                f'Notification {notification.get_type()} was not published, '
                f'because there are no subscribers on this ({self.name}) topic')
            return

        for subscriber in self.subscribers:
            copied_notification = deepcopy(notification)
            copied_notification.destination = subscriber.address
            copied_notification.correlation_id = correlation_id
            copied_notification.system_entry = str(datetime.datetime.now())
            self.event_queue.add_event(copied_notification)
