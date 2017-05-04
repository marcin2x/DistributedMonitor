auth.controller('addUserCtrl', ($scope, $state, authorizationService) => {
    $scope.form = {};

    $scope.addUser = (c = true) => {
    authorizationService.create($scope.form).then( res => {
            $state.go('login', {info: "New user registered"})
        }, err => {
            $scope.error = err.data.message;
        }
    )
    };
});