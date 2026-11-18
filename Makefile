
PYTHON ?= python

.PHONY: test demo dataset mutations audit-batch benchmark migration reproduce

test:
	$(PYTHON) -m pytest -q

demo:
	$(PYTHON) -m hash_audit.cli audit app/demo.py

dataset:
	$(PYTHON) -m hash_audit.cli dataset --out results/accounts.json

mutations:
	$(PYTHON) -m hash_audit.cli mutations --out data/mutations

audit-batch:
	$(PYTHON) -m hash_audit.cli audit-batch --input data/mutations --out results/mutation_audit.json

benchmark:
	$(PYTHON) -m hash_audit.benchmark_hash

migration:
	$(PYTHON) -m hash_audit.cli migration --out results/migration.json

reproduce: dataset mutations audit-batch benchmark migration test
	@echo Reproduction des experiences terminee.
