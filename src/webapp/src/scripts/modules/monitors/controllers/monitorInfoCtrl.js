monitors.controller('monitorInfoCtrl',  ($scope,$filter, $interval, $timeout, $state, $stateParams, monitorsService, measurementsService, hostRestangular) => {

    $scope.remove = id => {
        monitorsService.remove(id).then(succ => {
            $state.go('base.dashboard');
        }, err => {
            console.error(err);
        })
    }

    $scope.options = {
        scales: {
            xAxes: [{
                type: 'time',
                position: 'bottom'
            }]
        }
    }

    const dataToChart = values => {
        $scope.values = values.sort( (a,b) => new Date(a.date) - new Date(b.date));
        $scope.data = [$scope.values.map(value => {
            return {
                x: moment(value.date).valueOf(),
                y: value.value
            }
        })];

        $scope.series = [$scope.hostName];
    }

    $scope.selectMeasurement = id => {
        $scope.measurementId = id;
        measurementsService.valuesById(id).then(values => {
            dataToChart(values.plain());
        })
    }
    $scope.select = host => {
        $scope.hostName = host.name;
        $scope.selectMeasurement(host.measurements[0].id);
    };

    $interval(() => {
        measurementsService.valuesById(id).then(values => {
            dataToChart(values.plain());
        })
    }, 3000);



    monitorsService.get($stateParams.monitorId).then(monitor => {
        $scope.monitor = monitor;
        hostRestangular.init(monitor.address, monitor.port);


        $timeout(() => {


            measurementsService.getHosts().then(hosts => {
                $scope.hosts = hosts.plain();
            });

            measurementsService.values().then(res => {
                $scope.allValues = res.plain();
            })
        }, 0)

    }, err => {
        console.log(err);
        $state.go('base.dashboard');
    });



});