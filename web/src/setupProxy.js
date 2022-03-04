const { createProxyMiddleware } = require('http-proxy-middleware')

module.exports = function (app) {
  app.use(createProxyMiddleware('/wsui', { target: 'http://localhost:5000', ws: true }))
}