package main

import (
	"context"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"os/signal"
	"path"
	"path/filepath"
	"strings"
	"sync"
	"time"

	"github.com/BurntSushi/toml"
	"github.com/gorilla/websocket"
	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"
	"github.com/vmihailenco/msgpack/v5"
	"golang.org/x/time/rate"
)

type Conf struct {
	LogLevel        string
	Address         string
	WebRoot         string
	BaseURL         string
	ClientWebSocket WebSocketConf
	BotWebSocket    WebSocketConf
}

type WebSocketConf struct {
	ReadBufferSize   int
	WriteBufferSize  int
	MaxMessageSize   int64
	MessageQueueSize int
	PingInterval     time.Duration
	PongTimeout      time.Duration
	WriteTimeout     time.Duration
	RateLimit        float64
	RateLimitBurst   int
}

type Creds struct {
	ID     string `json:"id"`
	Secret string `json:"secret"`
}

type Actor struct {
	conn   *websocket.Conn
	sendC  chan []byte
	route  string
	pool   *WorkerPool
	peer   *Actor
	peerMu sync.RWMutex
}

func (c *Actor) Peer() *Actor {
	c.peerMu.RLock()
	defer c.peerMu.RUnlock()
	return c.peer
}

func (c *Actor) SetPeer(peer *Actor) {
	c.peerMu.Lock()
	c.peer = peer
	c.peerMu.Unlock()
}

func (c *Actor) send(b []byte) bool {
	select {
	case c.sendC <- b:
	default:
		close(c.sendC)
		return false
	}
	return true
}

type MsgOp byte // Header, first byte

const (
	MsgOpControl MsgOp = iota + 1 // Control message
	MsgOpMessage                  // P2P Message
)

const (
	MsgTypeError int = iota + 1
	MsgTypeJoin
	MsgTypeLeave
	MsgOpRequest
	MsgOpResponse
	MsgOpWatch
	MsgOpEvent
	MsgTypeText
	MsgTypeInput
	MsgTypeAbort
	MsgTypeResume
	MsgTypeRead
	MsgTypeWrite
	MsgTypeAppend
)

const (
	ErrCodePeerUnavailable int = iota + 1
	ErrCodePeerDead
	ErrCodeRateLimited
)

type ErrMsg struct {
	T    int `msgpack:"t"`
	Code int `msgpack:"c"`
}

var (
	msgPeerUnavailable = mustMarshal(ErrMsg{MsgTypeError, ErrCodePeerUnavailable})
	msgPeerDied        = mustMarshal(ErrMsg{MsgTypeError, ErrCodePeerDead})
	msgRateLimited     = mustMarshal(ErrMsg{MsgTypeError, ErrCodeRateLimited})
)

func (c *Actor) Read(readLimit int64, rateLimit float64, rateLimitBurst int, pongTimeout time.Duration) {
	conn := c.conn
	defer func() {
		conn.Close()
		peer := c.Peer()
		if peer != nil {
			peer.conn.Close()
		}
		log.Debug().Str("addr", conn.RemoteAddr().String()).Msg("reader closed")
	}()
	conn.SetReadLimit(readLimit)
	conn.SetReadDeadline(time.Now().Add(pongTimeout))
	conn.SetPongHandler(func(string) error {
		conn.SetReadDeadline(time.Now().Add(pongTimeout))
		return nil
	})

	limiter := rate.NewLimiter(rate.Limit(rateLimit), rateLimitBurst)

	for {

		if !limiter.Allow() {
			c.send(msgRateLimited)
			return
		}

		_, message, err := conn.ReadMessage()
		if err != nil {
			if websocket.IsUnexpectedCloseError(err, websocket.CloseGoingAway, websocket.CloseAbnormalClosure) {
				log.Error().Str("addr", conn.RemoteAddr().String()).Err(err).Msg("unexpected close")
			}
			return
		}

		peer := c.Peer()

		if peer == nil && c.pool != nil {
			peer = c.pool.Match(c)
		}

		if peer == nil {
			c.send(msgPeerUnavailable)
			continue
		}

		if !peer.send(message) {
			// peer dead; bail out
			c.send(msgPeerDied)
			return
		}
	}
}

func (c *Actor) Write(writeTimeout, pingInterval time.Duration) {
	conn := c.conn
	ping := time.NewTicker(pingInterval)
	defer func() {
		ping.Stop()
		conn.Close()
		peer := c.Peer()
		if peer != nil {
			peer.conn.Close()
		}
		log.Debug().Str("addr", conn.RemoteAddr().String()).Msg("writer closed")
	}()

	for {
		select {
		case msg, ok := <-c.sendC:
			conn.SetWriteDeadline(time.Now().Add(writeTimeout))
			if !ok {
				// send channel closed
				conn.WriteMessage(websocket.CloseMessage, []byte{})
				return
			}
			if err := conn.WriteMessage(websocket.BinaryMessage, msg); err != nil {
				log.Error().Err(err).Msg("failed to write message")
				return
			}
		case <-ping.C:
			conn.SetWriteDeadline(time.Now().Add(writeTimeout))
			if err := conn.WriteMessage(websocket.PingMessage, nil); err != nil {
				return
			}
		}
	}
}

