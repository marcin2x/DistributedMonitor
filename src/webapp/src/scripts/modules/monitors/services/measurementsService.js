monitors.factory('measurementsService', (Restangular, hostRestangular) => {
    const values = () => {
            return hostRestangular.rest().one('measurements/values').getList();
        },
        valuesById = id => {
            return hostRestangular.rest().one(`measurements/${id}/values`).getList();
        },
        valuesWithParams = params => {
            return hostRestangular.rest().one('measurements/values').customGET('',params);
        };

    return {
        values,
        valuesById,
        valuesWithParams
    };
});