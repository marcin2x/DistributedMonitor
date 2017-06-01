monitors.factory('measurementsService', (Restangular, $uibModal, $rootScope) => {
    const headers = {
        Authorization: $rootScope.jwt
    };
    const query = () => ({
        order: "desc",
        address: $rootScope._address,
        port: $rootScope._port
    });
    const values = () => {
            return Restangular.one('measurements/values').customGET('', query());
        },
        valuesById = id => {
            return Restangular.one(`measurements/${id}/values`).customGET('', query());
        },
        valuesWithParams = params => {
            return Restangular.one('measurements/values').customGET('',Object.assign({},params, query()));
        },
        getHosts = () => {
            return Restangular.one('hosts').customGET('', query());
        },
        addComplexModal = () => {
            console.log("Add modal complex");
            return $uibModal.open({
                templateUrl: 'scripts/modules/monitors/views/add-complex-modal.html',
                controller: 'addComplexModalCtrl',
                size: 'md',
                backdrop: true
            }).result;
        },
        createComplex = data => {
            console.log(data)
            // return Restangular.all('measurements').post(data, undefined, headers);
        }

    ;


    return {
        values,
        valuesById,
        valuesWithParams,
        getHosts,
        addComplexModal,
        createComplex
    };
});