type Server struct {
	conf           Conf
	workers        *WorkerPool
	clientUpgrader websocket.Upgrader
	workerUpgrader websocket.Upgrader
	fs             http.Handler
}

type WorkerPool struct {
	sync.Mutex
	workers map[string]map[*Actor]struct{}
}

func newWorkerPool() *WorkerPool {
	return &WorkerPool{
		workers: make(map[string]map[*Actor]struct{}),
	}
}

func (p *WorkerPool) Put(route string, w *Actor) {
	p.Lock()

	workers, ok := p.workers[route]
	if !ok {
		workers = make(map[*Actor]struct{})
		p.workers[route] = workers
	}
	workers[w] = struct{}{}

	p.Unlock()
}

func (p *WorkerPool) Match(caller *Actor) (callee *Actor) {
	p.Lock()
	if workers, ok := p.workers[caller.route]; ok {
		for callee = range workers {
			delete(workers, callee)
			break
		}
	}
	p.Unlock()

	if callee != nil {
		callee.SetPeer(caller)
		caller.SetPeer(callee)
	}
	return
}

func (s *Server) hijackBot(w http.ResponseWriter, r *http.Request) {
	query := r.URL.Query()
	route := query.Get("r")
	log.Debug().Str("addr", r.RemoteAddr).Str("route", route).Msg("worker joining")

	if route == "" {
		log.Error().Msg("empty route")
		http.Error(w, http.StatusText(http.StatusBadRequest), http.StatusBadRequest)
		return
	}

	id, secret, ok := r.BasicAuth()
	if !ok {
		log.Error().Msg("missing basic auth")
		http.Error(w, http.StatusText(http.StatusUnauthorized), http.StatusUnauthorized)
		return
	}

	if id != secret { // XXX check via keychain
		log.Error().Msg("bad id/secret")
		http.Error(w, http.StatusText(http.StatusUnauthorized), http.StatusUnauthorized)
		return
	}

	conf := s.conf.BotWebSocket
	conn, err := s.workerUpgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Error().Err(err).Msg("failed to upgrade bot")
		return
	}
	worker := &Actor{
		conn:  conn,
		sendC: make(chan []byte, conf.MessageQueueSize),
		route: route,
	}

	s.workers.Put(route, worker)

	go worker.Write(conf.WriteTimeout, conf.PingInterval)
	go worker.Read(conf.MaxMessageSize, conf.RateLimit, conf.RateLimitBurst, conf.PongTimeout)

	log.Info().Str("route", route).Str("addr", r.RemoteAddr).Msg("worker joined")
}

func (s *Server) hijackClient(w http.ResponseWriter, r *http.Request) {
	query := r.URL.Query()
	route := query.Get("r")
	log.Debug().Str("addr", r.RemoteAddr).Str("route", route).Msg("client joining")

	if route == "" {
		log.Error().Msg("empty route")
		http.Error(w, http.StatusText(http.StatusBadRequest), http.StatusBadRequest)
		return
	}

	// XXX authenticate

	conf := s.conf.ClientWebSocket
	conn, err := s.clientUpgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Error().Err(err).Msg("failed to upgrade client")
		return
	}

	client := &Actor{
		conn:  conn,
		sendC: make(chan []byte, conf.MessageQueueSize),
		route: route,
		pool:  s.workers,
	}

	go client.Write(conf.WriteTimeout, conf.PingInterval)
	go client.Read(conf.MaxMessageSize, conf.RateLimit, conf.RateLimitBurst, conf.PongTimeout)

	log.Info().Str("addr", r.RemoteAddr).Msg("client joined")
}

func (s *Server) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	p := strings.TrimPrefix(r.URL.Path, s.conf.BaseURL)

	log.Debug().Str("path", r.URL.Path).Msg("request")

	switch p {
	case "ws/ui":
		s.hijackClient(w, r)
		return

	case "ws/bot":
		s.hijackBot(w, r)
		return
	}

	if r.Method != http.MethodGet {
		http.Error(w, http.StatusText(http.StatusMethodNotAllowed), http.StatusMethodNotAllowed)
		return
	}

	s.fs.ServeHTTP(w, r)
}

func adjustDurations(conf *WebSocketConf) {
	conf.WriteTimeout *= time.Second
	conf.PingInterval *= time.Second
	conf.PongTimeout *= time.Second
}

