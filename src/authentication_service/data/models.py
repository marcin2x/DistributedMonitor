from peewee import *
from src.authentication_service.data.config import database

class BaseModel(Model):
    class Meta:
        database = database

class User(BaseModel):
    login = CharField(unique=True)
    password = CharField()

class Monitor(BaseModel):
    name = CharField(unique=True)
    port = CharField()
    address = CharField()
    user = ForeignKeyField(User)