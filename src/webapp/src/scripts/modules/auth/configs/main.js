auth.config(function ($stateProvider) {

    $stateProvider
        .state('login', {
            url: '/login',
            controller: 'loginUserCtrl',
            templateUrl: 'scripts/modules/auth/views/login.html',
            params: {
                info: null
            },
        })
        .state('register', {
            url: '/register',
            controller: 'addUserCtrl',
            templateUrl: 'scripts/modules/auth/views/register.html',
        })

});