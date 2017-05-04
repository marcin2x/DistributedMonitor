auth.controller('addUserCtrl', ($scope, $state, registerService) => {
    $scope.form = {};

    $scope.addUser = (c = true) => {
        console.log($scope.form)
        registerService.create($scope.form).then( res => {
            console.log("Everything is ok")
            $state.go('login', {info: "New user registered"})
        }, err => {
            $scope.error = err.data.message;
    }
)
        console.log("Dupa");


    };
});