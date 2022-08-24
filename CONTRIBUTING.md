# Contributing

## Development

### Getting started

You will need [Node 16+](https://nodejs.org/en/), [Python 3.7+](https://www.python.org/downloads/) and [entr](https://eradman.com/entrproject/).

Clone this repository and install dependencies:

```
git clone https://github.com/h2oai/nitro.git
cd nitro
make setup
```

Build everything (front-end, wheel, docs):

```
make
```

### Daily development

**Quickstart.** Run any app at `localhost:5000`, then run `make dev-web` and go to https://localhost:3000.

**Long version:**

Most of the time, you'll be editing the front-end sources in `web/` while running a Nitro app in parallel, like the Nitro interactive docs (`docs/docs.py`).
The `docs.py` file is generated from `py/pkg/docs/*.py`, which is what you'll be editing.

1. Open `web/` in Visual Studio Code.
2. Open `py/pkg` in PyCharm. If you're prompted to select an interpreter, use the one in `py/pkg/venv`.
3. Run `make dev-guide` in a new terminal window. This will rebuild `docs.py` whenever `py/pkg/docs/*.py` is changed.
4. Run `make dev-py` in a new terminal window. This will `docs.py` with auto-reload enabled.
5. Run `make dev-web` in a new terminal window. This will automatically launch the front-end at http://localhost:3000 with auto-reload enabled.

In general, as long as the backend is running at http://localhost:5000, the development version of the front-end can interact with it. 
This way, you can always interact with apps at http://localhost:3000, and switch backends at http://localhost:5000.

**Tip.** To preview the project website during development, also run `make serve-docs`, which will run `mkdocs` live.

Happy hacking!
