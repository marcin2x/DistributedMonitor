'use strict';

angular.element(document).ready(function () {
    angular.bootstrap(document, ['base']);
});
'use strict';

var base = angular.module('base', ['ui.router', 'ngAnimate', 'ngSanitize', 'restangular']);
'use strict';

base.config(function ($stateProvider, $urlRouterProvider, $locationProvider, $httpProvider) {
    $locationProvider.html5Mode({
        enabled: true
    });
    $stateProvider.state('base', {
        templateUrl: 'scripts/modules/base/views/base.html',
        controller: 'baseCtrl'
    }).state('base.dashboard', {
        url: '/dashboard',
        templateUrl: 'scripts/modules/base/views/dashboard.html'
    }).state('base.error', {
        url: '/error',
        templateUrl: 'scripts/modules/base/views/error.html'
    });
    $urlRouterProvider.otherwise('/dashboard');
    $httpProvider.interceptors.push('errorHandler');
}).run(function ($rootScope) {
    $rootScope.loaded = false;
    $rootScope.$on('$stateChangeSuccess', function () {
        if (!$rootScope.loaded) {
            (function () {
                $rootScope.loaded = true;
                var loader = document.getElementById('appLoader');
                setTimeout(function () {
                    document.body.removeChild(loader);
                }, 500);
            })();
        }
    });
});
"use strict";

base.config(function (RestangularProvider) {
    var ApiBaseUrl = '/api';
    RestangularProvider.setBaseUrl(ApiBaseUrl).setDefaultHeaders({ "Content-Type": "application/json" });
});
'use strict';

base.controller('baseCtrl', function () {
    console.log('baseController');
});
'use strict';

base.factory('errorHandler', function ($q, $injector) {
    function handle(rejection) {
        if (rejection.status === 403) {
            $injector.get('$state').go('');
        }
    }
    return {
        responseError: function responseError(rejection) {
            handle(rejection);
            return $q.reject(rejection);
        }
    };
});
//# sourceMappingURL=app.js.map
