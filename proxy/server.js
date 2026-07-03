const http = require('http');

const GRAFANA_HOST = process.env.GRAFANA_HOST || 'grafana';
const GRAFANA_PORT = parseInt(process.env.GRAFANA_PORT || '3000', 10);
const PROXY_PORT = parseInt(process.env.PROXY_PORT || '3000', 10);

function fixQueryBody(body) {
  try {
    const parsed = JSON.parse(body);
    if (parsed.queries && Array.isArray(parsed.queries)) {
      let fixed = false;
      for (const q of parsed.queries) {
        const ds = q.datasource;
        if (ds && !ds.uid && ds.name) {
          ds.uid = ds.name;
          delete ds.name;
          fixed = true;
        }
      }
      if (fixed) return JSON.stringify(parsed);
    }
  } catch (e) {
    console.error('Failed to parse request body:', e.message);
  }
  return null;
}

function proxyRequest(req, res, options) {
  return new Promise((resolve, reject) => {
    const proxyReq = http.request(options, (proxyRes) => {
      const chunks = [];
      proxyRes.on('data', (c) => chunks.push(c));
      proxyRes.on('end', () => {
        if (!res.writableEnded) {
          res.writeHead(proxyRes.statusCode, proxyRes.headers);
          res.end(Buffer.concat(chunks));
        }
        resolve();
      });
    });
    proxyReq.setTimeout(60000, () => { proxyReq.destroy(); reject(new Error('timeout')); });
    proxyReq.on('error', reject);
    req.pipe(proxyReq);
    req.on('error', () => proxyReq.destroy());
  });
}

const server = http.createServer((req, res) => {
  const isDSQuery = req.method === 'POST' && req.url === '/api/ds/query';
  const headers = {};
  for (const [k, v] of Object.entries(req.headers)) {
    const lk = k.toLowerCase();
    if (lk !== 'proxy-connection' && lk !== 'content-length' && lk !== 'transfer-encoding') {
      headers[k] = v;
    }
  }

  const makeProxy = (body, customHeaders) => {
    const opts = {
      hostname: GRAFANA_HOST, port: GRAFANA_PORT,
      path: req.url, method: req.method,
      headers: { ...headers, ...customHeaders },
    };
    const proxyReq = http.request(opts, (proxyRes) => {
      res.writeHead(proxyRes.statusCode, proxyRes.headers);
      proxyRes.pipe(res);
    });
    proxyReq.setTimeout(60000, () => { proxyReq.destroy(); if (!res.writableEnded) { res.writeHead(504); res.end('Gateway Timeout'); } });
    proxyReq.on('error', (err) => { console.error('Proxy error:', err.message); if (!res.writableEnded) { res.writeHead(502); res.end('Bad Gateway'); } });
    if (body !== undefined) {
      proxyReq.write(body);
    }
    proxyReq.end();
    return proxyReq;
  };

  if (isDSQuery) {
    let body = '';
    req.on('data', (c) => body += c);
    req.on('end', () => {
      const fixed = fixQueryBody(body);
      if (fixed !== null) {
        console.log('Fixed /api/ds/query datasource ref');
        body = fixed;
      }
      makeProxy(body, { 'content-length': Buffer.byteLength(body) });
    });
    req.on('error', () => {});
  } else {
    const opts = {
      hostname: GRAFANA_HOST, port: GRAFANA_PORT,
      path: req.url, method: req.method, headers,
    };
    const proxyReq = http.request(opts, (proxyRes) => {
      res.writeHead(proxyRes.statusCode, proxyRes.headers);
      proxyRes.pipe(res);
    });
    proxyReq.setTimeout(60000, () => { proxyReq.destroy(); if (!res.writableEnded) { res.writeHead(504); res.end('Gateway Timeout'); } });
    proxyReq.on('error', (err) => { console.error('Proxy error:', err.message); if (!res.writableEnded) { res.writeHead(502); res.end('Bad Gateway'); } });
    req.pipe(proxyReq);
    req.on('error', () => proxyReq.destroy());
  }
});

server.on('upgrade', (req, socket, head) => {
  const opts = {
    hostname: GRAFANA_HOST, port: GRAFANA_PORT,
    path: req.url, method: req.method, headers: req.headers,
  };
  const proxyReq = http.request(opts);
  proxyReq.on('upgrade', (proxyRes, proxySocket, proxyHead) => {
    socket.write(
      'HTTP/1.1 101 Switching Protocols\r\n' +
      'Upgrade: websocket\r\n' +
      'Connection: Upgrade\r\n' +
      `Sec-WebSocket-Accept: ${proxyRes.headers['sec-websocket-accept']}\r\n` +
      '\r\n'
    );
    proxySocket.pipe(socket);
    socket.pipe(proxySocket);
  });
  proxyReq.on('error', () => socket.destroy());
  proxyReq.end();
});

server.listen(PROXY_PORT, () => {
  console.log(`Grafana proxy listening on port ${PROXY_PORT}, forwarding to ${GRAFANA_HOST}:${GRAFANA_PORT}`);
});
