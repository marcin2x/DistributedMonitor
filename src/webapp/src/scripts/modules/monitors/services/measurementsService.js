monitors.factory('measurementsService', (Restangular, hostRestangular) => {
    const values = () => {
            return hostRestangular.rest().one('measurements/values').getList();
        },
        valuesWithParams = params => {
            return hostRestangular.rest().one('measurements/values').customGET('',params);
        };

    return {
        values,
        valuesWithParams
    };
});