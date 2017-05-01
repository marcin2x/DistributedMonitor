import pickle

from .exceptions import *
from .sensor_data_request import SensorDataRequest
from .sensor_data_response import SensorDataResponse
from .sensor_register_request import SensorRegisterRequest
from .sensor_register_response import SensorRegisterResponse


def serialize(message):
    return pickle.dumps(message.to_dict())


def deserialize_request(message):
    data = pickle.loads(message)
    type = data["type"]
    body = data["body"]

    if type == "register":
        return SensorRegisterRequest(**body)
    elif type == "data":
        return SensorDataRequest(**body)
    else:
        raise InvalidSensorMessageTypeException(type)


def deserialize_response(message):
    data = pickle.loads(message)
    type = data["type"]
    body = data["body"]

    if type == "register":
        return SensorRegisterResponse(**body)
    elif type == "data":
        return SensorDataResponse(body)
    else:
        raise InvalidSensorMessageTypeException(type)
