setup: setup-docs

clean: clean-docs

setup-docs:
	mkdir -p tools/docs && cd tools/docs && python3 -m venv venv
	./tools/docs/venv/bin/python -m pip install --upgrade pip mkdocs-material

serve-docs:
	./tools/docs/venv/bin/mkdocs serve

.PHONY: docs
docs:
	./tools/docs/venv/bin/mkdocs build

clean-docs:
	rm -rf tools/docs/venv

help: ## List all make tasks
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

