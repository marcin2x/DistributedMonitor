from .sensor_message import SensorMessage
from .exceptions import *


class SensorDataRequest(SensorMessage):
    type = "data"

    def __init__(self, sensor_id, values):
        if sensor_id is None:
            raise MissingSensorDataRequestParameterException("sensor_id")

        if type(sensor_id) is not int:
            raise InvalidSensorDataRequestParameterException("Parameter \"sensor_id\" must be of type \"int\"")

        self.sensor_id = sensor_id

        if values is None:
            raise MissingSensorDataRequestParameterException("values")

        if type(values) is not list:
            raise InvalidSensorDataRequestParameterException("Parameter \"values\" should be of type \"list\"")

        for value in values:
            if type(value) is not dict:
                raise InvalidSensorDataRequestParameterException("Elements of parameter \"values\" should be of type \"dictionary\"")
            if "measurement_id" not in value:
                raise InvalidSensorDataRequestParameterException("Elements of parameter \"values\" should have key \"measurement_id\"")
            if "measurement_value" not in value:
                raise InvalidSensorDataRequestParameterException("Elements of parameter \"values\" should have key \"measurement_value\"")

        self.values = values

    def get_message_body(self):
        return {
            "sensor_id": self.sensor_id,
            "values": self.values
        }
