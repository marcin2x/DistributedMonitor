monitors.controller('addMonitorModalCtrl', ($scope, $uibModalInstance, monitorsService) => {
    $scope.form = {};

    $scope.addMonitor = (c = true) => {
        if(c) delete $scope.form.additionalProperty;
        monitorsService.create($scope.form).then(res => {
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