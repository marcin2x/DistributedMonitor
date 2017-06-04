monitors.controller('monitorInfoCtrl',  ($scope,$filter, $interval, $timeout, $state, $stateParams, monitorsService, measurementsService, hostRestangular) => {
    let interval = '';
    console.log('monitorCtrl');
    $scope.isAddComplexVisible = false;


    $scope.addComplexModal = () => {
        measurementsService.addComplexModal().then(succ => {
            measurementsService.getHosts().then(hosts => {
                $scope.hosts = hosts.plain();
                $scope.select($scope.hosts[0]);
            });
            measurementsService.getComplex().then(res => {
                $scope.allComplex = res.plain();
            });
        });
    }

    $scope.search = {
        host_name: '',
        description: ''
    }

    $scope.remove = id => {
        monitorsService.remove(id).then(succ => {
            $state.go('base.dashboard');
        }, err => {
            console.error(err);
        })
    }

    $scope.removeComplex = id => {
        measurementsService.removeComplex(id).then(succ => {
            measurementsService.getComplex().then(res => {
                $scope.allComplex = res.plain();
            });
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
                x: value.date,
                y: value.value.toFixed(2)
            }
        })];

        $scope.series = [$scope.hostName];
    }

    const setInterval = () => {
        if(interval) {
            $interval.cancel(interval)
        }
        interval = $interval(() => {
            measurementsService.valuesById($scope.measurementId).then(values => {
                dataToChart(values.plain());
            })
        }, 3000);

    }

    $scope.selectMeasurement = id => {
        console.log(id);
        $scope.measurementId = id;
        measurementsService.valuesById(id).then(values => {
            dataToChart(values.plain());
            setInterval();
        })
    }
    $scope.select = host => {
        $scope.hostName = host.name;
        $scope.selectMeasurement(host.measurements[0].id);
    };

    const getMeasurementName =(name, id) => {
        const host = $scope.hosts.find(host => host.name === name);
        const me = host.measurements.find(m => m.id === id);
        return me.description;

    };
    $scope.filter = () => {
        if($scope.searchInput[0] === '@'){
            $scope.search.host_name = $scope.searchInput.slice(1);
        }
        if($scope.searchInput[0] === '#'){
            $scope.search.description = $scope.searchInput.slice(1);
        }
    }


    monitorsService.get($stateParams.monitorId).then(monitor => {
        $scope.monitor = monitor;
        hostRestangular.init(monitor.address, monitor.port);

        measurementsService.getComplex().then(res => {
            $scope.allComplex = res.plain();
        });

        measurementsService.getHosts().then(hosts => {
            $scope.hosts = hosts.plain();
            measurementsService.values().then(res => {
                $scope.allValues = res.plain().map(item => {
                    item.description = getMeasurementName(item.host_name, item.measurement_id);
                    item.value =  item.value.toFixed(2);
                    return item;
                });

            })
        });


    }, err => {
        console.log(err);
        $state.go('base.dashboard');
    });

});