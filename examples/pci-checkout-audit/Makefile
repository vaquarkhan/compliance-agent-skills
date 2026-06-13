.PHONY: validate audit hash-evidence help

BASELINE := config/baseline.yaml
URL ?= https://example.com
PYTHON ?= python

help:
	@echo "PCI checkout script audit example"
	@echo "  make validate              - Validate baseline YAML structure"
	@echo "  make audit URL=<url>       - Compare live page scripts to baseline"
	@echo "  make audit-discovered IDS= - Compare explicit script IDs to baseline"

validate:
	@$(PYTHON) audit_scripts.py --baseline $(BASELINE)

audit: validate
	@$(PYTHON) audit_scripts.py --baseline $(BASELINE) --url $(URL)

audit-discovered: validate
	@$(PYTHON) audit_scripts.py --baseline $(BASELINE) --discovered $(IDS)
