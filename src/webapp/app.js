const express = require('express'),
    httpProxy = require('http-proxy'),
    proxy = httpProxy.createProxyServer(),
    app = express(),
    parseUrl = require('parseurl');

app.use(express.static('./src'));


proxy.on('error', function (err, reqq, ress) {
    ress.writeHead(500, {
        'Content-Type': 'text/plain'
    });
    ress.end('Something went wrong. And we are reporting a custom error message.');
});

app.use('/api', function (req, res, next) {


    const parsed = parseUrl(req);
    const r = `${req.method} ${parsed.pathname}`;
    const authReq = [
        'POST /login',
        'POST /register',
        'POST /logout',
        'GET /monitors',
        'POST /monitors',
        'DELETE /monitors',
    ];
    if(authReq.indexOf(r) > -1) {
        console.log(r);
        proxy.web(req, res, {
            target: {
                host: '52.174.179.132',
                port: '8081'
            }
        }, e => {
            console.log("ERROR")
            console.log(e)
            res.send(400, 'API SERVER ERROR');
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