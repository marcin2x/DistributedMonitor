monitors.controller('monitorInfoCtrl',  ($scope, $state, $stateParams, monitorsService) => {

    monitorsService.get($stateParams.monitorId).then(monitor => {
        console.log(monitor)
    }, err => {
        console.error(err);
        $state.go('base.dashboard');
    });


});