import unittest

from app import app
from flask import json

from src.authentication_service.data.models import User
from src.authentication_service.utils.jwt import JwtManager


class TestMeasurements(unittest.TestCase):
    def setUp(self):
        # model.createTestData()
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.jwtManager = JwtManager()

    def test_get_measurements(self):
        r = self.app.get('/measurements?names=test', content_type='application/json')
        rj = json.loads(r.data.decode("utf-8"))

    def test_get_values(self):
        r = self.app.get('/measurements/values', content_type='application/json')
        rj = json.loads(r.data.decode("utf-8"))
        assert rj is not None
        assert len(rj) > 0

        r = self.app.get('/measurements/values?count=30', content_type='application/json')
        rj = json.loads(r.data.decode("utf-8"))
        assert len(rj) == 30

        r = self.app.get('/measurements/values?offset=10', content_type='application/json')
        rj = json.loads(r.data.decode("utf-8"))
        assert len(rj) == 30

        r = self.app.get('/measurements/values?host_name=Laptop', content_type='application/json')
        rj = json.loads(r.data.decode("utf-8"))
        assert len(rj) == 20  # 20 values in sample db
        r = self.app.get('/measurements/values?host_name=PC', content_type='application/json')
        rj = json.loads(r.data.decode("utf-8"))
        assert len(rj) == 20  # 20 values in sample db

        r = self.app.get('/measurements/values?measurement_id=1', content_type='application/json')
        rj = json.loads(r.data.decode("utf-8"))
        assert len(rj) == 10  # 10 values in sample db

    def test_get_values_by_id(self):
        r = self.app.get('/measurements/1/values', content_type='application/json')
        rj = json.loads(r.data.decode("utf-8"))
        assert len(rj) == 10  # 10 values in sample db

    def test_create_delete_complex_measurement(self):
        user = User()
        user.set_id("test_id")
        user.login = "user1"
        token = self.jwtManager.generate(user)
        data = {"name": "Test-Complex", "type": "avg", "interval": 7, "window": 30, "measurement_id": 1}
        r = self.app.post('/measurements',
                          data=json.dumps(data),
                          content_type='application/json',
                          headers={'Authorization': token})
        rj = json.loads(r.data.decode("utf-8"))
        assert rj['measurement_id'] is not None

        r = self.app.delete('/measurements/' + str(int(rj['measurement_id'])),
                            content_type='application/json',
                            headers={'Authorization': token})
        assert r.status_code == 200
