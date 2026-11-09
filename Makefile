PYTHON ?= python
.PHONY: test demo dataset
test:
	$(PYTHON) -m pytest -q
demo:
	$(PYTHON) -m hash_audit.cli audit app/demo.py
dataset:
	$(PYTHON) -m hash_audit.cli dataset
# Full reproduce target intentionally absent until all experiments are implemented.
