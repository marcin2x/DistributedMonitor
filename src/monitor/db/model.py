from peewee import *
import datetime
from src.common.TCP_messages import *
import json
import os.path
from src.monitor.db.exceptions import *

filename = ''
with open('db_config.json') as config_file:
    config = json.load(config_file)
    filename = config['path']

if filename is '':
    raise Exception("Config file: \"db_config.json\" with field \"path\" is required.")

db = SqliteDatabase(filename)


def nextid():
    measurementId = Measurement.select(fn.Max(Measurement.id)).scalar() or 0
    complexId = ComplexMeasurement.select(fn.Max(ComplexMeasurement.id)).scalar() or 0
    return max(measurementId, complexId) + 1


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
    id = PrimaryKeyField(default=nextid)
    name = CharField()
    description = CharField(null=True)
    sensor = ForeignKeyField(Sensor, related_name='measurements')
    created = DateTimeField(default=datetime.datetime.utcnow)


class ComplexMeasurement(BaseModel):
    id = PrimaryKeyField(default=nextid)
    name = CharField()
    measurement = ForeignKeyField(Measurement, related_name="complexes")
    interval = IntegerField()
    type = CharField()
    window = IntegerField()
    userid = CharField()
    created = DateTimeField(default=datetime.datetime.utcnow)

    def calculateValue(self, fromDate, toDate):
        values = self.values(fromDate, toDate)
        if self.type == 'max':
            return max(values)
        elif self.type == 'min':
            return min(values)
        elif self.type == 'avg':
            return float(sum(values)) / max(len(values), 1)

    def values(self, fromDate, toDate):
        query = MeasurementValue.select()\
                                                 .where(MeasurementValue.measurement == self.measurement,
                                                        MeasurementValue.created >= fromDate,
                                                        MeasurementValue.created <= toDate)
        return [v.value for v in query]



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
        self.database.create_tables([Sensor, Metadata, Measurement, ComplexMeasurement, MeasurementValue])

    def connect(self):
        if self.database.is_closed():
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
            Measurement.get_or_create(name=m['name'], description=m.get('description', ''), sensor=s)
        for m in request.metadata:
            try:
                m1 = Metadata.get(key=m['key'], sensor=s)
                m1.value = m['value']
                m1.save()
            except DoesNotExist:
                Metadata.create(key=m['key'], value=m['value'], sensor=s)

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
        order = request.args.get('order') or 'asc'
        onlyComplex = request.args.get('only_complex') or False

        query = MeasurementValue.select()

        conditions = []
        if id:
            query = query.join(Measurement, on=MeasurementValue.measurement, join_type=JOIN_LEFT_OUTER)
            conditions.append(Measurement.id == id)

        if hostName:
            if not id:
                query = query.join(Measurement, on=MeasurementValue.measurement, join_type=JOIN_LEFT_OUTER)

            query = query.join(Sensor, on=Measurement.sensor, join_type=JOIN_LEFT_OUTER)
            conditions.append(Sensor.name ** str('%' + hostName + '%'))

        if timeFrom:
            conditions.append(MeasurementValue.created > datetime.datetime.strptime(str(timeFrom), "%Y-%m-%dT%H:%M:%S"))

        if timeTo:
            conditions.append(MeasurementValue.created <= datetime.datetime.strptime(str(timeTo), "%Y-%m-%dT%H:%M:%S"))

        try:
            if len(conditions):
                query = query.where(*conditions)
            if order == 'asc':
                query = query.order_by(+MeasurementValue.created)
            elif order == 'desc':
                query = query.order_by(-MeasurementValue.created)

            query = query.limit(int(count)).offset(int(offset))
            if not query:
                raise DoesNotExist
        except DoesNotExist:
            if not id:
                return []

            conditions = [ComplexMeasurement.id == id]
            if hostName:
                conditions.append(Sensor.name ** str('%' + hostName + '%'))

            count = ComplexMeasurement.select() \
                .join(Measurement, on=ComplexMeasurement.measurement, join_type=JOIN_LEFT_OUTER) \
                .join(Sensor, on=Measurement.sensor, join_type=JOIN_LEFT_OUTER) \
                .where(*conditions) \
                .count()
            if count > 0:
                values = self.getComplexValuesById(request, id, True)
                return values

            return []

        normals = []
        complexs = {}
        for v in query:
            normals.append({"host_name": v.measurement.sensor.name,
                 "measurement_id": v.measurement.id,
                 "value": v.value,
                 "date": v.created})
            if not v.measurement.complexes or id:
                continue

            dict = complexs.setdefault(v.measurement.id, {"from": None,
                                                          "to": None,
                                                          "complex": v.measurement.complexes[0],
                                                          "host_name": v.measurement.sensor.name})

            if dict["from"] is None or dict["from"] > v.created:
                dict["from"] = v.created
            if dict["to"] is None or dict["to"] < v.created:
                dict["to"] = v.created
            complexs[v.measurement.id] = dict

        complexValues = []
        for c in complexs.values():
            values = self.calculateComplexValues(c["complex"], c["from"], c["to"])
            for v in values:
                v["host_name"] = c["host_name"]
                v["measurement_id"] = c["complex"].id
            complexValues += values

        if onlyComplex:
            return complexValues
        return normals + complexValues

    def getMeasurementValuesById(self, request, id):
        if self.measurementExistsById(id):
            return self.getNormalValuesById(request, id)
        elif self.complexExistsById(id):
            return self.getComplexValuesById(request, id)
        return []

    def getNormalValuesById(self, request, id):
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

        return [{"value": v.value,
                 "date": v.created} for v in query]

    def getSensors(self, request):
        hostName = request.args.get('name') or None
        count = request.args.get('count') or 50
        offset = request.args.get('offset') or 0

        query = Sensor.select()

        conditions = []
        if hostName:
            conditions.append(Sensor.name ** str('%' + hostName + '%'))

        try:
            if len(conditions):
                query = query.where(*conditions)
            query = query.limit(int(count)).offset(int(offset))
        except DoesNotExist:
            return []

        complexes = {m.id: [{"id": c.id,
                             "description": c.name} for c in m.complexes]
                     for s in query for m in s.measurements}

        measurements = {}
        for s in query:
            for m in s.measurements:
                measurements.setdefault(s.id, []).append({"id": m.id, "description": m.name})
                measurements[s.id] += complexes[m.id]

        return [{"id": s.id,
                 "name": s.name,
                 "measurements": measurements[s.id],
                 "metadata": [{"key": m.key,
                               "value": m.value}
                              for m in s.metadatas],
                 }
                for s in query]

    def createComplexMeasurement(self, data, userId):
        name = data['name']
        type = data['type']
        interval = data['interval']
        window = data['window']
        measurementId = data['measurement_id']

        if None in [name, type, interval, window, measurementId, userId]:
            raise MissingParameterException
        if not self.measurementExistsById(measurementId):
            raise MeasurementNotFoundException
        sId = Measurement.get(Measurement.id == measurementId).sensor.id
        count = ComplexMeasurement.select() \
            .join(Measurement, on=ComplexMeasurement.measurement, join_type=JOIN_LEFT_OUTER) \
            .join(Sensor, on=Measurement.sensor, join_type=JOIN_LEFT_OUTER) \
            .where(Sensor.id == sId,
                   ComplexMeasurement.name == name) \
            .count()
        if count is not 0:
            raise NameDuplicatedException

        c = ComplexMeasurement.create(name=name, type=type, interval=interval, window=window, measurement=measurementId,
                                  userid=userId)
        return {"measurement_id" : c.id}

    def deleteComplex(self, measurementId, userId):
        if self.complexBelongsToUser(measurementId, userId):
            ComplexMeasurement.delete().where(ComplexMeasurement.id == measurementId,
                                              ComplexMeasurement.userid == userId).execute()
            return True
        
    def getComplexMeasurements(self, request):
        names = request.args.get('names') or None
        count = request.args.get('count') or 50
        offset = request.args.get('offset') or 0

        query = ComplexMeasurement.select()

        conditions = []
        if names:
            conditions.append(ComplexMeasurement.name ** str('%' + names + '%'))

        try:
            if len(conditions):
                query = query.where(*conditions)
            query = query.limit(int(count)).offset(int(offset))
        except DoesNotExist:
            return []

        return [{"id": c.id,
                 "name": c.name,
                 "type": c.type,
                 "interval": c.interval,
                 "window": c.window,
                 "measurement_id": c.measurement.id,
                 "user_id": c.userid}
                for c in query]

    def getComplexValuesById(self, request, id, moreInfo= False):
        timeFrom = request.args.get('time_from') or None
        timeTo = request.args.get('time_to') or None
        count = request.args.get('count') or 50
        offset = request.args.get('offset') or 0

        c = ComplexMeasurement.get(ComplexMeasurement.id==id)
        mId = c.measurement.id

        query = MeasurementValue.select().join(Measurement, on=MeasurementValue.measurement, join_type=JOIN_LEFT_OUTER)
        conditions = [Measurement.id == mId]

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

        return self.calculateComplexValues(c, query[-1].created, query[0].created, moreInfo)

    def calculateComplexValues(self, complexMeasurement, fromDate, toDate, moreInfo= False):
        if fromDate == toDate:
            return []

        results = []
        while fromDate < toDate:
            start = fromDate - datetime.timedelta(minutes=complexMeasurement.window)
            res = {"value": complexMeasurement.calculateValue(start, fromDate),
                   "date": fromDate}
            if moreInfo:
                res["measurement_id"] = complexMeasurement.id
                res["host_name"] = complexMeasurement.measurement.sensor.name

            results.append(res)
            fromDate += datetime.timedelta(minutes=complexMeasurement.interval)

        return results

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

    def complexExistsByName(self, name):
        try:
            Measurement.get(Measurement.name == name)
            return True
        except DoesNotExist:
            return False

    def complexExistsById(self, id):
        try:
            ComplexMeasurement.get(ComplexMeasurement.id == id)
            return True
        except DoesNotExist:
            return False

    def measurementAssignedToSensor(self, measurementId, sensorId):
        try:
            Measurement.get(Measurement.id == measurementId, Measurement.sensor == sensorId)
            return True
        except DoesNotExist:
            return False

    def complexBelongsToUser(self, measurementId, userId):
        try:
            c = ComplexMeasurement.get(ComplexMeasurement.id == measurementId)
            if c.userid != userId:
                raise UserNotAllowedToDeleteException
            return True
        except DoesNotExist:
            try:
                Measurement.get(Measurement.id == measurementId)
                raise MeasurementIsNotComplexException
            except DoesNotExist:
                raise MeasurementNotFoundException


database = DatabaseModel()


def createTestData():
    for name in ["Laptop", "PC"]:
        s = Sensor.create(identifier=name, name=name)
        m1 = Measurement.create(name="CPU", description="Description", sensor=s)
        m2 = Measurement.create(name="GPU", description="Description", sensor=s)
        Metadata.create(key="Key1", value='Value1', sensor=s)
        Metadata.create(key="Key2", value='Value2', sensor=s)
        for m in [m1, m2]:
            for i in range(10):
                if m == m1:
                    MeasurementValue.create(value=i * 2.0, measurement=m,
                                            created= datetime.datetime.now() - datetime.timedelta(minutes=i+1))
                else:
                    MeasurementValue.create(value=i * 2.0, measurement=m,
                                            created=datetime.datetime.now() - datetime.timedelta(seconds=30*(i+1)))

    database.createComplexMeasurement({"name": "CPU-Complex", "type": "min", "interval": 5, "window": 30, "measurement_id": 1}, "test")
    database.createComplexMeasurement({"name": "GPU-Complex", "type": "avg", "interval": 5, "window": 30, "measurement_id": 2}, "test1")

# createTestData()
