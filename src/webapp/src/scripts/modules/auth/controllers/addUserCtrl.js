auth.controller('addUserCtrl', ($scope, $state, authService) => {
    $scope.form = {};

    $scope.addUser = (c = true) => {
        authService.create($scope.form).then( res => {
            $state.go('login', {info: "New user registered"})
        }, err => {
            $scope.error = err.data.message;
        }
    )
    };
});