monitors.controller('monitorInfoCtrl',  ($scope,$filter, $interval, $timeout, $state, $stateParams, monitorsService, measurementsService, hostRestangular) => {
    let interval = '';
    console.log('monitorCtrl');
    $scope.isAddComplexVisible = false;

    $scope.addComplexModal = () => {
        console.log("Open complex");
        measurementsService.addComplexModal().then( succ => {
            console.log("Opended");
        }, err => {
            console.log(err);
        })
        $scope.isAddComplexVisible = true;
        // document.getElementById("addComplex").style.height = "100%";
        // document.getElementById("menu").style.display = "none";
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
        console.log($scope.searchInput)
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


        $timeout(() => {


            measurementsService.getHosts().then(hosts => {
                $scope.hosts = hosts.plain();
            });

            measurementsService.values().then(res => {
                $scope.allValues = res.plain().map(item => {
                    item.description = getMeasurementName(item.host_name, item.measurement_id);
                    item.value =  item.value.toFixed(2);
                    return item;
                });

            })
        }, 0)

    }, err => {
        console.log(err);
        $state.go('base.dashboard');
    });






});