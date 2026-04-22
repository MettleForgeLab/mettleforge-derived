# Makefile — MettleForge Derived

## 🧭 Purpose

This Makefile provides **explicit, manual entrypoints** for working with the derived layer.

It does **not** automate pipelines.
It does **not** run implicitly.

All targets are:

```text
manual
transparent
non-authoritative
```

---

## 🧱 Makefile

```makefile
PYTHON ?= python3

DERIVED_DIR := derived
SCHEMA_DIR := schemas
OUTPUT_DIR := derived_output

# ----------------------------
# Setup
# ----------------------------

.PHONY: install
install:
	$(PYTHON) -m pip install -e .

# ----------------------------
# Derivation
# ----------------------------

# Usage:
# make derive-duplicates CLAIMS=path/to/claims.json OUT=path/to/output.json

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

# ----------------------------
# Multiplicity Lens (view only)
# ----------------------------

# Usage:
# make multiplicity RUNS="run1.json run2.json"

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

# ----------------------------
# Validation
# ----------------------------

# Usage:
# make validate FILE=path/to/file.json

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

# ----------------------------
# Testing
# ----------------------------

.PHONY: test
test:
	pytest

# ----------------------------
# Clean
# ----------------------------

.PHONY: clean
clean:
	rm -rf __pycache__ */__pycache__ .pytest_cache

```

---

## 🜇 Design Constraints

This Makefile intentionally avoids:

* automatic execution
* pipeline hooks
* CI coupling
* hidden dependencies

Every command must be:

```text
explicitly invoked
fully visible
fully controllable
```

---

## ∞ Example Usage

### Derive candidates

```bash
make derive-duplicates \
  CLAIMS=data/claims.json \
  OUT=derived/duplicate_candidates/v1/run.json
```

---

### Validate artifact

```bash
make validate FILE=derived/duplicate_candidates/v1/run.json
```

---

### View temporal lens

```bash
make multiplicity RUNS="run1.json run2.json"
```

---

## ∴ One-line Summary

This Makefile provides **manual, transparent entrypoints** into the derived layer—never automation, never authority.
