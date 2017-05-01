base.factory('authService', ($rootScope, Restangular) => {
    return {
        logout: () => {
            return Restangular.all('logout').post({}, undefined, {
                Authorization: 'jwt=' + $rootScope.jwt
            });
        }
    };


});