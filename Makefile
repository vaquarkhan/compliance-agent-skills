.PHONY: validate test smoke demo install sync-version

PYTHON ?= python

validate:
	$(PYTHON) scripts/smoke_syntax.py
	$(PYTHON) scripts/validate-skills.py
	$(PYTHON) scripts/validate-assets.py
	$(PYTHON) scripts/validate-plugin-manifest.py
	$(PYTHON) scripts/validate-evidence-manifest.py
	$(PYTHON) scripts/sync-install-manifest.py

test:
	$(PYTHON) -m pytest compliance_tests/ -v

test-unit:
	$(PYTHON) -m pytest compliance_tests/test_deanonymize_unit.py -v

smoke:
	$(PYTHON) scripts/smoke_syntax.py

demo:
	$(PYTHON) scripts/demo_agent.py

install:
	$(PYTHON) -m pip install -r requirements.txt -r requirements-dev.txt

sync-version:
	$(PYTHON) scripts/sync-version.py
