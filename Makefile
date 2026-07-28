.PHONY: test compile lint typecheck ci run index eval benchmark validate compose-up compose-down

test:
	PYTHONPATH=src python3 -m unittest discover -s tests

compile:
	PYTHONPYCACHEPREFIX=.pycache_tmp python3 -m compileall src tests scripts

lint:
	python3 -m ruff check src tests scripts

typecheck:
	python3 -m mypy src

ci: test compile eval

run:
	uvicorn rag_platform.main:app --reload --app-dir src

index:
	PYTHONPATH=src python3 scripts/build_index.py --docs sample_docs --out local_index.json

eval:
	PYTHONPATH=src python3 scripts/evaluate.py --index local_index.json --cases evals/regression_qa.json

benchmark:
	PYTHONPATH=src python3 scripts/benchmark_chunking.py

validate:
	python3 scripts/validate_runtime.py

compose-up:
	docker compose up --build

compose-down:
	docker compose down
