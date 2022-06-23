import { B, isO, S } from "./core"
import { Message, Server, ServerEvent, ServerEventHandler, ServerEventT } from "./protocol"
import yaml from "js-yaml"

const
  defaultRuntime = 'https://cdn.jsdelivr.net/pyodide/v0.20.0/full/pyodide.js',
  defaultBundle = 'h2o_nitride'

type Conf = {
  language: S
  runtime: S
  packages: S[]
  bundles: S[]
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
  packages: S[]
  bundles: S[]
  files: S[]
  entrypoint: S
  program: S
  autoload: B
} | {
  t: CommandT.ProgramLoaded
} | {
  t: CommandT.LoadModule
} | {
  t: CommandT.ModuleLoaded
}

const
  pythonConf: Conf = {
    language: 'python',
    runtime: defaultRuntime,
    packages: [],
    bundles: [],
    files: [],
    entrypoint: '',
    autoload: false,
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
      el = document.querySelector<HTMLScriptElement>('script[type="application/nitro"]'),
      data = el?.textContent
    if (data) {
      try {
        const raw: any = yaml.load(data)
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
      const
        program = scripts.join('\n\n'),
        { runtime, packages, bundles, autoload, files, entrypoint } = conf,
        c: Command = { t: CommandT.LoadProgram, runtime, packages, bundles, autoload, files, entrypoint, program }
      c.bundles.unshift(defaultBundle)
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
