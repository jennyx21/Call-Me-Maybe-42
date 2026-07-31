
export UV_CACHE_DIR=/goinfre/$USER/uv-cache uv sync
export HF_HOME=/goinfre/$USER/huggingface

install:
	uv sync
	uv sync --project llm_sdk

run: 
	uv run python -m src

lint:
	uv run flake8 src --exclude .venv\
			--exclude llm_sdk\
			--exclude moulinette
	uv run mypy . --exclude llm_sdk\
		--exclude moulinette\
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict: 
	flake8 . --exclude llm_sdk
	mypy . --exclude llm_sdk\
		--strict