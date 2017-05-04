auth.controller('loginUserCtrl', ($scope, $state, loginService) => {
    $scope.info = $state.params.info;
    $scope.form = {};

    $scope.loginUser = (c = true) => {
        console.log($scope.form)
        loginService.login($scope.form).then( res => {
            console.log("Everything is ok")

            $state.go('base.dashboard')
        }, err => {
            $scope.error = err.data.message;
        }
        )
    };
});