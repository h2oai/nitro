all: build

setup: ## Set up dependencies
	python3 -m venv venv
	./venv/bin/python -m pip install --upgrade pip
	./venv/bin/python -m pip install wheel
	./venv/bin/python -m pip install -r requirements.txt

build: ## Build docs
	./venv/bin/mkdocs build

serve: ## Launch docs in development mode
	./venv/bin/mkdocs serve

publish: ## Publish docs
	aws s3 sync site s3://nitro.h2o.ai --delete
	aws cloudfront create-invalidation --distribution-id ${AWS_CLOUDFRONT_ID} --paths "/*"

clean:
	rm -rf venv site

help: ## List all make tasks
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

