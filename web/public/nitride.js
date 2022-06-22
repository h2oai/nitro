
const pollInterval = 100

let _poller = 0;

async function init(runtime, program, autoload) {
  importScripts(runtime);
  self.pyodide = await loadPyodide();
  await self.pyodide.loadPackage(["micropip"]);
  if (autoload) await self.pyodide.loadPackagesFromImports(program);
  await self.pyodide.runPythonAsync(program);
  clearInterval(_poller);
  _poller = setInterval(() => {
    const message = self.pyodide.globals.get('_nitro_io').read();
    if (message) self.postMessage({ t: 1, message });
  }, pollInterval);
}

self.onmessage = async (event) => {
  const c = event.data;
  try {
    switch (c.t) {
      case 1:
        self.pyodide.globals.get('_nitro_io').write(c.message);
        break;
      case 2:
        await init(c.runtime, c.program, c.autoload);
        self.postMessage({ t: 3 });
        break;
    }
  } catch (error) {
    self.postMessage({ t: 0, error: error.message });
  }
}
