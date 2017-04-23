import unittest

from flask import json

from app import app


class TestSensors(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_get_sensors(self):
        r = self.app.get('/sensors', content_type='application/json')
        rj = json.loads(r.data.decode("utf-8"))
        assert rj is not None
