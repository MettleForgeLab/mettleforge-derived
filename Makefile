PYTHON ?= python3

DERIVED_DIR := derived
SCHEMA_DIR := schemas
OUTPUT_DIR := derived_output

.PHONY: install
install:
	$(PYTHON) -m pip install -e .

.PHONY: derive-duplicates
derive-duplicates:
ifndef CLAIMS
	$(error CLAIMS is required)
endif
ifndef OUT
	$(error OUT is required)
endif
	$(PYTHON) -m derived.duplicate_candidates_v1 \
		--claims $(CLAIMS) \
		--out $(OUT)

.PHONY: multiplicity
multiplicity:
ifndef RUNS
	$(error RUNS is required)
endif
	$(PYTHON) -c "\
import json; \
from derived.multiplicity_lens_v1 import multiplicity_lens; \
paths = '$(RUNS)'.split(); \
sets = [json.load(open(p)) for p in paths]; \
view = multiplicity_lens(sets); \
print(json.dumps(view, indent=2)) \
"

.PHONY: validate
validate:
ifndef FILE
	$(error FILE is required)
endif
	$(PYTHON) -c "\
import json; \
from jsonschema import Draft7Validator, FormatChecker; \
schema = json.load(open('$(SCHEMA_DIR)/duplicate_candidate_set.v1.schema.json')); \
validator = Draft7Validator(schema, format_checker=FormatChecker()); \
data = json.load(open('$(FILE)')); \
errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path)); \
if errors: \
    print('VALIDATION FAILED:'); \
    [print(f\"- {'/'.join(map(str, e.path)) or '$'}: {e.message}\") for e in errors]; \
    exit(1); \
else: \
    print('VALIDATION OK'); \
"

.PHONY: test
test:
	pytest

.PHONY: clean
clean:
	rm -rf __pycache__ */__pycache__ .pytest_cache