monitors.factory('hostRestangular', ($rootScope, Restangular) => {

    const init = (address, port) => {
            $rootScope._address = address;
            $rootScope._port = port;
        };
        // rest = () =>  {
        //     return Restangular.withConfig( RestangularConfigurer => {
        //         console.log(_address)
        //         Restangular.setDefaultRequestParams(['remove', 'post', 'put', 'get'], {
        //             address: _address,
        //             port: _port
        //         });
        //         // RestangularConfigurer.setBaseUrl(url);
        //     });
        // }

    return {
        init
    };


});