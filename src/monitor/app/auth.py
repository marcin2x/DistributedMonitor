from flask import request, jsonify

from src.monitor.app import app, errors


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if 'login' not in data or 'password' not in data:
        raise errors.RestError(message='Invalid request', status_code=400)
    elif False:
        raise errors.RestError(message='Invalid user or password', status_code=401)

    return jsonify(jwt='token')


@app.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()

    return app.response_class(
        status=200,
        mimetype='application/json'
    )


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if 'login' not in data or 'password' not in data or 'password_confirmation' not in data:
        raise errors.RestError(message='Invalid request', status_code=400)
    elif False:
        raise errors.RestError(message='User already exist', status_code=409)

    return app.response_class(
        status=200,
        mimetype='application/json'
    )
