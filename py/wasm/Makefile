all: build

setup: clean ## Setup everything
	cd web && $(MAKE) setup

.PHONY: build
build: purge ## Build everything
	cd web && $(MAKE) build
	mkdir -p build dist && \
		cp -R ../../web/build/ . && \
		cd build && \
		rm -f index.html image.png sample.jpg && \
		cp ../web/build/nitride.js . && \
		cp ../examples/* . && \
		mv static/css/main.*.css static/css/main.css && \
		mv static/js/main.*.js static/js/main.js && \
		zip -r ../dist/nitride-$(VERSION).zip *

publish: ## Publish release
	gh release upload v$(VERSION) dist/nitride-$(VERSION).zip --clobber

purge: ## Purge previous build
	rm -rf build dist

clean: purge ## Clean everything
	cd web && $(MAKE) clean

help: ## List all make tasks
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
