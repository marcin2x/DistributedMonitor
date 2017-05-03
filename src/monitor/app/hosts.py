from flask import request, jsonify

from app import app, errors
from src.monitor.db.model import database


@app.route('/hosts', methods=['GET'])
def hosts():
    return jsonify(database.getSensors(request))


