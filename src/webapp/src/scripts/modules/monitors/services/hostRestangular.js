monitors.factory('hostRestangular', Restangular => {
    let url = '';
    let _address = '';
    let _port = '';

    const init = (address, port) => {
            // url = 'http://'+ address + ':' + port;
            _address = address;
            _port = port;
            rest();
        },
        rest = () =>  {
            return Restangular.withConfig( RestangularConfigurer => {
                console.log(_address)
                Restangular.setDefaultRequestParams(['remove', 'post', 'put', 'get'], {
                    address: _address,
                    port: _port
                });
                // RestangularConfigurer.setBaseUrl(url);
            });
        }

    return {
        rest,
        init
    };


});