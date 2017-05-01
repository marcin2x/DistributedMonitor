from src.authentication_service.data.config import database
from src.authentication_service.data.models import User, Monitor

class DbProvider:

    def __init__(self):
        self.database = database
        self.database.create_tables([User, Monitor], safe=True)

    def connect(self):
        self.database.connect()

    def close(self):
        self.database.close()

dbProvider = DbProvider()