var http = require('http');

server = http.createServer(function (request, response) {
  response.writeHead(200, {'Content-Type': 'text/plain'});
  response.end('Hello World\n');
}).listen(0, '127.0.0.1', function (e, b) {
  console.log('Server running at %j', this.address());
});

