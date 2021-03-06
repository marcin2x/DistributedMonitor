from src.authentication_service.data.models import User, Monitor
from peewee import DoesNotExist

class UserRepository:

    def save(self, login, password):
        return User.create(login=login,password=password)

    def findById(self, id):
        return User.get(User.id == id)

    def findByLogin(self, login):
        users = User.select().where(User.login == login)
        if len(users) == 0:
            return None
        return users[0]

    def isUnique(self, login):
        return len(User.select().where(User.login == login)) == 0


class MonitorRepository:

    def save(self, name, port, address, user):
        return Monitor.create(name=name, port=port, address=address, user=user)

    def find(selfs, id):
        return Monitor.get(Monitor.id == id)

    def delete(self, monitor):
        monitor.delete_instance()

    def findAllForUser(self, user):
        try:
            return list(Monitor.select().where(Monitor.user == user))
        except DoesNotExist:
            return []

    def findAll(self):
        try:
            return list(Monitor.select())
        except DoesNotExist:
            return []

    def isUnique(self, name):
        return len(Monitor.select().where(Monitor.name == name)) == 0
