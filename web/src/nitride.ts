import { B, isO, S } from "./core"
import { Message, Server, ServerEvent, ServerEventHandler, ServerEventT } from "./protocol"
import yaml from "js-yaml"

type Conf = {
  language: S
  runtime: S
  packages: S[]
  autoload: B
  files: S[]
  entrypoint: S
}

enum CommandT { Error, Execute, LoadProgram, ProgramLoaded, ModuleLoaded, LoadModule }

type Command = {
  t: CommandT.Error
  error: S
} | {
  t: CommandT.Execute
  message: S
} | {
  t: CommandT.LoadProgram
  runtime: S
  program: S
  autoload: B
} | {
  t: CommandT.ProgramLoaded
} | {
  t: CommandT.LoadModule
} | {
  t: CommandT.ModuleLoaded
}

const prelude = `
import micropip
await micropip.install('h2o_nitride-0.10.1-py3-none-any.whl') # XXX USE PUBLISHED VERSION
`
const spawn = `
# XXX MOVE TO WHEEL
import asyncio
import collections

class PollIO:
    def __init__(self):
        self._input = collections.deque()
        self._output = collections.deque()
    async def send(self, x):
        self._output.append(x)
    async def recv(self):
        while True:
            print('in recv')
            if len(self._input):
                return self._input.popleft()
            await asyncio.sleep(0.1)
    def write(self, x):
        self._input.append(x)
    def read(self):
        return self._output.popleft() if len(self._output) else None

_nitro_io = PollIO()
print('starting to serve')
asyncio.create_task(nitro.serve(_nitro_io.send, _nitro_io.recv))
print('done serving')
`
const
  pythonConf: Conf = {
    language: 'python',
    runtime: 'https://cdn.jsdelivr.net/pyodide/v0.20.0/full/pyodide.js',
    packages: [],
    autoload: false,
    files: [],
    entrypoint: '',
  },
  dedent = (code: S): S => {
    const
      lines = code.split(/\r?\n/),
      indents = lines
        .filter(s => s.trim().length)
        .map(s => {
          const m = s.match(/^\s*/)
          return m ? m[0].length : 0
        }),
      indent = Math.min(...indents)
    return indent ? lines.map(s => s.substring(indent)).join('\n') : code
  },
  readScripts = (): S[] => Array.from(document.querySelectorAll<HTMLScriptElement>('script[type="text/python"]'))
    .map(e => e.textContent as S)
    .filter(s => s?.length)
    .map(dedent),
  readConf = (): Conf => {
    const
      el = document.querySelector<HTMLScriptElement>('script[type="text/nitro"]'),
      conf = el?.textContent
    if (conf) {
      try {
        const raw: any = yaml.load(conf)
        if (isO(raw)) return { ...pythonConf, ...raw }
      } catch (e) {
        console.error(`Failed parsing Nitro configuration, using defaults instead: ${e}. .`)
      }
    }
    return pythonConf
  },
  connectEvent: ServerEvent = { t: ServerEventT.Connect }

export const newLocalServer = (): Server => {
  let _worker: Worker | null = null

  const
    scripts = readScripts(),
    conf = readConf(),
    connect = (handle: ServerEventHandler) => {
      _worker = new Worker('nitride.js');
      _worker.onmessage = (event) => {
        const c = event.data as Command
        switch (c.t) {
          case CommandT.Error:
            handle({ t: ServerEventT.Error, error: c.error })
            break
          case CommandT.Execute:
            handle({ t: ServerEventT.Message, message: JSON.parse(c.message) })
            break
          case CommandT.ProgramLoaded:
            handle(connectEvent)
            break
          default:
            handle({ t: ServerEventT.Error, error: 'Unknown message received from worker.' })
        }
      }
      const program = [prelude, ...scripts, spawn].join('\n\n')
      const c: Command = { t: CommandT.LoadProgram, runtime: conf.runtime, program, autoload: conf.autoload }
      _worker.postMessage(c)
    },
    send = (message: Message) => {
      if (_worker) {
        const c: Command = { t: CommandT.Execute, message: JSON.stringify(message) }
        _worker.postMessage(c)
      }
    },
    disconnect = () => { }
  return { connect, send, disconnect }
}
