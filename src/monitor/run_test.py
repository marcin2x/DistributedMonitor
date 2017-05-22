import os
import test
from unittest import TestLoader, TextTestRunner, TestSuite

from src.monitor.db import model


model.createTestData()
model.database.close()

loader = TestLoader()
suite = TestSuite((
        loader.loadTestsFromTestCase(test.measurements_test.TestMeasurements),
        loader.loadTestsFromTestCase(test.hosts_test.TestHosts),
        ))

TextTestRunner(verbosity=2).run(suite)
