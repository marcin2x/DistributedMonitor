auth.factory('registerService', ($rootScope, Restangular) => {

    return {
        create: (data) => {
        return Restangular.all('register').post(data, undefined, {

        });
}
};


});