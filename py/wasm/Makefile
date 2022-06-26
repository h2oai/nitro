all: build

setup: clean ## Setup everything
	cd py && $(MAKE) setup
	cd web && $(MAKE) setup

.PHONY: build
build: purge ## Build everything
	cd py && $(MAKE) build
	cd web && $(MAKE) build
	mkdir -p build dist && \
		cp -R ../../web/build/ . && \
		cd build && \
		rm -f index.html image.png sample.jpg && \
		cp ../web/build/nitride.js . && \
		cp ../examples/* . && \
		mv static/css/main.*.css static/css/main.css && \
		mv static/js/main.*.js static/js/main.js && \
		zip -r ../dist/nitride-v$(VERSION).zip *

purge: ## Purge previous build
	rm -rf build dist

clean: purge ## Clean everything
	cd py && $(MAKE) clean
	cd web && $(MAKE) clean

publish: ## Publish
	cd py && $(MAKE) publish

help: ## List all make tasks
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
