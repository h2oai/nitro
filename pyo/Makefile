all: build

purge: ## Purge previous build
	rm -rf build dist h2o_nitro.egg-info

.PHONY: build
build: purge clone build-web ## Build wheel
	./venv/bin/python setup.py bdist_wheel

clone:
	mkdir -p h2o_nitro && \
		cp ../py/h2o_nitro/*.py h2o_nitro/ && \
		cd h2o_nitro && \
		sed -e 's/False/True/g' version.py > version.py.tmp && \
		mv version.py.tmp version.py

setup: clean clone setup-web ## Install dependencies
	python3 -m venv venv
	./venv/bin/python -m pip install --upgrade pip
	./venv/bin/python -m pip install -r requirements.txt
	./venv/bin/python -m pip install --editable .

publish: ## Publish wheel
	./venv/bin/python -m twine upload dist/*

clean: purge clean-web ## Clean everything
	rm -rf venv

setup-web:
	cd nitride && npm ci

build-web:
	cd nitride && npm run build

clean-web:
	rm -rf nitride/node_modules

help: ## List all make tasks
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

