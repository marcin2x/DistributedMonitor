monitors.factory('hostRestangular', Restangular => {
    let url = '';
    const init = (address, port) => {
            url = 'http://'+ address + ':' + port;
        },
        rest = () =>  {
            return Restangular.withConfig( RestangularConfigurer => {
                RestangularConfigurer.setBaseUrl(url);
            });
        }

    return {
        rest,
        init
    };


});