import unittest

from ..exceptions import *
from ..sensor_data_response import SensorDataResponse


class TestSensorDataResponse(unittest.TestCase):
    body = "OK"

    def test_missing_parameter(self):
        response = SensorDataResponse(self.body)
        self.assertIsInstance(response, SensorDataResponse)

    def test_invalid_body_parameter(self):
        with self.assertRaises(InvalidSensorDataResponseParameterException):
            SensorDataResponse(1)
