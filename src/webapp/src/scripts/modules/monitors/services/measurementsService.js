monitors.factory('measurementsService', (Restangular, $uibModal, $rootScope) => {
    const headers = {
        Authorization: $rootScope.jwt
    };
    const query = () => ({
        address: $rootScope._address,
        port: $rootScope._port
    }),
        values = () => {
            return Restangular.one('measurements/values').customGET('', query());
        },
        valuesById = id => {
            return Restangular.one(`measurements/${id}/values`).customGET('', query());
        },
        valuesWithParams = params => {
            return Restangular.one('measurements/values').customGET('',Object.assign({},params, query()));
        },
        valuesByIdWithParams = (id, params) => {
            return Restangular.one(`measurements/${id}/values`).customGET('', Object.assign({}, params, query()));
        },
        getHosts = () => {
            return Restangular.one('hosts').customGET('', query());
        },
        addComplexModal = () => {
            return $uibModal.open({
                templateUrl: 'scripts/modules/monitors/views/add-complex-modal.html',
                controller: 'addComplexModalCtrl',
                size: 'md',
                backdrop: true
            }).result;
        },
        getComplex = () => {
            return Restangular.all('measurements').customGET('', query());
        },
        createComplex = data => {
            return Restangular.all('measurements').customPOST(data, undefined , query(), headers);
        },
        removeComplex = id => {
            return Restangular.one('measurements',id).remove(query(), headers);
        };


    return {
        values,
        valuesById,
        valuesWithParams,
        valuesByIdWithParams,
        getHosts,
        addComplexModal,
        createComplex,
        getComplex,
        removeComplex
    };
});