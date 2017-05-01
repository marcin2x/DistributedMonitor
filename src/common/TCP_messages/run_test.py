from unittest import TestLoader, TextTestRunner, TestSuite

from src.common.TCP_messages.test.sensor_data_request_test import TestSensorDataRequest
from src.common.TCP_messages.test.sensor_data_response_test import TestSensorDataResponse
from src.common.TCP_messages.test.sensor_register_request_test import TestSensorRegisterRequest
from src.common.TCP_messages.test.sensor_register_response_test import TestSensorRegisterResponse
from src.common.TCP_messages.test.serializer_test import TestSerializer


loader = TestLoader()

suite = TestSuite((
        loader.loadTestsFromTestCase(TestSerializer),
        loader.loadTestsFromTestCase(TestSensorRegisterRequest),
        loader.loadTestsFromTestCase(TestSensorRegisterResponse),
        loader.loadTestsFromTestCase(TestSensorDataRequest),
        loader.loadTestsFromTestCase(TestSensorDataResponse),
    ))

TextTestRunner(verbosity=2).run(suite)
