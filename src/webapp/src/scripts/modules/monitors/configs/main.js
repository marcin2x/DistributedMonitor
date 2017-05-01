monitors.config(function ($stateProvider) {

    $stateProvider
        .state('monitors', {
            url: '/monitors',
            abstract: true,
            parent: 'base',
            template: '<ui-view autoscroll="false"/>'
        })
        .state('monitors.info', {
            url: '/:monitorId',
            templateUrl: 'scripts/modules/monitors/views/monitor-info.html',
            controller: 'monitorInfoCtrl',
            // params: {
            //     port: undefined,
            //     address: undefined
            // }
        })
});