const express = require('express'),
    httpProxy = require('http-proxy'),
    proxy = httpProxy.createProxyServer(),
    app = express();

app.use(express.static('./src'));



app.use('/api', function (req, res, next) {
    const r = `${req.method} ${req.url}`;
    const authReq = [
        'POST /login',
        'POST /register',
        'POST /logout',
        'GET /monitors',
        'POST /monitors',
        'DELETE /monitors/*',
    ]
    if(authReq.indexOf(r) > -1) {
        proxy.web(req, res, {
            target: {
                host: '52.174.179.132',
                port: '8081'
            }
        });
    }else if(req.query.address && req.query.port){
        proxy.web(req, res, {
            target: {
                host: req.query.address,
                port: req.query.port
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