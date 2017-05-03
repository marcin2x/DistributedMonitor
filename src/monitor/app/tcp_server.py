import socketserver
import json
from src.common.TCP_messages import *
from src.monitor.db.model import database

BUFFER_SIZE = 1024


class TCPHandler(socketserver.BaseRequestHandler):
    data = bytes()

    def handle(self):
        try:
            while True:
                chunk = self.request.recv(BUFFER_SIZE)
                self.data += chunk

                if len(chunk) < BUFFER_SIZE:
                    break

            deserialized_request = deserialize_request(self.data)

            if deserialized_request.type == "register":
                response = database.registerSensor(deserialized_request)

            elif deserialized_request.type == "data":
                response = database.createSensorData(deserialized_request)

            else:
                raise InvalidSensorMessageTypeException(deserialized_request.type)

            serialized_response = serialize(response)

        except Exception as e:
            response = ErrorResponse(str(e) or e.__class__.__name__)
            serialized_response = serialize(response)
            print(e)

        self.request.send(serialized_response)


def run():
    with open('tcp_server_config.json') as config_file:
        config = json.load(config_file)

    server = socketserver.TCPServer((config['host'], config['port']), TCPHandler)
    server.serve_forever()
