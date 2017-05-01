base.factory('monitorsService', (Restangular, $uibModal, $q) => {
    const  getMonitors = () => {
            return Restangular.one('monitors').getList();
        },
        addModal = () => {
            return $uibModal.open({
                templateUrl: 'scripts/modules/monitors/views/add-modal.html',
                controller: 'addMonitorModalCtrl',
                size: 'md',
                backdrop: true
            }).result;
        },
        get = (id) => {
            return new Promise((resolve,reject) => {
                getMonitors().then(monitors => {
                    const monitor = monitors.find(m => m.id == id);
                    if(monitor) resolve(monitor.plain());
                    else reject('Cannot find monitor with id ' + id);
                });
            })
        },
        createMonitor = data => {
            return Restangular.all('monitors').post(data);
        }

    return {
        getMonitors,
        get,
        addModal,
        createMonitor
    };


});