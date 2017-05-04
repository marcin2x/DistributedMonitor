auth.factory('authorizationService', (Restangular) => {
    const login = (data) => {
        return Restangular.all('login').post(data);
    },
    create = (data) => {
        return Restangular.all('register').post(data);
    }

    return {
        login,
        create
    }



});