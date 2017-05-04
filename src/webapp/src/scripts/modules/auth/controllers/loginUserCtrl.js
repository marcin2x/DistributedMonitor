auth.controller('loginUserCtrl', ($rootScope, $scope, $state, authorizationService) => {
    $scope.info = $state.params.info;
    $scope.form = {};

    $scope.loginUser = () => {
    authorizationService.login($scope.form).then( res => {
            $rootScope.jwt = res.jwt;
            $state.go('base.dashboard')
        }, err => {
            $scope.error = err.data.message;
        }
        )
    };
});