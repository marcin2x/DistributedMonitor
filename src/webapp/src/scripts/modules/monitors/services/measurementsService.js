monitors.factory('measurementsService', (Restangular, hostRestangular) => {
    const  values = () => {
        return hostRestangular.rest().one('measurements/values').getList();
    };

    return {
        values
    };
});