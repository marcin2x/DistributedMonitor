monitors.factory('monitorsService', (Restangular, $uibModal, $rootScope) => {
   const headers = {
            Authorization: $rootScope.jwt
        },
        getMonitors = () => {
            return Restangular.one('monitors').getList(undefined, undefined, headers);
        },
        addModal = () => {
            return $uibModal.open({
                templateUrl: 'scripts/modules/monitors/views/add-modal.html',
                controller: 'addMonitorModalCtrl',
                size: 'md',
                backdrop: true
            }).result;
        },

        get = id => {
            return new Promise((resolve,reject) => {
                getMonitors().then(monitors => {
                    const monitor = monitors.find(m => m.id == id);
                    if(monitor) resolve(monitor.plain());
                    else reject('Cannot find monitor with id ' + id);
                });
            })
        },
        create = data => {
            return Restangular.all('monitors').post(data,undefined, headers);
        },
        remove = id => {
            return Restangular.one('monitors').remove({
                monitor_id: id
            }, headers);
        }

    return {
        getMonitors,
        get,
        addModal,
        create,
        remove
    };
});