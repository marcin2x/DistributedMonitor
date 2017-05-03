from .exceptions import *
from .sensor_message import SensorMessage


class SensorRegisterRequest(SensorMessage):
    type = "register"

    def __init__(self, identifier, name, measurements, metadata):
        if identifier is None:
            raise MissingSensorRegisterRequestParameterException("identifier")

        if type(identifier) is not str:
            raise InvalidSensorRegisterRequestParameterException("Parameter \"identifier\" must be of type \"str\"")

        self.identifier = identifier

        if name is None:
            raise MissingSensorRegisterRequestParameterException("name")

        if type(name) is not str:
            raise InvalidSensorRegisterRequestParameterException("Parameter \"name\" must be of type \"string\"")

        self.name = name

        if measurements is None:
            raise MissingSensorRegisterRequestParameterException("measurements")

        if type(measurements) is not list:
            raise InvalidSensorRegisterRequestParameterException("Parameter \"measurements\" must be of type \"list\"")

        for measurement in measurements:
            if type(measurement) is not dict:
                raise InvalidSensorRegisterRequestParameterException("Parameter \"measurements\" can only contain objects of type \"dictionary\"")
            if "name" not in measurement:
                raise InvalidSensorRegisterRequestParameterException("Elements of parameter \"measurements\" should have key \"name\"")

        self.measurements = measurements

        if metadata is None:
            raise MissingSensorRegisterRequestParameterException("metadata")

        if type(metadata) is not list:
            raise InvalidSensorRegisterRequestParameterException("Parameter \"metadata\" must be of type \"list\"")

        for metadata_element in metadata:
            if type(metadata_element) is not dict:
                raise InvalidSensorRegisterRequestParameterException("Parameter \"metadata\" can only contain objects of type \"dictionary\"")
            if "key" not in metadata_element:
                raise InvalidSensorRegisterRequestParameterException("Elements of parameter \"metadata\" should have key \"key\"")
            if "value" not in metadata_element:
                raise InvalidSensorRegisterRequestParameterException("Elements of parameter \"metadata\" should have key \"value\"")

        self.metadata = metadata

    def get_message_body(self):
        return {
            "identifier": self.identifier,
            "name": self.name,
            "measurements": self.measurements,
            "metadata": self.metadata
        }
