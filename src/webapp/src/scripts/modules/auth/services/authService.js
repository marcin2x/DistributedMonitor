auth.factory('authService', (Restangular, $rootScope, $state) => {
    const login = data => Restangular.all('login').post(data),
        create = data => Restangular.all('register').post(data),
        logout = () => Restangular.all('logout').post({}, undefined, {
            Authorization: 'jwt=' + $rootScope.jwt
        }).then(res => {
            $state.go('login');
        });

    return {
        login,
        create,
        logout
    }
});