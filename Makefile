all: build

setup: clean setup-web setup-py setup-screenshots setup-docs ## Install dependencies

build: web py docs ## Build everything

clean: clean-docs clean-screenshots clean-py clean-web ## Clean everything

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

.PHONY: py
py: ## Build Python
	cd py/web && $(MAKE) build
	cd py/pkg && $(MAKE) build
	cd py/wasm && $(MAKE) build

clean-py: ## Clean Python dependencies
	cd py/web && $(MAKE) clean
	cd py/pkg && $(MAKE) clean
	cd py/wasm && $(MAKE) clean

setup-docs: ## Set up docs for development mode
	mkdir -p tools/docs && cd tools/docs && python3 -m venv venv
	cd tools/docs && ./venv/bin/python -m pip install --upgrade pip
	cd tools/docs && ./venv/bin/python -m pip install -r requirements.txt

.PHONY: docs
docs: docs-py ## Build docs
	cd py/pkg && $(MAKE) docs
	./tools/docs/venv/bin/mkdocs build

clean-docs: ## Clean docs
	rm -rf tools/docs/venv

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
	./tools/docs/venv/bin/mkdocs serve

release: # Tag and release on Github
	git tag v$(VERSION)
	git push origin && git push origin --tags
	cd cli && goreleaser release --rm-dist

publish-py: ## Publish wheel to PyPI
	cd py/web && $(MAKE) publish
	cd py/pkg && $(MAKE) publish
	cd py/wasm && $(MAKE) publish

publish-docs: docs ## Publish docs
	aws s3 sync site s3://nitro.h2o.ai --delete
	aws cloudfront create-invalidation --distribution-id ${AWS_CLOUDFRONT_ID} --paths "/*"

dev-web: # Launch front-end in development mode
	cd web && npm start

dev-py: # Launch backend in development mode
	cd py/pkg && FLASK_APP=../docs/docs.py FLASK_ENV=development ./venv/bin/flask run

dev-docs: # Rebuild docs.py when examples.py is changed
	cd py/pkg && find docs | entr $(MAKE) docs

docs-py: # Rebuild docs.py from examples.py
	cd py/pkg && $(MAKE) docs

help: ## List all make tasks
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

