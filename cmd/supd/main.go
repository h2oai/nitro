package main

import (
	"flag"
	"fmt"
	"os"
	"os/signal"
	"sync"
	"time"

	"github.com/BurntSushi/toml"
	"github.com/go-cmd/cmd"
	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"
)

type Conf struct {
	LogLevel string
	Worker   []WorkerConf
}

type WorkerConf struct {
	Name     string
	Command  string
	Args     []string
	Env      []string
	Dir      string
	PoolSize int
}

var logLevels = map[string]zerolog.Level{
	zerolog.LevelPanicValue: zerolog.PanicLevel,
	zerolog.LevelFatalValue: zerolog.FatalLevel,
	zerolog.LevelErrorValue: zerolog.ErrorLevel,
	zerolog.LevelWarnValue:  zerolog.WarnLevel,
	zerolog.LevelInfoValue:  zerolog.InfoLevel,
	zerolog.LevelDebugValue: zerolog.DebugLevel,
	zerolog.LevelTraceValue: zerolog.TraceLevel,
}

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
	return conf, nil
}

type Worker struct {
	conf  WorkerConf
	quitC chan struct{}
	doneC chan struct{}
}

func newWorker(conf WorkerConf) *Worker {
	return &Worker{
		conf,
		make(chan struct{}),
		make(chan struct{}),
	}
}

func (w *Worker) run(log zerolog.Logger) {
	log.Info().Msg("starting")
	conf := w.conf
	options := cmd.Options{
		Buffered:  false,
		Streaming: true,
	}
	cmd := cmd.NewCmdOptions(options, conf.Command, conf.Args...)
	cmd.Env = conf.Env
	cmd.Dir = conf.Dir

	go func() {
		<-w.quitC
		if err := cmd.Stop(); err != nil {
			log.Error().Err(err).Msg("failed to stop")
		}
	}()

	go func() {
		defer func() {
			close(w.doneC)
			log.Info().Msg("stopped")
		}()

		for cmd.Stdout != nil || cmd.Stderr != nil {
			select {
			case line, ok := <-cmd.Stdout:
				if !ok {
					cmd.Stdout = nil
					continue
				}
				log.Info().Msg(line)

			case line, ok := <-cmd.Stderr:
				if !ok {
					cmd.Stderr = nil
					continue
				}
				log.Error().Msg(line)
			}
		}
	}()

	status := <-cmd.Start()

	logger := log.With().
		Int64("start", status.StartTs).
		Int64("stop", status.StopTs).
		Float64("runtime", status.Runtime).
		Bool("complete", status.Complete).
		Int("exit", status.Exit).
		Int("pid", status.PID).
		Logger()
	if status.Error != nil {
		logger.Error().Err(status.Error).Msg("failure")
	} else {
		logger.Info().Msg("success")
	}
}

type WorkerPool struct {
	sync.RWMutex
	conf     WorkerConf
	workers  map[*Worker]struct{}
	stopping bool
	counter  int
}

func newWorkerPool(conf WorkerConf) *WorkerPool {
	return &WorkerPool{
		conf:    conf,
		workers: make(map[*Worker]struct{}),
	}
}

func (p *WorkerPool) size() int {
	p.RLock()
	defer p.RUnlock()
	return len(p.workers)
}

func (p *WorkerPool) run() {
	p.Lock()
	defer p.Unlock()

	for k, n := len(p.workers), p.conf.PoolSize; k < n; k++ {
		w := newWorker(p.conf)
		p.workers[w] = struct{}{}
		p.counter += 1
		logger := log.With().
			Str("name", p.conf.Name).
			Int("worker", p.counter).
			Logger()
		go w.run(logger)
		go p.monitor(w)
	}
}

func (p *WorkerPool) monitor(w *Worker) {
	<-w.doneC
	p.Lock()
	delete(p.workers, w)
	p.Unlock()

	p.RLock()
	stopping := p.stopping
	p.RUnlock()

	if !stopping {
		p.run()
	}
}

func (p *WorkerPool) quit() {
	p.Lock()
	p.stopping = true
	p.Unlock()

	p.RLock()
	defer p.RUnlock()

	for w := range p.workers {
		w.quitC <- struct{}{}
	}
}

func main() {
	confFile := flag.String("conf", "supd.toml", "location of configuration file")
	pretty := flag.Bool("pretty", false, "pretty-print and colorize log output for terminal")

	flag.Parse()

	conf, err := parseConf(*confFile)
	if err != nil {
		panic(err)
	}

	configureLogger(conf.LogLevel, *pretty)

	sigC := make(chan os.Signal, 1)
	signal.Notify(sigC, os.Interrupt)

	pools := make([]*WorkerPool, len(conf.Worker))
	for i, c := range conf.Worker {
		pool := newWorkerPool(c)
		pools[i] = pool
		pool.run()
	}

	<-sigC

	done := make(chan struct{})
	go func() {
		defer close(done)
		for _, pool := range pools {
			pool.quit()
		}

		ticker := time.NewTicker(500 * time.Millisecond)
		stop := time.NewTimer(10 * time.Second)
		for {
			select {
			case <-stop.C:
				return
			case <-ticker.C:
				n := 0
				for _, pool := range pools {
					n += pool.size()
				}
				if n == 0 {
					return
				}
			}
		}
	}()

	log.Info().Msg("pools stopping")
	<-done
	log.Info().Msg("pools stopped")
}
