from pathlib import Path

project_name: str = input('Name of project:')

main_template = '''
import os
from typing import Type, List

import pymongo
from dotenv import load_dotenv

from autumn import ExceptionHandler, Handler, HandlerBootstrapper, RepositoryExtension, MongoRepositoryFactory, \
    ExtensionBootstrapper
from autumn.event_dispatcher import EventDispatcher
from autumn.event_queue import EventQueue
from autumn.exit_state import ExitState
from autumn.store.client_store import ClientStore
from autumn.store.correlation_store import CorrelationStore
from autumn.store.thread_store import ThreadStore
from autumn.topic.topic_factory import TopicFactory
from autumn.websocket_server import WebsocketServer

handlers: 'List[Type[Handler]]' = []

extensions: 'List[Type[RepositoryExtension]]' = []

if __name__ == '__main__':
    load_dotenv('./.env')

    mongo_client = pymongo.MongoClient(f'mongodb://{os.environ["MONGODB_SERVER"]}:27017/')

    correlation_store = CorrelationStore()
    client_store = ClientStore()
    thread_store = ThreadStore()
    event_queue = EventQueue()
    handler_map = {}

    exception_handler = ExceptionHandler(event_queue)
    topic_factory = TopicFactory(event_queue)
    handler_bootstrapper = HandlerBootstrapper(handlers)
    repository_extension_bootstrapper = ExtensionBootstrapper(extensions)
    repository_factory = MongoRepositoryFactory(mongo_client, repository_extension_bootstrapper)

    exit_state = ExitState(topic_factory.get_topic('server_notifications'), client_store, thread_store, event_queue)

    event_dispatcher = EventDispatcher(event_queue, correlation_store, thread_store, client_store, exception_handler,
                                       topic_factory, repository_factory, handler_bootstrapper, exit_state,
                                       handler_map=handler_map)

    websocketServer = WebsocketServer(correlation_store, event_dispatcher, client_store, event_queue, exception_handler,
                                      topic_factory, exit_state)

    websocketServer.run(os.environ['HOST'], int(os.environ['PORT']))

'''
Path(f'./{project_name}').mkdir(parents=True)
Path(f'./{project_name}/contract').mkdir(parents=True)
Path(f'./{project_name}/contract/response').mkdir(parents=True)
Path(f'./{project_name}/contract/notification').mkdir(parents=True)
Path(f'./{project_name}/repository/repository_extension').mkdir(parents=True)
Path(f'./{project_name}/handler').mkdir(parents=True)

with open(f'./{project_name}/main.py', 'w') as f:
    f.write(main_template)

print(f'Created folder {project_name} with necessary folder structure!')

import socket

valid = False

while not valid:
    try:
        ip = input('The server should run on address: ')
        socket.inet_aton(ip)
        valid = True
    except socket.error as e:
        print(f'{ip} is not a valid address!')

valid = False
while not valid:
    try:
        port = int(input('The server must run on port: '))
        valid = True
    except ValueError as e:
        print(f'{port} is not a valid port!')

valid = False
while not valid:
    try:
        address = input('The mongodb server should run on address: ')
        socket.inet_aton(address)
        valid = True
    except socket.error as e:
        print(f'{address} is not a valid address!')

dot_env_file = f'MONGODB_SERVER={address}\nHOST={ip}\nPORT={port}\n'

with open(f'./{project_name}/.env', 'w') as f:
    f.write(dot_env_file)

print(f'Done! You can run the server by typing python3 main.py in the {project_name} folder!')


