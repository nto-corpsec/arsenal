UV ?= uv

.PHONY: sync fmt lint type test security check

sync:
	$(UV) sync --frozen

fmt:
	$(UV) run ruff format .

lint:
	$(UV) run ruff check .

type:
	$(UV) run mypy src

test:
	$(UV) run pytest --cov=src --cov-report=term-missing

security:
	$(UV) run bandit -q -r src -x tests

check: lint type test security
