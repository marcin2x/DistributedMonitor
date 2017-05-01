from flask import request, jsonify
from playhouse.shortcuts import model_to_dict, dict_to_model
from src.authentication_service.rest import service, errors
from src.authentication_service.data.repositories import MonitorRepository, UserRepository
from src.authentication_service.rest.config import getUserContext


userRepository = UserRepository()
monitorRepository = MonitorRepository()

@service.route('/monitors', methods=['GET'])
def getMonitors():

    #todo: handle paging count + offset from api
    user = userRepository.findById(getUserContext()['id'])
    monitors = monitorRepository.findAllForUser(user)

    result = []
    for monitor in monitors:
        result.append({
          'id' : monitor.id,
          'user_id' : monitor.user.id,
          'name' : monitor.name,
          'address' : monitor.address,
          'port' : monitor.port
        })

    return jsonify(result)


@service.route('/monitors', methods=['POST'])
def addMonitor():
   data = request.get_json()

   if 'name' not in data or 'port' not in data or 'address' not in data:
       raise errors.RestError(message='Invalid request', status_code=400)
   elif not monitorRepository.isUnique(data['name']):
       raise errors.RestError(message='Monitor already exists', status_code=409)

   user = userRepository.findById(getUserContext()['id'])
   monitor = monitorRepository.save(data['name'], data['port'], data['address'], user)

   return jsonify(monitor.get_id())

#todo: permissions?
@service.route('/monitors', methods=['DELETE'])
def deleteMonitor():

    if 'monitor_id' not in request.args:
        raise errors.RestError(message='Invalid request', status_code=400)
    monitor_id = request.args.get('monitor_id')
    monitor = monitorRepository.find(monitor_id)
    if monitor == None:
        raise errors.RestError(message='Monitor with provided id does not exist', status_code=400)

    monitorRepository.delete(monitor)

    return service.response_class(
        status=200,
        mimetype='application/json'
    )