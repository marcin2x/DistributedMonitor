import unittest

from flask import json

from app import app


class TestHosts(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_get_sensors(self):
        r = self.app.get('/hosts', content_type='application/json')
        rj = json.loads(r.data.decode("utf-8"))
        assert len(rj) == 2

        r = self.app.get('/hosts?name=PC', content_type='application/json')
        rj = json.loads(r.data.decode("utf-8"))
        assert len(rj) == 1
        assert len(rj[0]['measurements']) == 2  # 2 measurements for sensor PC in test db

        r = self.app.get('/hosts?name=Lap', content_type='application/json')
        rj = json.loads(r.data.decode("utf-8"))
        assert len(rj[0]['measurements']) == 4  # 4 measurements for sensor Laptop in test db
        assert len(rj) == 1
