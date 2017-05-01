import src.authentication_service.test as test
from unittest import TestLoader, TextTestRunner, TestSuite

loader = TestLoader()

suite = TestSuite((
    loader.loadTestsFromTestCase(test.auth_test.TestAuth),
    loader.loadTestsFromTestCase(test.db_test.TestDb),
    loader.loadTestsFromTestCase(test.rest_test.TestRest)
))
TextTestRunner(verbosity=2).run(suite)