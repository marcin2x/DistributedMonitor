import unittest

from ..exceptions import *
from ..sensor_register_response import SensorRegisterResponse


class TestSensorRegisterResponse(unittest.TestCase):
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

    def test_valid_parameters(self):
        response = SensorRegisterResponse(self.sensor_id, self.measurements)
        self.assertIsInstance(response, SensorRegisterResponse)

    def test_missing_parameter(self):
        with self.assertRaises(MissingSensorRegisterResponseParameterException):
            SensorRegisterResponse(self.sensor_id, None)

    def test_invalid_sensor_id_parameter(self):
        with self.assertRaises(InvalidSensorRegisterResponseParameterException):
            SensorRegisterResponse("12", self.measurements)

    def test_invalid_measurements_parameter(self):
        with self.assertRaises(InvalidSensorRegisterResponseParameterException):
            SensorRegisterResponse(self.sensor_id, {})

        invalid_measurements = [
            "CPU",
            "RAM",
        ]
        with self.assertRaises(InvalidSensorRegisterResponseParameterException):
            SensorRegisterResponse(self.sensor_id, invalid_measurements)

        invalid_measurements = [
            {
                "measurements_name": "CPU",
                "measurements_id": 19
            },
            {
                "RAM": 20
            }
        ]
        with self.assertRaises(InvalidSensorRegisterResponseParameterException):
            SensorRegisterResponse(self.sensor_id, invalid_measurements)
