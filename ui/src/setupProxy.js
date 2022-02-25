const { createProxyMiddleware } = require('http-proxy-middleware')

module.exports = function (app) {
  app.use(createProxyMiddleware('/ws/ui', { target: 'http://localhost:11111', ws: true }))
}