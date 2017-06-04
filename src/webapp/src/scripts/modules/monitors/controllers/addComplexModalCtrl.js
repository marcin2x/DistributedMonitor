monitors.controller('addComplexModalCtrl', ($scope, $uibModalInstance, monitorsService, measurementsService) => {
    $scope.form = {};

    measurementsService.getHosts().then(hosts => {
        $scope.hosts = hosts.plain();

    });

    $scope.types = ['MIN', 'MAX', 'AVG'].map(type => ({name: type, value: type.toLowerCase()}));

    $scope.getMeasurements = () => {
        const host = $scope.hosts.find(host => host.name === $scope.host_name);
        $scope.measurements = host.measurements;
    }

    $scope.addComplex = () => {
        measurementsService.createComplex($scope.form).then(res => {
            $scope.ok(res.plain());
        }, err => {
            $scope.error = err.data;
        });
    };

    $scope.ok = function (o) {
        $uibModalInstance.close(o);
    };

    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
});