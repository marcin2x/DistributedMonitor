from src.authentication_service.rest import service, errors
from src.authentication_service.rest.errors import RestError
from src.authentication_service.data.db_provider import dbProvider
from flask import request
from src.authentication_service.utils.jwt import JwtManager
from flask import jsonify

jwtManager = JwtManager()

def getUserContext():
    jwt = request.headers['Authorization']
    return jwtManager.decodeToken(jwt)

@service.before_request
def before_request():
    if not request.path in ('/login', '/logout', '/register'):
        jwt = request.headers['Authorization']
        if jwt == None or not jwtManager.authenticate(jwt):
            raise errors.RestError(message='User not authenticated', status_code=401)

    dbProvider.connect()

@service.after_request
def after_request(response):
    dbProvider.close()
    return response

@service.errorhandler(RestError)
def handle_invalid_usage(error):
    dbProvider.close()
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

#@service.errorhandler(Exception)
#def all_exception_handler(error):
#   dbProvider.close()
#   return 'Internal Server Error', 500
