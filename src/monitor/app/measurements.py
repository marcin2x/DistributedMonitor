from app import app, errors
from flask import request, jsonify

from src.authentication_service.utils.jwt import JwtManager
from src.monitor.db.exceptions import MissingParameterException, MeasurementNotFoundException, NameDuplicatedException, \
    UserNotAllowedToDeleteException, MeasurementIsNotComplexException
from src.monitor.db.model import database


jwtManager = JwtManager()


@app.route('/measurements', methods=['POST', 'GET'])
def measurements():
    if request.method == 'GET':
        return jsonify(database.getComplexMeasurements(request))

    elif request.method == 'POST':
        token = request.headers.get('Authorization')

        if not jwtManager.authenticate(token):
            raise errors.RestError(message='Invalid token', status_code=401)
        try:
            return jsonify(
                database.createComplexMeasurement(data=request.get_json(), userId=jwtManager.decodeToken(token)['id']))
        except MissingParameterException:
                raise errors.RestError(message='Invalid request', status_code=400)
        except MeasurementNotFoundException:
            raise errors.RestError(message='Measurement already exists', status_code=404)
        except NameDuplicatedException:
            raise errors.RestError(message='Measurement already exists', status_code=409)


@app.route('/measurements/<int:measurement_id>', methods=['DELETE'])
def delete_complex(measurement_id):
    token = request.headers.get('Authorization')

    if not jwtManager.authenticate(token):
        raise errors.RestError(message='Invalid token', status_code=401)
    try:
        if database.deleteComplex(measurement_id, jwtManager.decodeToken(token)['id']):
            return app.response_class(status=200, mimetype='application/json')
    except MeasurementNotFoundException:
        raise errors.RestError(message='Measurement does not exists', status_code=404)
    except UserNotAllowedToDeleteException:
        raise errors.RestError(message='Not allowed', status_code=403)
    except MeasurementIsNotComplexException:
        raise errors.RestError(message='Measurement is not complex', status_code=409)


@app.route('/measurements/values', methods=['GET'])
def get_values():
    return jsonify(database.getMeasurementValues(request=request))


@app.route('/measurements/<int:measurement_id>/values', methods=['GET'])
def get_values_for_measurement_id(measurement_id):
    return jsonify(database.getMeasurementValuesById(request=request, id=measurement_id))


