import unittest

from ..sensor_data_request import SensorDataRequest
from ..exceptions import *


class TestSensorDataRequest(unittest.TestCase):
    sensor_id = 12
    values = [
        {
            "measurement_id": 19,
            "measurement_value": "95"
        },
        {
            "measurement_id": 20,
            "measurement_value": "15"
        },
    ]

    def test_valid_parameters(self):
        request = SensorDataRequest(self.sensor_id, self.values)
        self.assertIsInstance(request, SensorDataRequest)

    def test_missing_parameter(self):
        with self.assertRaises(MissingSensorDataRequestParameterException):
            SensorDataRequest(self.sensor_id, None)

    def test_invalid_sensor_id_parameter(self):
        with self.assertRaises(InvalidSensorDataRequestParameterException):
            SensorDataRequest("12", self.values)

    def test_invalid_values_parameter(self):
        invalid_values = {
            "measurement_id": 19,
            "measurement_value": "95"
        }
        with self.assertRaises(InvalidSensorDataRequestParameterException):
            SensorDataRequest(self.sensor_id, invalid_values)

        invalid_values = [
            "measurement_id",
            19,
            "measurement_value",
            "95"
        ]
        with self.assertRaises(InvalidSensorDataRequestParameterException):
            SensorDataRequest(self.sensor_id, invalid_values)

        invalid_values = [
            {
                "measurement_id": 19,
                "measurement_value": "95"
            },
            {
                20: "15"
            }
        ]
        with self.assertRaises(InvalidSensorDataRequestParameterException):
            SensorDataRequest(self.sensor_id, invalid_values)
