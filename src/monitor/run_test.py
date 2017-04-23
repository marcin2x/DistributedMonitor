import test
from unittest import TestLoader, TextTestRunner, TestSuite

loader = TestLoader()

suite = TestSuite((
        loader.loadTestsFromTestCase(test.auth_test.TestAuth),
        loader.loadTestsFromTestCase(test.measurements_test.TestMeasurements),
        loader.loadTestsFromTestCase(test.sensors_test.TestSensors),
        ))

TextTestRunner(verbosity=2).run(suite)
