.PHONY: fmt
fmt:
	black . && isort .

.PHONY: lint
lint:
	${CMD} ruff check src/

.PHONY: pre-commit
pre-commit:
	${CMD} pre-commit run --all-files

.PHONY: py_tests
py_tests:
	cd python_app && pytest tests/ -v -s