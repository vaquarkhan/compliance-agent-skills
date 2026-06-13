.PHONY: validate validate-sme lint typecheck security coverage test test-unit smoke demo install lock sync-version pre-commit report

PYTHON ?= python
INPUT ?= templates/reports/regulatory-findings-report.yaml
OUTPUT ?= findings-report.md

validate:
	$(PYTHON) scripts/smoke_syntax.py
	$(PYTHON) scripts/validate-skills.py
	$(PYTHON) scripts/validate-assets.py
	$(PYTHON) scripts/validate-plugin-manifest.py
	$(PYTHON) scripts/validate-evidence-manifest.py
	$(PYTHON) scripts/sync-install-manifest.py

validate-sme:
	$(PYTHON) scripts/validate-sme-provenance.py

lint:
	ruff check agent.py redaction.py scripts/ compliance_tests/
	ruff format --check agent.py redaction.py scripts/ compliance_tests/

typecheck:
	mypy agent.py redaction.py scripts/

security:
	pip-audit -r requirements-lock.txt --strict --desc on
	bandit -r agent.py redaction.py scripts/ -c pyproject.toml
	detect-secrets scan --baseline .secrets.baseline .

coverage: test

test:
	$(PYTHON) -m pytest compliance_tests/ -v

test-unit:
	$(PYTHON) -m pytest compliance_tests/test_deanonymize_unit.py -v

smoke:
	$(PYTHON) scripts/smoke_syntax.py

demo:
	$(PYTHON) scripts/demo_agent.py

install:
	$(PYTHON) -m pip install -r requirements-lock.txt -r requirements-dev.txt

lock:
	$(PYTHON) scripts/compile-requirements.py

pre-commit:
	pre-commit run --all-files

sync-version:
	$(PYTHON) scripts/sync-version.py

report:
	$(PYTHON) scripts/generate-regulatory-report.py $(INPUT) -o $(OUTPUT)
