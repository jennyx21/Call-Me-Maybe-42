

export UV_CACHE_DIR=/goinfre/$USER/uv-cache uv sync
export HF_HOME=/goinfre/$USER/huggingface

install:
	uv sync

run: 
	uv run pyhton src/main.py

lint:
	flake8 . --exclude llm_sdk
	mypy . --exclude llm_sdk\
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict: 
	flake8 . --exclude llm_sdk
	mypy . --exclude llm_sdk\
		--strict