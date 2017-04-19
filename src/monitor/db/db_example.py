from peewee import *
import datetime
import os

database = SqliteDatabase('test.db')

class BaseModel(Model):
    class Meta:
        database = database

class Sensor(BaseModel):
    name = CharField(unique=True)
    added_date = DateTimeField(default=datetime.datetime.now)

class MeasurementType(BaseModel):
    name = CharField(unique=True)

class Measurement(BaseModel):
    sensor = ForeignKeyField(Sensor)
    type = ForeignKeyField(MeasurementType)
    value = DoubleField()
    added_date = DateTimeField(default=datetime.datetime.now)

database.connect()
database.create_tables([Sensor,MeasurementType,Measurement])

s = Sensor.create(name='Sensor')
cpu = MeasurementType.create(name='CPU')
gpu = MeasurementType.create(name='GPU')
hdd = MeasurementType.create(name='HDD')
Measurement.create(sensor=s,type=cpu,value=1.1)
Measurement.create(sensor=s,type=gpu,value=1.2)
Measurement.create(sensor=s,type=hdd,value=1.3)
Measurement.create(sensor=s,type=cpu,value=2.1)
Measurement.create(sensor=s,type=gpu,value=2.2)
Measurement.create(sensor=s,type=hdd,value=2.3)

print(s.name,'measurements:')
for m in Measurement.select().where(Measurement.sensor == s):
    print(m.type.name,m.value,m.added_date)

database.close()

os.remove('test.db')