all: build

purge: ## Purge previous build
	rm -rf build dist h2o_nitro.egg-info h2o_nitro/www

.PHONY: build
build: purge docs ## Build wheel and docs
	rm -rf h2o_nitro/www && cp -r ../web/build h2o_nitro/www
	./venv/bin/python setup.py bdist_wheel

setup: clean ## Install dependencies
	python3 -m venv venv
	./venv/bin/python -m pip install --upgrade pip
	./venv/bin/python -m pip install -r requirements.txt
	./venv/bin/python -m pip install --editable .

.PHONY: docs
docs: ## Compile examples into readme, docs and tour
	./venv/bin/python make.py

publish: ## Publish wheel
	./venv/bin/python -m twine upload dist/*

clean: purge ## Clean everything
	rm -rf venv

help: ## List all make tasks
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

