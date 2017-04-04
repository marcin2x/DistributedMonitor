import unittest

from flask import json

from app import app


class TestMeasurements(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_get_measurements(self):
        r = self.app.get('/measurements?names=test', content_type='application/json')
        rj = json.loads(r.data.decode("utf-8"))

    def test_post_measurements(self):
        data = {'sensor_name': 'name', 'measurement_name': 'name', 'metadata': {}}
        r = self.app.post('/measurements', data=json.dumps(data), content_type='application/json')
        assert r.status_code == 200

        data = {'sensor_name': 'name', 'measurement_name': 'name'}
        r = self.app.post('/measurements', data=json.dumps(data), content_type='application/json')
        assert r.status_code == 400

    def test_put_measurements_with_id(self):
        data = {'sensor_id': '1', 'metadata': {}}
        r = self.app.put('/measurements/1', data=json.dumps(data), content_type='application/json')
        assert r.status_code == 200

        data = {'sensor_id': '1'}
        r = self.app.put('/measurements/1', data=json.dumps(data), content_type='application/json')
        assert r.status_code == 400

    def test_get_values(self):
        r = self.app.get('/measurements/values', content_type='application/json')
        rj = json.loads(r.data.decode("utf-8"))
        assert rj is not None

    def test_create_complex_measurement(self):
        data = {'measurements_id': '123', 'jwt': 'token'}
        r = self.app.post('/measurements/complex', data=json.dumps(data), content_type='application/json')
        rj = json.loads(r.data.decode("utf-8"))
        assert rj['measurement_id'] is not None





