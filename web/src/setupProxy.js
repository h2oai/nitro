const { createProxyMiddleware } = require('http-proxy-middleware')

module.exports = function (app) {
  app.use(createProxyMiddleware('/ws/f', { target: 'http://localhost:11111', ws: true }))
}