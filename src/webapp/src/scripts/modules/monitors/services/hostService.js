monitors.factory('hostService', (Restangular, hostRestangular, $uibModal, $q) => {
    const  getHosts = () => {
        return hostRestangular.rest().one('hosts').getList();
    };

    return {
        getHosts
    };
});