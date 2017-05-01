import unittest

from ..serializer import *


class TestSerializer(unittest.TestCase):
    id = 1
    name = "test name"
    measurements = [
        {
            "name": "CPU"
        },
    ]
    metadata = [
        {
            "key": "Total RAM",
            "value": "8GB"
        },
    ]

    def test_serialize(self):
        request = SensorRegisterRequest(self.id, self.name, self.measurements, self.metadata)

        serialized_request = serialize(request)

        assert type(serialized_request) == bytes

    def test_deserialize_message(self):
        request = SensorRegisterRequest(self.id, self.name, self.measurements, self.metadata)
        serialized_request = serialize(request)

        deserialized_request = deserialize_request(serialized_request)

        assert deserialized_request.__class__ == SensorRegisterRequest

        assert deserialized_request.identifier == self.id
        assert deserialized_request.name == self.name
        assert deserialized_request.measurements == self.measurements
        assert deserialized_request.metadata == self.metadata

    def test_deserialize_invalid_message(self):
        request = SensorRegisterRequest(self.id, self.name, self.measurements, self.metadata)
        request.type = "invalid_type"

        serialized_request = serialize(request)

        with self.assertRaises(InvalidSensorMessageTypeException):
            deserialize_request(serialized_request)
