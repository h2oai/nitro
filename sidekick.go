package main

import (
	"context"
	"fmt"
	"net/http"
	"os"
	"os/signal"
	"path"
	"strings"
	"sync"
	"time"

	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"

	"github.com/BurntSushi/toml"
	"github.com/gorilla/websocket"
)

type Conf struct {
	LogLevel        string
	Address         string
	WebRoot         string
	BasePath        string
	ClientWebSocket WebSocketConf
	BotWebSocket    WebSocketConf
	Bot             []BotConf
}

type WebSocketConf struct {
	ReadBufferSize   int
	WriteBufferSize  int
	MaxMessageSize   int64
	MessageQueueSize int
	PingInterval     time.Duration
	PongTimeout      time.Duration
	WriteTimeout     time.Duration
}

type BotConf struct {
	Name             string
	Path             string
	Command          string
	Arguments        []string
	Env              []string
	InheritEnv       bool
	WorkingDirectory string
}

var (
	newline = []byte{'\n'}
)

type Actor struct {
	sync.RWMutex
	conn *websocket.Conn
	send chan []byte
	peer *Actor
}

type Client struct {
	*Actor
}

type Bot struct {
	*Actor
}

func (c *Actor) Read(readLimit int64, pongTimeout time.Duration) {
	conn := c.conn
	defer func() {
		conn.Close()
		log.Debug().Str("addr", conn.RemoteAddr().String()).Msg("reader closed")
	}()
	conn.SetReadLimit(readLimit)
	conn.SetReadDeadline(time.Now().Add(pongTimeout))
	conn.SetPongHandler(func(string) error {
		conn.SetReadDeadline(time.Now().Add(pongTimeout))
		return nil
	})
	for {
		_, message, err := conn.ReadMessage()
		if err != nil {
			if websocket.IsUnexpectedCloseError(err, websocket.CloseGoingAway, websocket.CloseAbnormalClosure) {
				log.Error().Str("addr", conn.RemoteAddr().String()).Err(err).Msg("unexpected close")
			}
			return
		}

		peer := c.peer

		select {
		case peer.send <- message:
		default: // peer dead
			close(peer.send)

			// reply with peer-dead
			select {
			case c.send <- message: // XXX send peer-dead
			default: // i'm dead, too
				close(c.send)
			}

			return // stop reading
		}
	}
}

func (c *Actor) Write(writeTimeout, pingInterval time.Duration) {
	conn := c.conn
	ping := time.NewTicker(pingInterval)
	defer func() {
		ping.Stop()
		conn.Close()
		log.Debug().Str("addr", conn.RemoteAddr().String()).Msg("reader closed")
	}()
	for {
		select {
		case message, ok := <-c.send:
			conn.SetWriteDeadline(time.Now().Add(writeTimeout))
			if !ok {
				// send channel closed
				conn.WriteMessage(websocket.CloseMessage, []byte{})
				return
			}

			w, err := conn.NextWriter(websocket.TextMessage)
			if err != nil {
				log.Error().Err(err).Msg("failed to obtain connection writer")
				return
			}
			w.Write(message)

			// drain
			n := len(c.send)
			for i := 0; i < n; i++ {
				w.Write(newline)
				w.Write(<-c.send)
			}

			if err := w.Close(); err != nil {
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
	pool           *BotPool
	routes         map[string]http.HandlerFunc
	clientUpgrader websocket.Upgrader
	botUpgrader    websocket.Upgrader
}

const (
	inSocketSuffix  = "/in"
	outSocketSuffix = "/out"
)

type BotPool struct {
	bots chan *Bot
}

func newBotPool() *BotPool {
	return &BotPool{bots: make(chan *Bot, 512)}
}

func (s *Server) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	p := r.URL.Path

	for route, fs := range s.routes {
		if !strings.HasPrefix(p, route) {
			continue
		}

		if strings.HasSuffix(p, inSocketSuffix) {
			log.Debug().Str("addr", r.RemoteAddr).Msg("client joining")
			conf := s.conf.ClientWebSocket

			conn, err := s.clientUpgrader.Upgrade(w, r, nil)
			if err != nil {
				log.Error().Err(err).Msg("failed to upgrade client")
				return
			}

			select {
			case bot := <-s.pool.bots:
				client := &Client{
					&Actor{
						conn: conn,
						send: make(chan []byte, conf.MessageQueueSize),
						peer: bot.Actor,
					},
				}
				bot.peer = client.Actor

				go client.Write(conf.WriteTimeout, conf.PingInterval)
				go client.Read(conf.MaxMessageSize, conf.PongTimeout)

			default: // pool empty
				conn.SetWriteDeadline(time.Now().Add(conf.WriteTimeout))
				conn.WriteMessage(websocket.CloseMessage, websocket.FormatCloseMessage(websocket.CloseTryAgainLater, "unavailable"))
				conn.Close()

			}

		} else if strings.HasSuffix(p, outSocketSuffix) {
			log.Debug().Str("addr", r.RemoteAddr).Msg("bot joining")
			conf := s.conf.BotWebSocket

			conn, err := s.botUpgrader.Upgrade(w, r, nil)
			if err != nil {
				log.Error().Err(err).Msg("failed to upgrade bot")
				return
			}
			bot := &Bot{
				&Actor{
					conn: conn,
					send: make(chan []byte, conf.MessageQueueSize),
				},
			}

			select {
			case s.pool.bots <- bot:
				go bot.Write(conf.WriteTimeout, conf.PingInterval)
				go bot.Read(conf.MaxMessageSize, conf.PongTimeout)
			default: // pool full
				conn.SetWriteDeadline(time.Now().Add(conf.WriteTimeout))
				conn.WriteMessage(websocket.CloseMessage, websocket.FormatCloseMessage(websocket.CloseTryAgainLater, "crowded"))
				conn.Close()
			}
		} else {
			if r.Method != http.MethodGet {
				http.Error(w, http.StatusText(http.StatusMethodNotAllowed), http.StatusMethodNotAllowed)
				return
			}
			fs.ServeHTTP(w, r)
		}
		return
	}

	http.Error(w, http.StatusText(http.StatusNotFound), http.StatusNotFound)
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

func newServer(conf Conf) *Server {
	clientConf, botConf := conf.ClientWebSocket, conf.BotWebSocket

	fs := http.FileServer(http.Dir(conf.WebRoot))

	routes := make(map[string]http.HandlerFunc)
	for _, bc := range conf.Bot {
		p := path.Clean(conf.BasePath + bc.Path)
		// Ensure trailing slash so that relative URLs for static files resolve correctly
		if p != "/" {
			p += "/"
		}
		log.Debug().Str("path", p).Msg("register path")
		routes[p] = http.StripPrefix(p, fs).ServeHTTP
	}
	return &Server{
		conf,
		newBotPool(),
		routes,
		newUpgrader(clientConf),
		newUpgrader(botConf),
	}
}

func serve(conf Conf) error {
	server := newServer(conf)

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

func main() {
	conf, err := parseConf("./sidekick.toml")
	if err != nil {
		panic(err)
	}

	zerolog.TimeFieldFormat = zerolog.TimeFormatUnix
	zerolog.SetGlobalLevel(toLogLevel(conf.LogLevel))

	// handle error
	if err := serve(conf); err != nil {
		log.Fatal().Err(err).Msg("failed to run server")
	}
}
