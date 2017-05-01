import socketserver
import json
from src.common.TCP_messages import *


BUFFER_SIZE = 1024


class TCPHandler(socketserver.BaseRequestHandler):
    data = bytes()

    def handle(self):
        while True:
            chunk = self.request.recv(BUFFER_SIZE)
            self.data += chunk

            if len(chunk) < BUFFER_SIZE:
                break

        deserialized_request = deserialize_request(self.data)

        if deserialized_request.type == "register":
            # TODO: handle register request
            # deserialized_request.identifier
            # deserialized_request.name
            # deserialized_request.measurements
            # deserialized_request.metadata

            # Example response:
            sensor_id = 12
            measurements = [
                {
                    "measurements_name": "CPU",
                    "measurements_id": 19
                },
                {
                    "measurements_name": "RAM",
                    "measurements_id": 20
                },
            ]
            response = SensorRegisterResponse(sensor_id, measurements)

        elif deserialized_request.type == "data":
            # TODO: handle data request
            # deserialized_request.sensor_id
            # deserialized_request.values

            # Example response:
            response = SensorDataResponse("OK")

        else:
            raise InvalidSensorMessageTypeException(deserialized_request.type)

        self.request.send(serialize(response))


def run():
    with open('tcp_server_config.json') as config_file:
        config = json.load(config_file)

    server = socketserver.TCPServer((config['host'], config['port']), TCPHandler)
    server.serve_forever()
