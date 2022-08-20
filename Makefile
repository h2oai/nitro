.EXPORT_ALL_VARIABLES:
VERSION:=$(shell cat VERSION)

all: build

version:
	echo "__version__ = \"${VERSION}\"" > py/pkg/h2o_nitro/version.py
	echo "__version__ = \"${VERSION}\"" > py/web/h2o_nitro_web/version.py

setup: clean version setup-web setup-py setup-screenshots setup-docs ## Install dependencies

build: version web py docs ## Build everything

clean: clean-docs clean-screenshots clean-py clean-web ## Clean everything
	rm -f py/pkg/h2o_nitro/version.py
	rm -f py/web/h2o_nitro_web/version.py

setup-web: ## Install dependencies for web
	cd web && npm ci

.PHONY: web
web: ## Build web
	cd web && npm run build

clean-web: ## Clean web dependencies
	cd web && rm -rf build node_modules

setup-py: ## Install dependencies for Python
	cd py/web && $(MAKE) setup
	cd py/pkg && $(MAKE) setup
	cd py/wasm && $(MAKE) setup
	cd py/examples && $(MAKE) setup

.PHONY: py
py: ## Build Python
	cd py/web && $(MAKE) build
	cd py/pkg && $(MAKE) build
	cd py/wasm && $(MAKE) build

clean-py: ## Clean Python dependencies
	cd py/web && $(MAKE) clean
	cd py/pkg && $(MAKE) clean
	cd py/wasm && $(MAKE) clean
	cd py/examples && $(MAKE) clean

setup-docs: ## Set up docs for development mode
	cd help && $(MAKE) setup

.PHONY: docs
docs: guide ## Build docs
	cd help && $(MAKE) build

guide: # Build guide pages
	cd py/pkg && $(MAKE) docs

clean-docs: ## Clean docs
	cd help && $(MAKE) clean

setup-screenshots: # Set up screenshot automation tooling
	mkdir -p tools/screenshots && cd tools/screenshots && python3 -m venv venv
	cd tools/screenshots && ./venv/bin/python -m pip install --upgrade pip
	cd tools/screenshots && ./venv/bin/python -m pip install -r requirements.txt
	cd tools/screenshots && ./venv/bin/playwright install

screenshots: # Capture screenshots for docs
	./tools/screenshots/venv/bin/python tools/screenshots/screenshot.py

clean-screenshots: # Clean screenshot automation tooling
	rm -rf tools/screenshots/venv

serve-docs: # Launch docs in development mode
	cd help && $(MAKE) serve

publish: publish-tag publish-cli publish-py # Publish everything

publish-tag: # Push tags to origin
	git tag v$(VERSION)
	git push origin && git push origin --tags

publish-cli: # Publish CLI
	cd cli && goreleaser release --rm-dist

publish-py: ## Publish wheel to PyPI
	cd py/web && $(MAKE) publish
	cd py/pkg && $(MAKE) publish
	cd py/wasm && $(MAKE) publish

publish-docs: docs ## Publish docs
	cd help && $(MAKE) publish

dev-web: # Launch front-end in development mode
	cd web && npm start

dev-py: # Launch backend in development mode
	cd py/pkg && FLASK_APP=../../docs/docs.py FLASK_ENV=development ./venv/bin/flask run

dev-guide: # Rebuild guide pages when pkg/docs is changed
	cd py/pkg && find docs | entr $(MAKE) docs

help: ## List all make tasks
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

