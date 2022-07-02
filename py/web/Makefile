all: build

.PHONY: build
build: purge ## Build wheel
	cp -R ../../web/build h2o_nitro_web/www
	./venv/bin/python setup.py bdist_wheel

setup: clean ## Install dependencies
	python3 -m venv venv
	./venv/bin/python -m pip install --upgrade pip
	./venv/bin/python -m pip install -r requirements.txt
	./venv/bin/python -m pip install --editable .

publish: ## Publish wheel
	./venv/bin/python -m twine upload dist/*

purge: ## Purge previous build
	rm -rf build dist h2o_nitro_web.egg-info h2o_nitro_web/www

clean: purge ## Clean everything
	rm -rf venv

help: ## List all make tasks
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

