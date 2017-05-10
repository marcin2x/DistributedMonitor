base.directive('navbar', function (authService) {
    return {
        restrict: 'E',
        templateUrl: 'scripts/modules/base/views/directives/navbar.html',
        link: function ($scope, $element, $attrs) {
            
        },
        controller: function ($scope, $state, $element, $timeout, $attrs) {
            $scope.logout = () => authService.logout();
        }
    };
});