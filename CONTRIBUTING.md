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
The `docs.py` file is generated from `py/examples/*.py`, which is what you'll be editing.

1. Open `web/` in Visual Studio Code.
2. Open `py/` in PyCharm. If you're prompted to select an interpreter, use the one in `py/venv`.
3. Auto-rebuild `docs.py` whenever `examples.py` is changed: `make dev-docs`.
4. Run `docs.py` with auto-reload enabled: run `make dev-py`.
5. Run the front-end with auto-reload enabled: `make dev-web`. This will automatically launch the front-end at https://localhost:3000.

The project's `README.md` and the guide pages under `docs/` are also generated from `examples.py`, so the above process
will also update the docs simultaneously.


**Tip.** To preview the project website during development, also run `make serve-docs`, which will run `mkdocs` live.

Happy hacking!
