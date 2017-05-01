base.config(($stateProvider, $urlRouterProvider, $locationProvider, $httpProvider) => {
    $locationProvider.html5Mode({
        enabled: true
    });
    $stateProvider
        .state('base', {
            templateUrl: 'scripts/modules/base/views/base.html',
            controller: 'baseCtrl'
        })
        .state('base.dashboard', {
            url: '/dashboard',
            templateUrl: 'scripts/modules/base/views/dashboard.html'
        })
        .state('base.error', {
            url: '/error',
            templateUrl: 'scripts/modules/base/views/error.html'
        });
    $urlRouterProvider.otherwise('/dashboard');
    $httpProvider.interceptors.push('errorHandler');
}).run( $rootScope => {
    $rootScope.jwt = '11111111111111';
    $rootScope.loaded = false;
    $rootScope.$on('$stateChangeSuccess', function () {
        if (!$rootScope.loaded) {
            $rootScope.loaded = true;
            const loader = document.getElementById('appLoader');
            setTimeout(()=>{
                document.body.removeChild(loader);
            },500)
        }
    });
});
