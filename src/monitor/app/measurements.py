from flask import request, jsonify

from app import app, errors
from src.monitor.db.model import database


@app.route('/measurements', methods=['POST', 'GET'])
def measurements():
    if request.method == 'GET':
        return jsonify(database.getComplexMeasurements(request))

    elif request.method == 'POST':
        data = request.get_json()

        if 'sensor_name' not in data or 'measurement_name' not in data or 'metadata' not in data:
            raise errors.RestError(message='Invalid request', status_code=400)
        elif False:  # TODO implement validation
            raise errors.RestError(message='Measurement already exists', status_code=409)

        return jsonify(sensor_id=-1, measurement_id=-1)


@app.route('/measurements/<int:measurement_id>', methods=['PUT', 'POST', 'DELETE'])
def update(measurement_id):
    data = request.get_json()

    if request.method == 'PUT':

        if 'sensor_id' not in data or 'metadata' not in data:
            raise errors.RestError(message='Invalid request', status_code=400)
        elif False:  # TODO implement validation (measurement or sensor doesnt exist)
            raise errors.RestError(message='Measurement or sensor doesn\'t exists', status_code=404)
        elif False:  # TODO implement validation (measurement doesn't belong to sensor)
            raise errors.RestError(message='Measurement doesn\'t belong to sensor', status_code=403)
        return app.response_class(status=200, mimetype='application/json')

    elif request.method == 'POST':
        if 'sensor_id' not in data or 'value' not in data or 'date' not in data:
            raise errors.RestError(message='Invalid request', status_code=400)
        elif False:  # TODO implement validation (measurement or sensor doesnt exist)
            raise errors.RestError(message='Measurement or sensor doesn\'t exist', status_code=404)
        return app.response_class(status=201, mimetype='application/json')

    elif request.method == 'DELETE':
        if 'jwt' not in data:
            raise errors.RestError(message='Invalid request', status_code=400)
        elif False:  # TODO implement validation (measurement doesnt exist)
            raise errors.RestError(message='Invalid token', status_code=401)
        elif False:  # TODO implement validation (measurement doesnt exist)
            raise errors.RestError(message='Measurement doesn\'t exist', status_code=404)
        elif False:  # TODO implement validation (measurement is not complex)
            raise errors.RestError(message='Measurement is not complex', status_code=409)
        return app.response_class(status=200, mimetype='application/json')


@app.route('/measurements/values', methods=['GET'])
def get_values():
    return jsonify(database.getMeasurementValues(request=request))


@app.route('/measurements/<int:measurement_id>/values', methods=['GET'])
def get_values_for_measurement_id(measurement_id):
    return jsonify(database.getMeasurementValuesById(request=request, id=measurement_id))


@app.route('/measurements/complex', methods=['POST'])
def create_complex():
    data = request.get_json()
    if 'measurements_id' not in data or 'jwt' not in data:
        raise errors.RestError(message='Invalid request', status_code=400)
    elif False:  # TODO implement validation (measurement doesnt exist)
        raise errors.RestError(message='Measurement doesn\'t exist', status_code=404)
    elif False:  # TODO implement validation (measurement doesnt exist)
        raise errors.RestError(message='Invalid token', status_code=401)

    return jsonify(measurement_id=-1)
