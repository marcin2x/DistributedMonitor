import unittest

from ..sensor_register_request import SensorRegisterRequest
from ..exceptions import *


class TestSensorRegisterRequest(unittest.TestCase):
    id = 1
    name = "test name"
    measurements = [
        {
            "name": "CPU"
        },
        {
            "name": "RAM"
        },
    ]
    metadata = [
        {
            "key": "Total RAM",
            "value": "8GB"
        },
        {
            "key": "CPU core count",
            "value": "4"
        },
    ]

    def test_valid_parameters(self):
        request = SensorRegisterRequest(self.id, self.name, self.measurements, self.metadata)
        self.assertIsInstance(request, SensorRegisterRequest)

    def test_missing_parameter(self):
        with self.assertRaises(MissingSensorRegisterRequestParameterException):
            SensorRegisterRequest(self.id, self.name, self.measurements, None)

    def test_invalid_identifier_parameter(self):
        with self.assertRaises(InvalidSensorRegisterRequestParameterException):
            SensorRegisterRequest("1", self.name, self.measurements, self.metadata)

    def test_invalid_name_parameter(self):
        with self.assertRaises(InvalidSensorRegisterRequestParameterException):
            SensorRegisterRequest(self.id, 1234, self.measurements, self.metadata)

    def test_invalid_measurements_parameter(self):
        with self.assertRaises(InvalidSensorRegisterRequestParameterException):
            SensorRegisterRequest(self.id, self.name, {}, self.metadata)

        invalid_measurements = [
            "CPU",
            "RAM",
        ]
        with self.assertRaises(InvalidSensorRegisterRequestParameterException):
            SensorRegisterRequest(self.id, self.name, invalid_measurements, self.metadata)

        invalid_measurements = [
            {
                "name": "CPU"
            },
            {
                "invalid_key": "RAM"
            },
        ]
        with self.assertRaises(InvalidSensorRegisterRequestParameterException):
            SensorRegisterRequest(self.id, self.name, invalid_measurements, self.metadata)

    def test_invalid_metadata_parameter(self):
        invalid_metadata = {
            "CPU core count": "4"
        }
        with self.assertRaises(InvalidSensorRegisterRequestParameterException):
            SensorRegisterRequest(self.id, self.name, self.measurements, invalid_metadata)

        invalid_metadata = [
            "CPU core count",
            "4"
        ]
        with self.assertRaises(InvalidSensorRegisterRequestParameterException):
            SensorRegisterRequest(self.id, self.name, self.measurements, invalid_metadata)

        invalid_metadata = [
            {
                "key": "CPU core count",
                "value": "4"
            },
            {
                "CPU core count": "4"
            },
        ]
        with self.assertRaises(InvalidSensorRegisterRequestParameterException):
            SensorRegisterRequest(self.id, self.name, self.measurements, invalid_metadata)
