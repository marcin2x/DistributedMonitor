from flask import Flask
service = Flask(__name__)
from src.authentication_service.rest import config, auth, monitors, errors