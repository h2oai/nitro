# Contributing

## Development

### Getting started

You will need [Node 16+](https://nodejs.org/en/) and [Python 3.7+](https://www.python.org/downloads/).

Clone this repository and install dependencies:

```
git clone https://github.com/h2oai/nitro.git
cd nitro
make setup
```

Build everything:

```
make
```

### Daily development

Most of the time, you'll be editing the front-end sources in `web/` while running the Nitro tour `tour.py` in parallel.
The `tour.py` file is generated from `examples.py`, which is what you'll be editing.

1. Open `web/` in Visual Studio Code.
2. Open `py/` in PyCharm.
3. Auto-rebuild `tour.py` whenever `examples.py` is changed: `echo examples.py | entr make tour`.
4. Run `tour.py` with auto-reload enabled: `FLASK_APP=tour.py FLASK_ENV=development flask run`.
5. Run the front-end with auto-reload enabled: `npm start`.

The project's `README.md` and the guide pages under `docs/` are also generated from `examples.py`, so the above process
will also update the docs simultaneously.

- To preview the project website during development, also run `make serve-docs`, which will run `mkdocs` live.
- To preview `README.md`, you can use Visual Studio Code or PyCharm's markdown preview mode.

Happy hacking!