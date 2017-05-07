from peewee import *
import datetime
from src.common.TCP_messages import *
import json
import os.path
from playhouse.shortcuts import model_to_dict

filename = ''
with open('db_config.json') as config_file:
    config = json.load(config_file)
    filename = config['path']

if filename is '':
    raise Exception("Config file: \"db_config.json\" with field \"path\" is required.")

db = SqliteDatabase(filename)


class BaseModel(Model):
    class Meta:
        database = db


class Sensor(BaseModel):
    identifier = CharField(unique=True)
    name = CharField()
    created = DateTimeField(default=datetime.datetime.utcnow)


class Metadata(BaseModel):
    key = CharField()
    value = CharField()
    sensor = ForeignKeyField(Sensor, related_name='metadatas')


class Measurement(BaseModel):
    name = CharField()
    description = CharField(null=True)
    sensor = ForeignKeyField(Sensor, related_name='measurements')
    created = DateTimeField(default=datetime.datetime.utcnow)


class MeasurementValue(BaseModel):
    value = DoubleField()
    measurement = ForeignKeyField(Measurement, related_name='values')
    created = DateTimeField(default=datetime.datetime.utcnow)


class DatabaseModel(Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.database = db
        exists = os.path.isfile(filename)
        self.database.connect()
        if not exists:
            self.createTables()

        self.database.close()

    def createTables(self):
        self.database.create_tables([Sensor, Metadata, Measurement, MeasurementValue])

    def connect(self):
        self.database.connect()

    def close(self):
        if not self.database.is_closed():
            self.database.close()

    def registerSensor(self, request):
        try:
            s = Sensor.get(identifier=request.identifier)
        except DoesNotExist:
            s = Sensor.create(identifier=request.identifier, name=request.name)

        for m in request.measurements:
            Measurement.get_or_create(name=m['name'], description=m['description'], sensor=s)
        for m in request.metadata:
            try:
                m1 = Metadata.get(key=m['key'], sensor=s)
                m1.value = m['value']
                m1.save()
            except DoesNotExist:
                Metadata.create(key=m['key'],value=m['value'],sensor=s)

        return SensorRegisterResponse(s.id,
                                      [{'measurements_name': m.name,
                                        'measurements_id': m.id}
                                       for m in
                                       Measurement.select().where(Measurement.sensor == s)])

    def createSensorData(self, request):
        try:
            s = Sensor.get(Sensor.id == request.sensor_id)
            self.database.begin()
            for v in request.values:
                try:
                    m = Measurement.get(Measurement.id == v['measurement_id'], Measurement.sensor == s)
                    MeasurementValue.create(value=v['measurement_value'], measurement=m)
                except DoesNotExist:
                    db.rollback()
                    return ErrorResponse("Measurement with id " + str(v['measurement_id']) + " does not exist.")

            self.database.commit()
        except DoesNotExist:
            return ErrorResponse("Sensor with id " + str(request.sensor_id) + " does not exist.")

        return SensorDataResponse("OK")

    def getMeasurementValues(self, request):
        id = request.args.get('measurement_id') or None
        hostName = request.args.get('host_name') or None
        timeFrom = request.args.get('time_from') or None
        timeTo = request.args.get('time_to') or None
        count = request.args.get('count') or 50
        offset = request.args.get('offset') or 0

        query = MeasurementValue.select()

        conditions = []
        if id:
            query = query.join(Measurement, on=MeasurementValue.measurement, join_type=JOIN_LEFT_OUTER)
            conditions.append(Measurement.id == id)

        if hostName:
            if not id:
                query = query.join(Measurement, on=MeasurementValue.measurement, join_type=JOIN_LEFT_OUTER)

            query = query.join(Sensor, on=Measurement.sensor, join_type=JOIN_LEFT_OUTER)
            conditions.append(Sensor.name % str('*' + hostName + '*'))

        if timeFrom:
            conditions.append(MeasurementValue.created > datetime.datetime.strptime(str(timeFrom), "%Y-%m-%dT%H:%M:%S"))

        if timeTo:
            conditions.append(MeasurementValue.created <= datetime.datetime.strptime(str(timeTo), "%Y-%m-%dT%H:%M:%S"))

        try:
            if len(conditions):
                query = query.where(*conditions)
            query = query.limit(int(count)).offset(int(offset))
        except DoesNotExist:
            return []

        return [{"host_name":v.measurement.sensor.name,
                 "measurement_id":v.measurement.id,
                 "value":v.value,
                 "date":v.created } for v in query]

    def getMeasurementValuesById(self, request, id):
        timeFrom = request.args.get('time_from') or None
        timeTo = request.args.get('time_to') or None
        count = request.args.get('count') or 50
        offset = request.args.get('offset') or 0

        query = MeasurementValue.select().join(Measurement, on=MeasurementValue.measurement, join_type=JOIN_LEFT_OUTER)
        conditions = [Measurement.id == id]

        if timeFrom:
            conditions.append(MeasurementValue.created > datetime.datetime.strptime(str(timeFrom), "%Y-%m-%dT%H:%M:%S"))

        if timeTo:
            conditions.append(MeasurementValue.created <= datetime.datetime.strptime(str(timeTo), "%Y-%m-%dT%H:%M:%S"))

        try:
            if len(conditions):
                query = query.where(*conditions).order_by(-MeasurementValue.created)

                query = query.limit(int(count)).offset(int(offset))
        except DoesNotExist:
            return []

        return [{"value":v.value,
                 "date":v.created } for v in query]

    def getSensors(self, request):
        hostName = request.args.get('name') or None
        count = request.args.get('count') or 50
        offset = request.args.get('offset') or 0

        query = Sensor.select()

        conditions = []
        if hostName:
            conditions.append(Sensor.name % str('*' + hostName + '*'))

        try:
            if len(conditions):
                query = query.where(*conditions)
            query = query.limit(int(count)).offset(int(offset))
        except DoesNotExist:
            return []

        return [{"id":s.id,
                 "name":s.name,
                 "measurements":[{"id":m.id,
                                  "description":m.description}
                                  for m in s.measurements],
                 "metadata": [{"key": m.key,
                               "value": m.value}
                               for m in s.metadatas],
                 }
                 for s in query]

    def sensorExistsById(self, id):
        try:
            Sensor.get(Sensor.id == id)
            return True
        except DoesNotExist:
            return False

    def sensorExistsByName(self, name):
        try:
            Sensor.get(Sensor.name == name)
            return True
        except DoesNotExist:
            return False

    def measurementExistsById(self, id):
        try:
            Measurement.get(Measurement.id == id)
            return True
        except DoesNotExist:
            return False

    def measurementExistsByName(self, name):
        try:
            Measurement.get(Measurement.name == name)
            return True
        except DoesNotExist:
            return False

    def measurementAssignedToSensor(self, measurementId, sensorId):
        try:
            Measurement.get(Measurement.id == measurementId, Measurement.sensor == sensorId)
            return True
        except DoesNotExist:
            return False

database = DatabaseModel()

def createTestData():
    database.connect()
    if Sensor.select().count() > 0:
        return

    for name in ["Laptop", "PC"]:
        s = Sensor.create(identifier=name,name=name)
        m1 = Measurement.create(name="CPU",description="Description",sensor=s)
        m2 = Measurement.create(name="GPU",description="Description",sensor=s)
        Metadata.create(key="Key1", value='Value1', sensor=s)
        Metadata.create(key="Key2", value='Value2', sensor=s)
        for m in [m1,m2]:
            for i in range(10):
                if m == m1:
                    MeasurementValue.create(value=i*2.0, measurement=m)
                else:
                    MeasurementValue.create(value=i * 2.0, measurement=m, created=datetime.datetime.now() + datetime.timedelta(days=1))
    database.close()

# createTestData()