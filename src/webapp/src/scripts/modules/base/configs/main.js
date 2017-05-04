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
}).run( ($rootScope, $state, $timeout) => {
    $rootScope.loaded = false;
    $rootScope.$on('$stateChangeSuccess', () => {
        if (!$rootScope.loaded) {
            $rootScope.loaded = true;
            const loader = document.getElementById('appLoader');
            setTimeout(()=>{
                document.body.removeChild(loader);
            },500)
        }
    });

    $rootScope.$on('$stateChangeStart', (event, toState, toParams, fromState, fromParams, options) => {
        if (!$rootScope.jwt &&
            ['/login', '/register'].indexOf(toState.url) < 0) {
            $timeout(function() {
                $state.go('login');
            });
        }
    })
});