func parseConf(filename string) (Conf, error) {
	var conf Conf
	if meta, err := toml.DecodeFile(filename, &conf); err != nil {
		return conf, fmt.Errorf("failed to decode configuration file: %v", err)
	} else {
		undecoded := meta.Undecoded()
		if len(undecoded) > 0 {
			return conf, fmt.Errorf("illegal keys found in configuration: %v", undecoded)
		}
	}

	adjustDurations(&conf.ClientWebSocket)
	adjustDurations(&conf.BotWebSocket)

	return conf, nil
}

func newUpgrader(conf WebSocketConf) websocket.Upgrader {
	return websocket.Upgrader{
		ReadBufferSize:  conf.ReadBufferSize,
		WriteBufferSize: conf.WriteBufferSize,
	}
}

func loadIndexPage(baseURL, webRoot string) ([]byte, error) {
	b, err := ioutil.ReadFile(filepath.Join(webRoot, "index.html"))
	if err != nil {
		return nil, fmt.Errorf("failed reading default index.html page: %v", err)
	}

	// embed base url
	html := strings.Replace(string(b), "<body", `<body data-baseurl="`+baseURL+`"`, 1)

	// redirect /foo -> /base/url/foo
	html = strings.ReplaceAll(html, `="/`, `="`+baseURL)

	return []byte(html), nil
}

func newWebServer(baseURL, webRoot string, html []byte) http.Handler {
	fs := http.StripPrefix(baseURL, http.FileServer(http.Dir(webRoot)))
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// if the url has an extension, serve the file
		if len(path.Ext(r.URL.Path)) > 0 {
			fs.ServeHTTP(w, r)
			return
		}

		// url has no extension; assume index.html
		header := w.Header()
		header.Add("Content-Type", "text/html; charset=UTF-8")
		header.Add("Cache-Control", "no-cache, must-revalidate")
		header.Add("Pragma", "no-cache")
		w.Write(html)
	})
}

func newServer(conf Conf) (*Server, error) {
	html, err := loadIndexPage(conf.BaseURL, conf.WebRoot)
	if err != nil {
		return nil, err
	}
	clientConf, botConf := conf.ClientWebSocket, conf.BotWebSocket
	return &Server{
		conf,
		newWorkerPool(),
		newUpgrader(clientConf),
		newUpgrader(botConf),
		newWebServer(conf.BaseURL, conf.WebRoot, html),
	}, nil
}

func serve(conf Conf) error {
	server, err := newServer(conf)
	if err != nil {
		return err
	}

	s := &http.Server{
		// TODO TLS config
		Addr:         conf.Address,
		Handler:      server,
		ReadTimeout:  time.Second * 10, // TODO expose
		WriteTimeout: time.Second * 10, // TODO expose
	}

	errC := make(chan error, 1)
	go func() {
		// TODO TLS
		log.Info().Str("address", conf.Address).Msg("listening")
		errC <- s.ListenAndServe()
	}()

	sigC := make(chan os.Signal, 1)
	signal.Notify(sigC, os.Interrupt)

	select {
	case err := <-errC:
		log.Error().Err(err).Msg("failed to listen")
	case sig := <-sigC:
		log.Info().Str("signal", sig.String()).Msg("stopping")
	}

	ctx, cancel := context.WithTimeout(context.Background(), time.Second*10)
	defer cancel()

	return s.Shutdown(ctx)
}

var (
	logLevels = map[string]zerolog.Level{
		zerolog.LevelPanicValue: zerolog.PanicLevel,
		zerolog.LevelFatalValue: zerolog.FatalLevel,
		zerolog.LevelErrorValue: zerolog.ErrorLevel,
		zerolog.LevelWarnValue:  zerolog.WarnLevel,
		zerolog.LevelInfoValue:  zerolog.InfoLevel,
		zerolog.LevelDebugValue: zerolog.DebugLevel,
		zerolog.LevelTraceValue: zerolog.TraceLevel,
	}
)

func toLogLevel(s string) zerolog.Level {
	if level, ok := logLevels[s]; ok {
		return level
	}
	return zerolog.Disabled
}

func configureLogger(logLevel string, pretty bool) {
	zerolog.TimestampFieldName = "t"
	zerolog.LevelFieldName = "l"
	zerolog.MessageFieldName = "m"
	zerolog.TimeFieldFormat = zerolog.TimeFormatUnix
	zerolog.SetGlobalLevel(toLogLevel(logLevel))

	if pretty {
		log.Logger = log.Output(zerolog.ConsoleWriter{Out: os.Stderr})
	}
}

func mustMarshal(i interface{}) []byte {
	b, err := msgpack.Marshal(i)
	if err != nil {
		panic(err)
	}
	return b
}

func main() {

	conf, err := parseConf("./sidekick.toml") // XXX tie to -conf
	if err != nil {
		panic(err)
	}

	configureLogger(conf.LogLevel, true) // XXX tie to -pretty

	// handle error
	if err := serve(conf); err != nil {
		log.Fatal().Err(err).Msg("failed to run server")
	}
}
