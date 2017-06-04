monitors.controller('monitorInfoCtrl',  ($scope,$filter, $interval, $timeout, $state, $stateParams, $q, monitorsService, measurementsService, hostRestangular) => {
    const DEFAULT_REFRESH_INTERVAL_IN_SECONDS = 10;

    $scope.isAddComplexVisible = false;
    $scope.refreshEnabled = true;
    $scope.refreshInterval = DEFAULT_REFRESH_INTERVAL_IN_SECONDS;

    let interval = '',
        selectedMeasurements = [];


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
        $scope.complexError = null;
        measurementsService.removeComplex(id).then(succ => {
            measurementsService.getComplex().then(res => {
                $scope.allComplex = res.plain();
            });
        }, err => {
            $scope.complexError = err.data;
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
                y: value.value.toFixed(2)
            };
        });
    };

    $scope.setInterval = () => {
        if(interval) {
            $interval.cancel(interval)
        }

        if ($scope.archival || !$scope.refreshEnabled || !$scope.refreshInterval || !selectedMeasurements.length) {
            return;
        }

        interval = $interval(renderChart, $scope.refreshInterval * 1000);
    };

    const renderChart = () => {
        if (!selectedMeasurements.length) {
            $scope.data = null;
            $scope.series = null;

            return $scope.$apply();
        }

        let series = [];

        let promises = selectedMeasurements.map(measurement => {
            series.push(`${measurement.hostName} [${measurement.description}]`);

            if ($scope.archival) {
                return measurementsService
                    .valuesByIdWithParams(measurement.id, {
                        time_from: $scope.timeFrom,
                        time_to: $scope.timeTo
                    }).then(values => prepareDataForChart(values.plain()));
            }

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

    $scope.getDataForExport = data => {
        return Object.keys(data[0]).map(index => {
            return [data[0][index].x.format()].concat(data.map(dataset => dataset[index].y));
        });
    };

    $scope.getSeriesForExport = series => {
        return ['time'].concat(series);
    };

    $scope.resetTimeFilter = () => {
        $scope.timeFrom = null;
        $scope.timeTo = null;

        $scope.archival = false;

        renderChart();
    };

    $scope.plotArchivalMeasurements = () => {
        if ($scope.timeFrom && $scope.timeTo) {
            $scope.refreshEnabled = false;
            $scope.archival = true;
            $scope.setInterval();

            return renderChart();
        }

        if (!$scope.timeFrom && !$scope.timeTo) {
            $scope.archival = false;
            return renderChart();
        }
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