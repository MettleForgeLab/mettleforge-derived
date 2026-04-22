import json
import hashlib
from derived.duplicate_candidates_v1 import detect_duplicate_candidates
from jsonschema import Draft7Validator

SCHEMA_PATH = "schemas/duplicate_candidate_set.v1.schema.json"


def load_schema():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_sample_claims():
    claims = []
    with open("examples/sample_claims.ndjson", "r", encoding="utf-8") as f:
        for line in f:
            claims.append(json.loads(line))
    return claims


# ----------------------------
# Import test
# ----------------------------


def test_import():
    assert detect_duplicate_candidates is not None


# ----------------------------
# Determinism test
# ----------------------------


def test_determinism():
    claims = load_sample_claims()

    result1 = detect_duplicate_candidates(claims)
    result2 = detect_duplicate_candidates(claims)

    assert json.dumps(result1, sort_keys=True) == json.dumps(result2, sort_keys=True)


# ----------------------------
# Schema validation test
# ----------------------------


def test_schema_validation():
    claims = load_sample_claims()
    result = detect_duplicate_candidates(claims)

    schema = load_schema()
    validator = Draft7Validator(schema)

    errors = list(validator.iter_errors(result))
    assert not errors, f"Schema validation failed: {errors}"


# ----------------------------
# Non-authoritative check
# ----------------------------


def test_non_authoritative_flag():
    claims = load_sample_claims()
    result = detect_duplicate_candidates(claims)

    assert result.get("non_authoritative") is True
