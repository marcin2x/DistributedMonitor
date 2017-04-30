from flask import request, jsonify
from src.authentication_service.rest import service, errors
from src.authentication_service.data.repositories import MonitorRepository, UserRepository
from src.authentication_service.rest.config import getUserContext

userRepository = UserRepository()
monitorRepository = MonitorRepository()

@service.route('/monitors', methods=['GET'])
def getMonitors():
    data = request.get_json()

    #todo: handle paging count + offset from api
    user = userRepository.findById(getUserContext()['id'])
    monitors = monitorRepository.findAllForUser(user)
    return jsonify(monitors)


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
    data = request.get_json()

    if 'monitor_id' not in data:
        raise errors.RestError(message='Invalid request', status_code=400)
    monitor = monitorRepository.find(data['monitor_id'])
    if monitor == None:
        raise errors.RestError(message='Monitor with provided id does not exist', status_code=400)

    monitorRepository.delete(monitor)

    return service.response_class(
        status=200,
        mimetype='application/json'
    )