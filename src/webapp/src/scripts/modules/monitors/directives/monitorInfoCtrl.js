monitors.controller('monitorInfoCtrl',  ($scope,$filter, $state, $stateParams, monitorsService, hostService, measurementsService, hostRestangular) => {
    
    $scope.remove = id => {
        monitorsService.remove(id).then(succ => {
            $state.go('base.dashboard');
        }, err => {
            console.error(err);
        })
    }

    $scope.select = host_name => {
        $scope.hostName = host_name;
        measurementsService.valuesWithParams({
            host_name
        }).then(values => {
            $scope.values = values.plain().sort( (a,b) => new Date(a.date) - new Date(b.date));
            $scope.labels = $scope.values.map(value => $filter('timeago')(value.date));
            $scope.data = [$scope.values.map(value => value.value)];

            $scope.series = [$scope.hostName];
        });
    }

    monitorsService.get($stateParams.monitorId).then(monitor => {
        $scope.monitor = monitor;
        hostRestangular.init(monitor.address, monitor.port);

        hostService.getHosts().then(hosts => {
            $scope.hosts = hosts.plain();
        })


    }, err => {
        console.log(err);
        $state.go('base.dashboard');
    });



});