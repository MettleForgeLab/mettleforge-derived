# TESTING.md — MettleForge Derived

## 🧭 Purpose

This document defines how to test the derived layer (A′).

Testing here is not about performance or coverage first.

It is about enforcing **invariants**:

```text
determinism
schema compliance
non-authority
boundary integrity
```

---

## 🜇 Core Principle

> **If a test cannot prove the system is not drifting toward authority, it is insufficient.**

---

## ∞ Test Categories

### 1. Determinism Tests

### Goal

Ensure:

```text
same input → same output → same bytes
```

### Example

```python id="determinism-test"
from derived.duplicate_candidates_v1 import detect_duplicate_candidates
import json

def test_determinism():
    claims = [...]  # fixed input

    result1 = detect_duplicate_candidates(claims)
    result2 = detect_duplicate_candidates(claims)

    assert json.dumps(result1, sort_keys=True) == json.dumps(result2, sort_keys=True)
```

---

## 🧱 2. Schema Validation Tests

### Goal

Ensure all outputs:

```text
must pass schema
must fail if invalid
```

### Example

```python id="schema-test"
from jsonschema import Draft7Validator
import json

def test_schema_valid():
    with open("schemas/duplicate_candidate_set.v1.schema.json") as f:
        schema = json.load(f)

    validator = Draft7Validator(schema)

    result = detect_duplicate_candidates([...])

    errors = list(validator.iter_errors(result))
    assert not errors
```

---

### Negative Case

```python id="schema-fail-test"
def test_schema_rejects_invalid():
    invalid = {
        "type": "DuplicateCandidateSet",
        "schema_version": "v1"
        # missing required fields
    }

    errors = list(validator.iter_errors(invalid))
    assert errors
```

---

## 🜇 3. Non-Authority Tests

### Goal

Ensure no output suggests:

```text
selection
ranking
collapse
decision
```

### Example

```python id="non-authority-test"
def test_no_authority_fields():
    result = detect_duplicate_candidates([...])

    for c in result["candidates"]:
        assert "rank" not in c
        assert "priority" not in c
        assert "selected" not in c
        assert "canonical" not in c
```

---

## ∞ 4. Closed Vocabulary Tests

### Goal

Ensure reasons never drift beyond allowed set.

### Example

```python id="reason-test"
ALLOWED = {
    "high_token_overlap",
    "shared_normalized_phrase",
    "shared_anchor_text",
    "low_edit_distance",
}

def test_reason_vocab():
    result = detect_duplicate_candidates([...])

    for c in result["candidates"]:
        for r in c["reasons"]:
            assert r in ALLOWED
```

---

## 🧱 5. Multiplicity Lens Tests

### Goal

Ensure temporal logic is correct and stable.

### Example

```python id="multiplicity-test"
from derived.multiplicity_lens_v1 import multiplicity_lens

def test_multiplicity_stable():
    sets = [run1, run2]

    view = multiplicity_lens(sets)

    for c in view["candidates"]:
        if len(c["present_in"]) == len(view["runs"]):
            assert c["status"] == "stable"
```

---

### Duplicate Time Guard

```python id="time-guard-test"
def test_duplicate_time_rejected():
    with pytest.raises(ValueError):
        multiplicity_lens([run1, run1])  # same timestamp
```

---

## 🜇 6. Byte Stability Tests

### Goal

Ensure output is byte-identical across runs.

### Example

```python id="byte-test"
def test_byte_stability(tmp_path):
    result = detect_duplicate_candidates([...])

    path1 = tmp_path / "a.json"
    path2 = tmp_path / "b.json"

    write(result, path1)
    write(result, path2)

    assert path1.read_bytes() == path2.read_bytes()
```

---

## ∞ 7. Boundary Tests

### Goal

Ensure no coupling or path violations.

### Example

```python id="boundary-test"
def test_no_monorepo_imports():
    import inspect
    import derived.duplicate_candidates_v1 as mod

    src = inspect.getsource(mod)

    assert "mettleforge" not in src
```

---

## 🜇 8. Minimal Input Tests

### Goal

Ensure system behaves safely with edge inputs.

### Cases

* empty input
* single claim
* no overlap
* identical claims

### Example

```python id="edge-test"
def test_empty_input():
    result = detect_duplicate_candidates([])
    assert result["candidates"] == []
```

---

## 🧠 Testing Philosophy

Tests should verify:

```text
the system does not gain power
```

not just:

```text
the system produces correct output
```

---

## 🚫 Anti-Patterns in Testing

Do not:

* assert “best match”
* validate ranking quality
* test semantic correctness
* introduce subjective evaluation

These belong outside this system.

---

## 🜇 Test Execution

Run tests explicitly:

```bash id="run-tests"
pytest
```

No CI auto-trigger for derivation runs.

---

## ∴ One-line Summary

Tests exist to ensure the system **remains a system that can see without deciding**, not to improve what it sees.
