const express = require('express'),
    httpProxy = require('http-proxy'),
    proxy = httpProxy.createProxyServer(),
    app = express();

app.use(express.static('./src'));



app.use('/api', function (req, res, next) {
    // res.setHeader('Last-Modified', (new Date()).toUTCString());
    console.log(req.url);
    if(req.url === '/login' || req.url === '/register'){
        proxy.web(req, res, {
            target: {
                host: '52.174.179.132',
                port: '8081'
            }
        });
    }else{
        proxy.web(req, res, {
            target: {
                host: '127.0.0.1',
                port: '3333'
            }
        });
    }
});

app.use('/', (req, res) => {
    res.sendfile('./src/index.html');
});

app.listen(8080);
console.log("App listening on port 8080");