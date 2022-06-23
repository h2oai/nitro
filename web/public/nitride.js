
const pollInterval = 100

let _poller = 0;

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
`;

const launcher = `
from h2o_nitride import Duplex as _Nitro_IO
_nitro_io = _Nitro_IO()
asyncio.create_task(nitro.serve(_nitro_io.send, _nitro_io.recv))
print('🚀 Nitro launched! 🚀')
print('Please take a moment to ⭐ Nitro on Github: https://github.com/h2oai/nitro')
`

async function init(command) {
  const { runtime, packages, bundles, autoload, files, entrypoint, program } = command;

  console.log(`Loading runtime ${runtime}...`);
  importScripts(runtime);

  console.log('Loading Pyodide...');
  const pyodide = await loadPyodide();

  console.log('Installing micropip...');
  await pyodide.loadPackage(["micropip"]);

  if (packages.length) {
    console.log(`Installing packages ${packages.join(', ')}...`)
    await pyodide.loadPackage(packages);
  }

  console.log('Executing prelude...');
  await pyodide.runPythonAsync(prelude)

  if (bundles.length) {
    const micropip = pyodide.globals.get('micropip');
    for (const bundle of bundles) {
      console.log(`Installing bundle ${bundle}...`)
      await micropip.install(bundle);
    }
    micropip.destroy();
  }

  if (files.length) {
    const download = pyodide.globals.get('_nitro_download');
    for (const file of files) {
      console.log(`Fetching file ${file}...`);
      const basename = file.split('/').pop();
      await download(file, basename);
    }
    download.destroy();
  }

  if (autoload) {
    console.log(`Loading packages from imports...`);
    await pyodide.loadPackagesFromImports(program);
  }

  if (entrypoint.length) console.log(`Fetching entrypoint ${entrypoint}...`);
  const app = entrypoint.length
    ? await (await fetch(entrypoint)).text()
    : program;

  console.log('Executing program...');
  await pyodide.runPythonAsync([app, launcher].join('\n\n'));

  self.pyodide = pyodide;

  clearInterval(_poller);
  _poller = setInterval(() => {
    const message = pyodide.globals.get('_nitro_io').read();
    if (message) self.postMessage({ t: 1, message });
  }, pollInterval);
}

self.onmessage = async (event) => {
  const c = event.data;
  try {
    switch (c.t) {
      case 1:
        {
          self.pyodide.globals.get('_nitro_io').write(c.message);
        }
        break;
      case 2:
        {
          await init(c);
          self.postMessage({ t: 3 });
        }
        break;
    }
  } catch (error) {
    self.postMessage({ t: 0, error: error.message });
  }
}
