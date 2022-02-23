const { createProxyMiddleware } = require('http-proxy-middleware')

const wsFilter = (path) => path.endsWith('/in')

module.exports = function (app) {
  app.use(createProxyMiddleware(wsFilter, { target: 'http://localhost:11111', ws: true }))
}