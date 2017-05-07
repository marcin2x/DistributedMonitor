import uuid
import psutil
import json
import time
import socket
import sys
import pickle
from functools import reduce
sys.path.append("../../")
print(sys.path)
from src.common.TCP_messages import *


BUFFER_SIZE = 1024
QUIET_MODE = False

def generate_id():
    return str(uuid.uuid4())

def prepare_metadata(metadata):
    fields={
            "CPU Core count": lambda: psutil.cpu_count(),
            "Total RAM": lambda: psutil.virtual_memory().total
            }
    result = []
    for key in metadata:
        if key in fields.keys():
            result.append({"key": key, "value": fields[key]()})
    return result

def prepare_register(data):
    name = socket.gethostname()
    measurements = [{"name": x } for x in data["measurements"]]
    result = SensorRegisterRequest(data["identifier"], name, measurements, prepare_metadata(data["metadata"]))
    return result

def prepare_data(response):
    fields={
            "CPU": lambda: reduce(lambda x, y : x+y ,[psutil.cpu_percent(interval=0.1) for indx in range(10)])/10,
            "RAM": lambda: psutil.virtual_memory().percent
            }
    data = []
    for measurement in response.measurements:
        if measurement["measurements_name"] in fields.keys():
            data.append({
                                "measurement_id": measurement["measurements_id"],
                                "measurement_value": fields[measurement["measurements_name"]]()})
            result = SensorDataRequest(response.sensor_id, data)
    return result

def register(config, conn):
    reg_data = prepare_register(config)
    if not QUIET_MODE:
        print ("Register: ", reg_data.get_message_body())
    s = socket.socket()
    s.connect(conn)
    s.sendall(serializer.serialize(reg_data))
    response =  bytes() 
    while True:
        chunk = s.recv(BUFFER_SIZE)
        response += chunk
        if len(chunk) < BUFFER_SIZE:
            break
    
    response = serializer.deserialize_response(response)
    return response


def run():
    with open('sensor_config.json') as data_file:
        config = json.load(data_file)
    
    if config["identifier"] == "":
        config["identifier"] = generate_id()
        with open("sensor_config.json","w") as con_file:
            json.dump(config, con_file,sort_keys=True, indent=4)
    

    conn_tuple = (config["host"], config["port"])
    reg_response = register(config,conn_tuple)
    rtime = time.time()

    while True:
        dtime = time.time()
        if config["register_interval"]> 0 and time.time() - rtime > config["register_interval"]:
            rtime = time.time()
            reg_response = register(config, conn_tuple)
            if not QUIET_MODE:
                print("Register response: ", reg_response.get_message_body())
        data = prepare_data(reg_response)
        s = socket.socket()
        s.connect(conn_tuple)
        s.sendall(serializer.serialize(data))
        data_response = bytes()
        while True:
            chunk = s.recv(BUFFER_SIZE)
            data_response += chunk
            if len(chunk) < BUFFER_SIZE:
                break
        data_response = serializer.deserialize_response(data_response)
        s.close()
        if not QUIET_MODE:
            print ("Data: ", data.get_message_body())
            print ("Data response :", data_response.get_message_body())
        
        interval = config["data_interval"] - time.time() + dtime
        if interval > 0 :
            time.sleep(interval)
        
