auth.controller('loginUserCtrl', ($rootScope, $scope, $state, authService) => {
    $scope.info = $state.params.info;
    $scope.form = {};

    $scope.loginUser = () => {
        authService.login($scope.form).then( res => {
            $rootScope.jwt = res.jwt;
            $state.go('base.dashboard')
        }, err => {
            $scope.error = err.data.message;
        }
        )
    };
});