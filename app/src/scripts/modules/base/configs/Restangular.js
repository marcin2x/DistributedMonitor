base.config( RestangularProvider => {
    const ApiBaseUrl = '/api';
    RestangularProvider
        .setBaseUrl(ApiBaseUrl)
        .setDefaultHeaders({"Content-Type": "application/json"})
});