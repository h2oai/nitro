const { createProxyMiddleware } = require('http-proxy-middleware')

module.exports = function (app) {
  app.use(createProxyMiddleware('/sidekick', { target: 'http://localhost:5000', ws: true }))
}