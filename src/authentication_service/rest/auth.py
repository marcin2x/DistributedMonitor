from flask import request, jsonify
from src.authentication_service.rest import service, errors
from src.authentication_service.data.repositories import UserRepository
from src.authentication_service.utils.hashing import PasswordHasher
from src.authentication_service.utils.jwt import JwtManager
from werkzeug.security import generate_password_hash, check_password_hash

userRepository = UserRepository()
hasher = PasswordHasher()
jwtManager = JwtManager()

@service.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if 'login' not in data or 'password' not in data:
        raise errors.RestError(message='Invalid request', status_code=400)

    user = userRepository.findByLogin(data['login'])
    if user == None or not check_password_hash(user.password, data['password']):
        raise errors.RestError(message='Invalid user or password', status_code=401)

    jwt = jwtManager.generate(user)
    return jsonify(jwt=jwt.decode('utf-8'))

@service.route('/logout', methods=['POST'])
def logout():
   return service.response_class(
        status=200,
        mimetype='application/json'
    )

@service.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if 'login' not in data or 'password' not in data or 'password_confirmation' not in data:
        raise errors.RestError(message='Invalid request', status_code=400)
    elif not userRepository.isUnique(data['login']):
        raise errors.RestError(message='User already exists', status_code=409)

    userRepository.save(data['login'], generate_password_hash(data['password']))

    return service.response_class(
        status=200,
        mimetype='application/json'
    )