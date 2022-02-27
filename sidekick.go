package main

import (
	"context"
	"flag"
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
	LogLevel     string
	Address      string
	WebRoot      string
	BaseURL      string
	ReadTimeout  time.Duration
	WriteTimeout time.Duration
	Frontend     WebSocketConf
	Backend      WebSocketConf
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

const (
	MsgOpControl byte = iota + 1 // Control message
	MsgOpMessage                 // P2P Message
)

const (
	MsgTypeError int = iota + 1
	MsgTypeJoin
	MsgTypeLeave
	MsgTypeRequest
	MsgTypeResponse
	MsgTypeWatch
	MsgTypeEvent
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
	ErrCodeBadOp
)

type ErrMsg struct {
	T    int `msgpack:"t"`
	Code int `msgpack:"c"`
}

var (
	msgPeerUnavailable = mustMarshal(ErrMsg{MsgTypeError, ErrCodePeerUnavailable})
	msgPeerDied        = mustMarshal(ErrMsg{MsgTypeError, ErrCodePeerDead})
	msgRateLimited     = mustMarshal(ErrMsg{MsgTypeError, ErrCodeRateLimited})
	msgErrBadOp        = mustMarshal(ErrMsg{MsgTypeError, ErrCodeBadOp})
)

type Actor struct {
	conn   *websocket.Conn
	sendC  chan []byte
	quitC  chan bool
	route  string
	pool   *ActorPool
	peer   *Actor
	peerMu sync.RWMutex
}

func newActor(conn *websocket.Conn, queueSize int, route string, pool *ActorPool) *Actor {
	return &Actor{
		conn:  conn,
		sendC: make(chan []byte, queueSize),
		quitC: make(chan bool),
		route: route,
		pool:  pool,
	}
}

func (a *Actor) Peer() *Actor {
	a.peerMu.RLock()
	defer a.peerMu.RUnlock()
	return a.peer
}

func (a *Actor) SetPeer(peer *Actor) {
	a.peerMu.Lock()
	a.peer = peer
	a.peerMu.Unlock()
}

func (a *Actor) Read(readLimit int64, rateLimit float64, rateLimitBurst int, pongTimeout time.Duration) {
	conn := a.conn
	defer func() {
		a.quit()
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
			a.send(msgRateLimited)
			return
		}

		_, msg, err := conn.ReadMessage()
		if err != nil {
			if websocket.IsUnexpectedCloseError(err, websocket.CloseGoingAway, websocket.CloseAbnormalClosure) {
				log.Error().Str("addr", conn.RemoteAddr().String()).Err(err).Msg("unexpected close")
			}
			return
		}

		peer := a.Peer()

		if peer == nil && a.pool != nil {
			peer = a.pool.Bridge(a)
			if peer != nil {
				log.Info().Str("remote", peer.conn.RemoteAddr().String()).Msg("bridged")
			}
		}

		if peer == nil {
			a.send(msgPeerUnavailable)
			continue // let actor decide whether to hang on or hang up
		}

		if len(msg) > 1 {
			op := msg[0]
			msg = msg[1:]
			switch op {
			case MsgOpMessage:
				if !peer.send(msg) {
					// peer dead; bail out
					a.send(msgPeerDied)
					return
				}
			case MsgOpControl:
				panic("not implemented") // XXX
			default:
				a.send(msgErrBadOp)
				return
			}
		}
	}
}

func (a *Actor) Write(writeTimeout, pingInterval time.Duration) {
	conn := a.conn
	ping := time.NewTicker(pingInterval)
	defer func() {
		ping.Stop()
		a.quit()
		log.Debug().Str("addr", conn.RemoteAddr().String()).Msg("writer closed")
	}()

	for {
		select {
		case msg, ok := <-a.sendC:
			conn.SetWriteDeadline(time.Now().Add(writeTimeout))
			if !ok {
				// send channel closed
				conn.WriteMessage(websocket.CloseMessage, []byte{})
				return
			}
			if err := conn.WriteMessage(websocket.BinaryMessage, msg); err != nil {
				log.Error().Err(err).Msg("write failed")
				return
			}
		case <-ping.C:
			conn.SetWriteDeadline(time.Now().Add(writeTimeout))
			if err := conn.WriteMessage(websocket.PingMessage, nil); err != nil {
				return
			}
		case <-a.quitC:
			return
		}
	}
}

func (a *Actor) send(b []byte) bool {
	select {
	case a.sendC <- b:
	default:
		close(a.sendC)
		return false
	}
	return true
}

