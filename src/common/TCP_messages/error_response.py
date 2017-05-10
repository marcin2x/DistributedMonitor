from .sensor_message import SensorMessage
from .exceptions import *


class ErrorResponse(SensorMessage):
    type = "error"

    def __init__(self, body):
        if body is None:
            raise MissingErrorResponseParameterException("body")

        if type(body) is not str:
            raise InvalidErrorResponseParameterException("Parameter \"body\" must be of type \"string\"")

        self.body = body

    def get_message_body(self):
        return self.body
