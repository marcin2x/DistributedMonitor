import unittest
from src.authentication_service.data.db_provider import DbProvider

class TestDb(unittest.TestCase):

    def test_db_conn(self):
        db = DbProvider()
        db.close()
        db.connect()
        db.close()

