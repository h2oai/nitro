const { createProxyMiddleware } = require('http-proxy-middleware')

module.exports = function (app) {
  app.use(createProxyMiddleware('/wss', { target: 'http://localhost:11111', ws: true }))
}