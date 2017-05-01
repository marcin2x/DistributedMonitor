from .exceptions import *
from .sensor_message import SensorMessage


class SensorRegisterResponse(SensorMessage):
    type = "register"

    def __init__(self, sensor_id, measurements):
        if sensor_id is None:
            raise MissingSensorRegisterResponseParameterException("sensor_id")

        if type(sensor_id) is not int:
            raise InvalidSensorRegisterResponseParameterException("Parameter \"sensor_id\" must be of type \"int\"")

        self.sensor_id = sensor_id

        if measurements is None:
            raise MissingSensorRegisterResponseParameterException("measurements")

        if type(measurements) is not list:
            raise InvalidSensorRegisterResponseParameterException("Parameter \"measurements\" must be of type \"list\"")

        for measurement in measurements:
            if type(measurement) is not dict:
                raise InvalidSensorRegisterResponseParameterException("Elements of parameter \"measurements\" must be of type \"dictionary\"")
            if "measurements_name" not in measurement:
                raise InvalidSensorRegisterResponseParameterException("Elements of parameter \"measurements\" should have key \"measurements_name\"")
            if "measurements_id" not in measurement:
                raise InvalidSensorRegisterResponseParameterException("Elements of parameter \"measurements\" should have key \"measurements_id\"")

        self.measurements = measurements

    def get_message_body(self):
        return {
            "sensor_id": self.sensor_id,
            "measurements": self.measurements
        }
