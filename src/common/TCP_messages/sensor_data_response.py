from .sensor_message import SensorMessage
from .exceptions import *


class SensorDataResponse(SensorMessage):
    type = "data"

    def __init__(self, body):
        if body is None:
            raise MissingSensorDataResponseParameterException("body")

        if type(body) is not str:
            raise InvalidSensorDataResponseParameterException("Parameter \"body\" must be of type \"string\"")

        self.body = body

    def get_message_body(self):
        return self.body
