monitors.factory('measurementsService', (Restangular, $rootScope) => {
    const query = () => ({
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
        valuesByIdWithParams = (id, params) => {
            return Restangular.one(`measurements/${id}/values`).customGET('', Object.assign({}, params, query()));
        },
        getHosts = () => {
            return Restangular.one('hosts').customGET('', query());
        };


    return {
        values,
        valuesById,
        valuesWithParams,
        valuesByIdWithParams,
        getHosts
    };
});