from flask import request, jsonify

from app import app


@app.route('/sensors', methods=['GET'])
def get_sensors():
    names = request.args.get('names')
    count = request.args.get('count')
    offset = request.args.get('offset')
    if count is None:
        count = 50
    if offset is None:
        offset = 0

    return jsonify(list())
