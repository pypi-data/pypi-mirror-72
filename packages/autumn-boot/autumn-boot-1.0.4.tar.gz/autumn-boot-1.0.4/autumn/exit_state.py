import _thread
import datetime
import os
import signal
import sys
from time import sleep
from uuid import uuid4

from .event_queue import EventQueue
from .events.server_disconnect import DisconnectedNotification
from .events.shutdown_requested import ShutdownRequestedNotification
from .store.client_store import ClientStore
from .store.thread_store import ThreadStore
from .topic.topic import Topic


class ExitState:
    should_exit: bool

    def __init__(self, server_notifications_topic: Topic, client_store: ClientStore, thread_store: ThreadStore,
                 event_queue: EventQueue):
        self.should_exit = False
        self.client_store = client_store
        self.thread_store = thread_store
        self.server_notifications_topic = server_notifications_topic
        self.event_queue = event_queue

        if sys.platform != 'win32':
            signal.signal(signal.SIGUSR1, self.actual_exit)
            signal.signal(signal.SIGINT, self.exit_gracefully)
            signal.signal(signal.SIGTERM, self.exit_gracefully)
        else:
            self.original_sigint = signal.getsignal(signal.SIGINT)
            signal.signal(signal.SIGINT, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        def actual_exit():
            self.server_notifications_topic.publish(ShutdownRequestedNotification(), str(uuid4()))
            self.send_disconnect_message()
            sleep(2)
            self.should_exit = True
            for dictionary in self.thread_store.map.values():
                for executor_thread in list(dictionary.values()):
                    if executor_thread.handler_instance:
                        executor_thread.handler_instance.running = False
            if sys.platform == 'win32':
                signal.signal(signal.SIGINT, self.original_sigint)
                exit(1)

            os.kill(os.getpid(), signal.SIGUSR1)
        if sys.platform == 'win32':
            actual_exit()
        else:
            _thread.start_new_thread(actual_exit, ())

    def actual_exit(self, signum, frame):
        exit(1)

    def send_disconnect_message(self):
        for client_id in self.client_store.map.keys():
            print(client_id)
            event = DisconnectedNotification()
            event.destination = f'remote://websocket/{client_id}'
            event.correlation_id = str(uuid4())
            event.system_entry = str(datetime.datetime.now())
            self.event_queue.add_event(event)
