auth.factory('loginService', ($rootScope, Restangular) => {

    return {
        login: (data) => {
        return Restangular.all('login').post(data, undefined, {

        });
}
};


});