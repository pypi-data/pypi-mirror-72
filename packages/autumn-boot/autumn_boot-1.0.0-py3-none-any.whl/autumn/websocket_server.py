import asyncio
import ssl
from datetime import datetime
from uuid import uuid4

import websockets

from .exit_state import ExitState
from . import serializer
from .client import Client
from .events.client_disconnected import ClientDisconnectedNotification
from .topic.topic_factory import TopicFactory


class WebsocketServer:
    def __init__(self, correlation_store, event_dispatcher, client_store, event_queue, exception_handler,
                 topic_factory, exit_state: ExitState):
        self.correlation_store = correlation_store
        self.event_dispatcher = event_dispatcher
        self.client_store = client_store
        self.event_queue = event_queue
        self.exception_handler = exception_handler
        self.topic_factory: TopicFactory = topic_factory
        self.exit_state: ExitState = exit_state
        self.number_of_incoming_events = 0

    async def send_heartbeat(self):
        while True:
            to_disconnect = []
            for client_id in self.client_store.keys():
                if not self.should_disconnect(client_id):
                    await self.send_to(client_id, 'HEARTBEAT')
                else:
                    to_disconnect.append(client_id)

            for client_id in to_disconnect:
                await self.unregister(client_id)

            await asyncio.sleep(5)

    async def register(self, websocket):
        client_id = str(uuid4())
        self.client_store.add(client_id, Client(client_id, websocket))
        await websocket.send('REGISTERED')
        return client_id

    async def unregister(self, client_id):
        client = self.client_store.get(client_id)
        await client.websocket.close()

        self.client_store.remove(client_id)

    def should_disconnect(self, client_id):
        client = self.client_store.get(client_id)
        since_heartbeat = (datetime.now() - client.last_heartbeat).seconds

        return True if since_heartbeat >= 5 or client.websocket.closed else False

    def got_client_heartbeat(self, client_id):
        client = self.client_store.get(client_id)
        client.last_heartbeat = datetime.now()

    async def websocket_connection_handler(self, websocket, path):
        client_id = await self.register(websocket)
        started_to_handle = set()

        try:
            while not self.exit_state.should_exit:
                correlation_id = str(uuid4())
                self.correlation_store.add(correlation_id, client_id)
                started_to_handle.add(correlation_id)

                message = await websocket.recv()

                if message == 'HEARTBEAT':
                    self.got_client_heartbeat(client_id)
                else:
                    try:
                        event = serializer.deserialize(
                            message, correlation_id, client_id)
                        event.return_address = f'remote://websocket/{client_id}'
                        self.event_queue.add_event(event)
                        self.number_of_incoming_events += 1
                    except Exception as e:
                        event = type('evt', (object,), dict(system_entry=str(
                            datetime.now()), destination=f'remote://websocket/{client_id}'))()

                        self.exception_handler.handle_exception(
                            e, event)
        except Exception as exception:
            print(
                f'client {client_id} suddenly disconnected. Reason: {type(exception).__name__} -> {exception}')
            self.client_store.remove(client_id)
            self.topic_factory.remove_client(client_id)
            self.topic_factory.get_topic('server_notifications').publish(ClientDisconnectedNotification(client_id),
                                                                         str(uuid4()))

    async def send_to(self, client_id, contents):
        client = self.client_store.get(client_id)
        if client:
            await client.websocket.send(contents)

    def run(self, address: str, port: int, ssl_context: ssl.SSLContext = None):
        start_server = websockets.serve(
            self.websocket_connection_handler, address, port, ssl=ssl_context)

        event_loop = asyncio.get_event_loop()
        heartbeat_task = event_loop.create_task(self.send_heartbeat())
        event_coroutine = event_loop.create_task(
            self.event_dispatcher.dispatch())

        print(f'Running on {"wss" if ssl_context else "ws"}://{address}:{port}')
        event_loop.run_until_complete(start_server)
        event_loop.run_until_complete(heartbeat_task)
        event_loop.run_until_complete(event_coroutine)