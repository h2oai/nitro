setup: setup-docs

clean: clean-docs

setup-docs: # Set up docs for development mode
	mkdir -p tools/docs && cd tools/docs && python3 -m venv venv
	./tools/docs/venv/bin/python -m pip install --upgrade pip mkdocs-material

serve-docs: # Launch docs in development mode
	./tools/docs/venv/bin/mkdocs serve

.PHONY: docs
docs: # Build docs
	./tools/docs/venv/bin/mkdocs build

publish-docs: docs ## Publish docs
	aws s3 sync site s3://nitro.h2o.ai --delete

clean-docs:
	rm -rf tools/docs/venv

help: ## List all make tasks
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

