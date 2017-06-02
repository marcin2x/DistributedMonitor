monitors.controller('monitorInfoCtrl',  ($scope,$filter, $interval, $timeout, $state, $stateParams, $q, monitorsService, measurementsService, hostRestangular) => {
    const DEFAULT_REFRESH_INTERVAL_IN_SECONDS = 10;

    let interval = '';
    let selectedMeasurements = [];

    $scope.refreshEnabled = true;
    $scope.refreshInterval = DEFAULT_REFRESH_INTERVAL_IN_SECONDS;

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

    const prepareDataForChart = values => {
        const sortedValues = values.sort((a, b) => new Date(a.date) - new Date(b.date));

        return sortedValues.map(value => {
            return {
                x: moment(value.date),
                y: value.value
            };
        });
    };

    $scope.setInterval = () => {
        if(interval) {
            $interval.cancel(interval)
        }

        if (!$scope.refreshEnabled || !$scope.refreshInterval || !selectedMeasurements.length) {
            return;
        }

        interval = $interval(renderChart, $scope.refreshInterval * 1000);
    };

    const renderChart = () => {
        if (!selectedMeasurements.length) {
            $scope.data = null;
            $scope.series = null;

            $scope.$apply();
            return;
        }

        let series = [];

        let promises = selectedMeasurements.map(measurement => {
            series.push(`${measurement.hostName} [${measurement.description}]`);

            return measurementsService
                .valuesById(measurement.id)
                .then(values => prepareDataForChart(values.plain()))
        });

        $q.all(promises).then(values => {
            $scope.series = series;
            $scope.data = values;
        });
    };

    $scope.selectMeasurements = measurements => {
        selectedMeasurements = selectedMeasurements.concat(measurements);

        renderChart();
        $scope.setInterval();
    };

    $scope.deselectMeasurements = measurements => {
        const deselectedIds = measurements.map(measurement => measurement.id);
        selectedMeasurements = selectedMeasurements.filter(element => deselectedIds.indexOf(element.id) < 0);

        renderChart();
        $scope.setInterval();
    };

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