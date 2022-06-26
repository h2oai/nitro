const defaultRuntime = 'https://cdn.jsdelivr.net/pyodide/v0.20.0/full/pyodide.js'

type S = string
type B = boolean

type PyodideGlobals = {
  get(name: S): any
}

type Pyodide = {
  globals: PyodideGlobals
  loadPackage(packages: S[]): Promise<void>
  loadPackagesFromImports(code: S): Promise<void>
  runPythonAsync(code: S): Promise<void>
}

interface WorkerGlobalScope {
  pyodide: Pyodide
  io: NitrideIO
}

declare const loadPyodide: () => Pyodide

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

type NitrideIO = {
  read(): S
  write(data: S): void
}

const pollInterval = 100

let _poller = 0

const prelude = `
import asyncio
import micropip
from pyodide.http import pyfetch
async def _nitro_download(url, filename):
    r = await pyfetch(url)
    if r.status != 200:
        raise RuntimeError(f'Failed fetching file {url}, status {r.status}.')
    with open(filename, "wb") as f:
        f.write(await r.bytes())
    return
`

const launcher = `
from h2o_nitro import Duplex as _Nitro_IO
_nitro_io = _Nitro_IO()
asyncio.create_task(nitro.serve(_nitro_io.send, _nitro_io.recv))
print('🚀 Nitro launched! 🚀')
print('Please take a moment to ⭐ Nitro on Github: https://github.com/h2oai/nitro')
`

async function init(command: Command) {
  if (command.t !== CommandT.LoadProgram) return

  if (!command.runtime.length) command.runtime = defaultRuntime

  const { runtime, packages, bundles, autoload, files, entrypoint, program } = command

  console.log(`Loading runtime ${runtime}...`)
  importScripts(runtime)

  console.log('Loading Pyodide...')
  const pyodide = await loadPyodide()

  console.log('Installing micropip...')
  await pyodide.loadPackage(["micropip"])

  if (packages.length) {
    console.log(`Installing packages ${packages.join(', ')}...`)
    await pyodide.loadPackage(packages)
  }

  console.log('Executing prelude...')
  await pyodide.runPythonAsync(prelude)

  let loadNitro = true
  for (const bundle of bundles) {
    if (bundle === 'h2o-nitro' || bundle === 'h2o_nitro' || bundle.indexOf('h2o_nitro-') >= 0) {
      loadNitro = false
      break
    }
  }

  if (loadNitro) bundles.unshift('h2o_nitro')

  if (bundles.length) {
    const micropip = pyodide.globals.get('micropip')
    for (const bundle of bundles) {
      console.log(`Installing bundle ${bundle}...`)
      await micropip.install(bundle)
    }
    micropip.destroy()
  }

  if (files.length) {
    const download = pyodide.globals.get('_nitro_download')
    for (const file of files) {
      console.log(`Fetching file ${file}...`)
      const basename = file.split('/').pop()
      await download(file, basename)
    }
    download.destroy()
  }

  if (autoload) {
    console.log(`Loading packages from imports...`)
    await pyodide.loadPackagesFromImports(program)
  }

  if (entrypoint.length) console.log(`Fetching entrypoint ${entrypoint}...`)
  const app = entrypoint.length
    ? await (await fetch(entrypoint)).text()
    : program

  console.log('Executing program...')
  await pyodide.runPythonAsync([app, launcher].join('\n\n'))

  self.pyodide = pyodide
  self.io = pyodide.globals.get('_nitro_io')

  clearInterval(_poller)
  _poller = setInterval(() => {
    const message = self.io.read()
    if (message) {
      const execute: Command = { t: CommandT.Execute, message }
      self.postMessage(execute)
    }
  }, pollInterval)
}

self.onmessage = async (event) => {
  const c = event.data as Command
  try {
    switch (c.t) {
      case CommandT.Execute:
        self.io.write(c.message)
        break
      case CommandT.LoadProgram:
        {
          await init(c)
          const loaded: Command = { t: CommandT.ProgramLoaded }
          self.postMessage(loaded)
        }
        break
    }
  } catch (error: any) {
    const failed: Command = { t: CommandT.Error, error: error.message }
    self.postMessage(failed)
  }
}
