import uuid
import psutil
import json
import time
import socket

BUFFER_SIZE = 1024
QUIET_MODE = False

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

def prepare_register(data, sensor_id = ""):
    identifier = str(uuid.uuid4()) if sensor_id == "" else sensor_id
    measurements = [{"name": x } for x in data["measurements"]]
    result = {"type":"register",
            "body": {
                "identifier": identifier,
                "name": "some PC name", # TODO Menage to generate name
                "measurements": measurements,
                "metadata": prepare_metadata(data["metadata"])
                }}
    return result

def prepare_data(response):
    fields={
            "CPU": lambda: reduce(lambda x, y : x+y ,[psutil.cpu_percent(interval=0.1) for indx in range(10)])/10,
            "RAM": lambda: psutil.virtual_memory().percent
            }
    result = {"type": "data", "body": {"sensor_id": response["body"]["sensor_id"], "values": []}}
    for measurement in response["body"]["measurements"]:
        if measurement["measurement_name"] in fields.keys():
            result["body"]["values"].append({
                                "measurement_id": measurement["measurement_id"],
                                "measurement_value": fields[measurement["measurement_name"]]()})
    return result

def register(config, conn, sensor_id=""):
    reg_data = prepare_register(config)
    if not QUIET_MODE:
        print ("Register: ", reg_data)
    s = socket.socket()
    s.connect(conn)
    s.sendall(json.dumps(reg_data))
    response =  "" 
    while True:
        chunk = s.recv(BUFFER_SIZE)
        response += chunk
        if len(chunk) < BUFFER_SIZE:
            break
    
    response = json.loads(response)
    # WORKAROUND -if server doesn't response with what we need-
    # response = {"type": "register",
    #    "body":{ "sensor_id": 666,
    #        "measurements": 
    #        [
    #            {
    #                "measurement_name": "CPU",
    #                "measurement_id": 1
    #            },
    #            {
    #                "measurement_name": "RAM",
    #                "measurement_id": 2
    #            }
    #        ]
    #        }
    #    }   

    return response

with open('sensor_config.json') as data_file:
    config = json.load(data_file)

conn_tuple = (config["host"], config["port"])
response = register(config,conn_tuple)
rtime = time.time()
 

while True:
    dtime = time.time()
    if time.time() - rtime > config["register_interval"]:
        rtime = time.time()
        response = register(config, conn_tuple, response["body"]["sensor_id"])
        if not QUIET_MODE:
            print("Monitor response: ", response)
    data = prepare_data(response)
    s = socket.socket()
    s.connect(conn_tuple)
    s.sendall(json.dumps(data))
    s.close()
    if not QUIET_MODE:
        print ("Data: ", data)
    
    interval = config["data_interval"] - time.time() + dtime
    if interval > 0 :
        time.sleep(interval)

