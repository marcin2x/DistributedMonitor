base.factory('errorHandler', ($q, $injector) => {
    function handle(rejection) {
        // if (rejection.status === 403) {
        //     $injector.get('$state').go('base.dashboard');
        // }
    }
    return {
        responseError: function (rejection) {
            handle(rejection);
            return $q.reject(rejection);
        }
    };


});