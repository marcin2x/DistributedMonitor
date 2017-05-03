monitors.controller('monitorInfoCtrl',  ($scope, $state, $stateParams, monitorsService, hostService, measurementsService, hostRestangular) => {
    
    $scope.remove = id => {
        monitorsService.remove(id).then(succ => {
            $state.go('base.dashboard');
        }, err => {
            console.error(err);
        })
    }
    
    monitorsService.get($stateParams.monitorId).then(monitor => {
        $scope.monitor = monitor;
        hostRestangular.init(monitor.address, monitor.port);

        hostService.getHosts().then(hosts => {
            $scope.hosts = hosts.plain();
        })

        measurementsService.values().then(values => {
            $scope.values = values.plain();
        })
    }, err => {
        console.log(err);
        $state.go('base.dashboard');
    });




});