func (a *Actor) quit() {
	a.conn.Close()
	peer := a.Peer()
	if peer != nil {
		a.SetPeer(nil)
		peer.quitC <- true
	}
}

type ActorPool struct {
	sync.Mutex
	actors map[string]map[*Actor]struct{}
}

func newActorPool() *ActorPool {
	return &ActorPool{
		actors: make(map[string]map[*Actor]struct{}),
	}
}

func (p *ActorPool) Put(route string, w *Actor) {
	p.Lock()

	actors, ok := p.actors[route]
	if !ok {
		actors = make(map[*Actor]struct{})
		p.actors[route] = actors
	}
	actors[w] = struct{}{}

	p.Unlock()
}

func (p *ActorPool) Bridge(caller *Actor) (callee *Actor) {
	p.Lock()
	if actors, ok := p.actors[caller.route]; ok {
		for callee = range actors {
			delete(actors, callee)
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

type Server struct {
	conf             Conf
	actors           *ActorPool
	frontendUpgrader websocket.Upgrader
	backendUpgrader  websocket.Upgrader
	fs               http.Handler
}

func newServer(conf Conf) (*Server, error) {
	html, err := loadIndexPage(conf.BaseURL, conf.WebRoot)
	if err != nil {
		return nil, err
	}
	clientConf, botConf := conf.Frontend, conf.Backend
	return &Server{
		conf,
		newActorPool(),
		newUpgrader(clientConf),
		newUpgrader(botConf),
		newWebServer(conf.BaseURL, conf.WebRoot, html),
	}, nil
}

func (s *Server) hijackBackend(w http.ResponseWriter, r *http.Request) {
	query := r.URL.Query()
	route := query.Get("r")
	log.Debug().Str("addr", r.RemoteAddr).Str("route", route).Msg("bot joining")

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

	conf := s.conf.Backend
	conn, err := s.backendUpgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Error().Err(err).Msg("failed to upgrade bot")
		return
	}

	a := newActor(conn, conf.MessageQueueSize, route, nil)

	s.actors.Put(route, a)

	go a.Write(conf.WriteTimeout, conf.PingInterval)
	go a.Read(conf.MaxMessageSize, conf.RateLimit, conf.RateLimitBurst, conf.PongTimeout)

	log.Info().Str("route", route).Str("addr", r.RemoteAddr).Msg("bot joined")
}

func (s *Server) hijackFrontend(w http.ResponseWriter, r *http.Request) {
	query := r.URL.Query()
	route := query.Get("r")
	log.Debug().Str("addr", r.RemoteAddr).Str("route", route).Msg("client joining")

	if route == "" {
		log.Error().Msg("empty route")
		http.Error(w, http.StatusText(http.StatusBadRequest), http.StatusBadRequest)
		return
	}

	// XXX authenticate

	conf := s.conf.Frontend
	conn, err := s.frontendUpgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Error().Err(err).Msg("failed to upgrade client")
		return
	}

	client := newActor(conn, conf.MessageQueueSize, route, s.actors)

	go client.Write(conf.WriteTimeout, conf.PingInterval)
	go client.Read(conf.MaxMessageSize, conf.RateLimit, conf.RateLimitBurst, conf.PongTimeout)

	log.Info().Str("addr", r.RemoteAddr).Msg("client joined")
}

func (s *Server) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	p := strings.TrimPrefix(r.URL.Path, s.conf.BaseURL)
	switch p {
	case "ws/f":
		s.hijackFrontend(w, r)
		return

	case "ws/b":
		s.hijackBackend(w, r)
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

	conf.ReadTimeout *= time.Second
	conf.WriteTimeout *= time.Second
	adjustDurations(&conf.Frontend)
	adjustDurations(&conf.Backend)

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

func serve(conf Conf) error {
	server, err := newServer(conf)
	if err != nil {
		return err
	}

	s := &http.Server{
		// TODO TLS config
		Addr:         conf.Address,
		Handler:      server,
		ReadTimeout:  conf.ReadTimeout,
		WriteTimeout: conf.WriteTimeout,
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

	confFile := flag.String("conf", "sidekick.toml", "location of configuration file")
	pretty := flag.Bool("pretty", false, "pretty-print and colorize log output for terminal")

	flag.Parse()

	conf, err := parseConf(*confFile)
	if err != nil {
		panic(err)
	}

	configureLogger(conf.LogLevel, *pretty)

	// handle error
	if err := serve(conf); err != nil {
		log.Fatal().Err(err).Msg("failed to run server")
	}
}
