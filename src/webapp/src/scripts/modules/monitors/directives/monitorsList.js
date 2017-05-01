monitors.directive('monitorsList', function () {
    return {
        restrict: 'E',
        templateUrl: 'scripts/modules/monitors/views/directives/monitors-list.html',
        link: function ($scope, $element, $attrs) {
            
        },
        controller: function ($scope, monitorsService) {

            const getMonitors = () => {
                monitorsService.getMonitors().then(monitors => {
                    $scope.monitors = monitors.plain();
                }, err => {
                    console.log(err);
                });
            };

            getMonitors();

            $scope.addModal = () => {
                monitorsService.addModal().then( result => {
                    getMonitors();
                });
            }
        }
    };
});