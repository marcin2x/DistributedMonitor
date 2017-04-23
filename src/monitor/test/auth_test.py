import unittest

from flask import json

from app import app


class TestAuth(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

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
