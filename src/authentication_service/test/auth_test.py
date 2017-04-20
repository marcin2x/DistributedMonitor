import unittest
import jwt
from src.common.authconfig import jwtsecret, jwtalgorithm

class TestAuth(unittest.TestCase):

    def test_auth(self):
      testdata = {
            "sub": "1234567890",
            "name": "John Doe",
            "admin": True
        }

      encoded = jwt.encode(testdata, jwtsecret, algorithm=jwtalgorithm)
      decoded = jwt.decode(encoded, jwtsecret, algorithms=[jwtalgorithm])

      assert testdata['sub'] == decoded['sub'], "sub does not match"
      assert testdata['name'] == decoded['name'], "name does not match"
      assert testdata['admin'] == decoded['admin'], "admin does not match"