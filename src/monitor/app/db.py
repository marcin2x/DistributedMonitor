from app import app
from src.monitor.db.model import *

@app.before_request
def _db_connect():
    database.connect()

@app.teardown_request
def _db_close(exc):
    database.close()
