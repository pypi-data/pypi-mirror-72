import os
from threading import Thread, active_count, enumerate
from time import sleep
import click

from .event_dispatcher import EventDispatcher
from .exit_state import ExitState
from .store.client_store import ClientStore
from .store.thread_store import ThreadStore
from .websocket_server import WebsocketServer


class InfoDisplay(Thread):
    def __init__(self, exit_state: ExitState, client_store: ClientStore, thread_store: ThreadStore, handler_map,
                 event_dispatcher: EventDispatcher, websocket_server: WebsocketServer):
        super(InfoDisplay, self).__init__()
        self.exit_state: ExitState = exit_state
        self.client_store = client_store
        self.thread_store = thread_store
        self.handler_map = handler_map
        self.event_dispatcher = event_dispatcher
        self.websocket_server = websocket_server

    def run(self) -> None:
        os.environ['TERM'] = 'xterm-256color'
        while not self.exit_state.should_exit:
            click.clear()
            number_of_dispatched_events = len(self.event_dispatcher.handle_times)
            avg = 0 if number_of_dispatched_events == 0 else sum(
                self.event_dispatcher.handle_times) / number_of_dispatched_events
            print(f'Currently running threads: {active_count()}\t\t'
                  f'Connected clients: {len(self.client_store.keys())}\t\t\t'
                  f'Running handlers: {len(self.handler_map.keys())}')
            print(f'Number of dispatched events: {self.event_dispatcher.number_of_handled_events}\t\t'
                  f'Number of incoming events: {self.websocket_server.number_of_incoming_events}\t\t'
                  f'Number of outgoing events: {self.event_dispatcher.number_of_outgoing_events}\t\t')
            print(f'Average handling delta: {avg}')
            
            print('Running threads:')
            for thread in enumerate():
                print(type(thread), end=' ## ')
            print()
            sleep(1)

        click.clear()
        print(f'Gracefully shutting down...')
