import unittest
from flask import json
from src.authentication_service.rest import service


class TestRest(unittest.TestCase):
    def setUp(self):
        service.config['TESTING'] = True
        self.app = service.test_client()

    def test_login(self):
        data = {'login': 'user', 'password': 'pass'}
        r = self.app.post('/login', data=json.dumps(data), content_type='application/json')
        rj = json.loads(r.data.decode("utf-8"))
        assert rj["jwt"] is not None

        data = {'login': 'user'}
        r = self.app.post('/login', data=json.dumps(data), content_type='application/json')
        assert r.status_code == 400

    def test_register(self):
        data = {'login': 'user', 'password': 'pass', 'password_confirmation': 'pass'}
        r = self.app.post('/register', data=json.dumps(data), content_type='application/json')
        assert r.status_code == 200

        data = {'login': 'user', 'password': 'pass'}
        r = self.app.post('/register', data=json.dumps(data), content_type='application/json')
        assert r.status_code == 400