const { createProxyMiddleware } = require('http-proxy-middleware')

module.exports = function (app) {
  app.use(createProxyMiddleware('/nitro', { target: 'http://localhost:5000', ws: true }))
}