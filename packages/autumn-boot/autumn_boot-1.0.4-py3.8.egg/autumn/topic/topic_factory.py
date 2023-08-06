from ..subscriber import SubscriberType
from .topic import Topic


class TopicFactory:
    def __init__(self, event_queue):
        self.event_queue = event_queue
        self.map = dict()

    def get_topic(self, topic_identifier) -> Topic:
        if topic_identifier in self.map:
            return self.map[topic_identifier]

        instance = Topic(self.event_queue, topic_identifier)
        self.map[topic_identifier] = instance
        return instance

    def remove_client(self, client_id):
        for (topic_identifier, topic) in self.map.items():
            subscribers_in_topic = list(
                filter(lambda subscriber: subscriber.type == SubscriberType.CLIENT and client_id in subscriber.address,
                       topic.subscribers))

            for sub in subscribers_in_topic:
                topic.remove_subscriber(sub)
