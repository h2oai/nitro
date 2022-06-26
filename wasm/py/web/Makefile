all: build

.PHONY: build
build: ## Build wheel
	npm run build

setup: clean ## Install dependencies
	npm ci

purge: ## Purge previous build
	rm -rf build

clean: purge ## Clean everything
	rm -rf node_modules

help: ## List all make tasks
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

