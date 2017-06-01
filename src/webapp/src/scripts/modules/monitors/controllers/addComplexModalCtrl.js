monitors.controller('addComplexModalCtrl', ($scope, $uibModalInstance, monitorsService, measurementsService) => {
    $scope.form = {};

    measurementsService.getHosts().then(hosts => {
        $scope.hosts = hosts.plain();
    });

    $scope.getMeasurements = () => {
        console.log($scope.form.host_name);
        const host = $scope.hosts.find(host => host.name ===  $scope.form.host_name.trim());
        $scope.measurements = host.measurements;
    }

    $scope.addComplex = (c = true) => {
        console.log("Add complex");
        if(c) delete $scope.form.additionalProperty;
        measurementsService.createComplex($scope.form).then(res => {
            $scope.ok(res.plain());
        }, err => {
            $scope.error = err.data.message;
        });
    };
    
    $scope.simulateError = () => {
        $scope.form.additionalProperty = 'test';
        $scope.addMonitor(false);
    }

    $scope.ok = function (o) {
        $uibModalInstance.close(o);
    };

    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
});