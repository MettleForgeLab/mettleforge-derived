# EXAMPLES.md — MettleForge Derived

## 🧭 Purpose

This document provides **concrete examples** of:

* input artifacts (A)
* derived artifacts (A′)
* perception via lenses (DAL, ML)

All examples are minimal and illustrative.

---

## 🜇 Example 1 — Input Claims (A)

```json
[
  {
    "claim_id": "c1",
    "artifact_id": "a1",
    "statement": "The forge preserves structure under load.",
    "normalized_statement": "forge preserves structure under load",
    "anchors": ["forge", "structure"]
  },
  {
    "claim_id": "c2",
    "artifact_id": "a2",
    "statement": "Structure is preserved under load by the forge.",
    "normalized_statement": "structure preserved under load forge",
    "anchors": ["forge", "structure"]
  },
  {
    "claim_id": "c3",
    "artifact_id": "a3",
    "statement": "The system observes without acting.",
    "normalized_statement": "system observes without acting",
    "anchors": ["system"]
  }
]
```

---

## ∞ Example 2 — Derived Output (A′)

Result of running:

```bash
python -m derived.duplicate_candidates_v1 \
  --claims claims.json \
  --out run1.json
```

```json
{
  "type": "DuplicateCandidateSet",
  "schema_version": "v1",
  "non_authoritative": true,
  "lineage": {
    "method": "duplicate_candidates_v1",
    "threshold": 0.7,
    "generated_at": "2026-01-01T00:00:00Z",
    "source_artifact_count": 3
  },
  "candidates": [
    {
      "candidate_id": "a1b2c3d4e5f6a7b8",
      "claim_refs": [
        { "claim_id": "c1", "artifact_id": "a1" },
        { "claim_id": "c2", "artifact_id": "a2" }
      ],
      "similarity_basis": "lexical",
      "similarity_score": 0.83,
      "reasons": [
        "high_token_overlap",
        "shared_normalized_phrase",
        "shared_anchor_text"
      ],
      "component_scores": {
        "token_overlap": 0.75,
        "phrase_overlap": 0.66,
        "anchor_overlap": 1.0,
        "edit_similarity": 0.82
      }
    }
  ]
}
```

---

## 🜇 Example 3 — DAL View (LaForge)

Presentation inside LaForge:

```text
[ CLAIM A ]                          [ CLAIM B ]
----------------------------------   ----------------------------------
The forge preserves structure        Structure is preserved under load
under load.                          by the forge.

----------------------------------   ----------------------------------
DERIVED — NON-AUTHORITATIVE

similarity_score: 0.83

reasons:
- high_token_overlap
- shared_normalized_phrase
- shared_anchor_text

component_scores:
- token_overlap: 0.75
- phrase_overlap: 0.66
- anchor_overlap: 1.0
- edit_similarity: 0.82
```

---

## ∞ Example 4 — Second Run (A′₂)

Later run produces:

```json
{
  "type": "DuplicateCandidateSet",
  "schema_version": "v1",
  "non_authoritative": true,
  "lineage": {
    "method": "duplicate_candidates_v1",
    "threshold": 0.7,
    "generated_at": "2026-01-02T00:00:00Z",
    "source_artifact_count": 3
  },
  "candidates": [
    {
      "candidate_id": "a1b2c3d4e5f6a7b8",
      "claim_refs": [
        { "claim_id": "c1", "artifact_id": "a1" },
        { "claim_id": "c2", "artifact_id": "a2" }
      ],
      "similarity_basis": "lexical",
      "similarity_score": 0.87,
      "reasons": [
        "high_token_overlap",
        "shared_normalized_phrase",
        "shared_anchor_text",
        "low_edit_distance"
      ],
      "component_scores": {
        "token_overlap": 0.80,
        "phrase_overlap": 0.70,
        "anchor_overlap": 1.0,
        "edit_similarity": 0.90
      }
    }
  ]
}
```

---

## 🜇 Example 5 — Multiplicity Lens View (ML)

```json
{
  "type": "MultiplicityLensView",
  "non_authoritative": true,
  "runs": [
    "2026-01-01T00:00:00Z",
    "2026-01-02T00:00:00Z"
  ],
  "run_count": 2,
  "candidates": [
    {
      "candidate_id": "a1b2c3d4e5f6a7b8",
      "claim_refs": [
        { "claim_id": "c1", "artifact_id": "a1" },
        { "claim_id": "c2", "artifact_id": "a2" }
      ],
      "similarity_basis": "lexical",
      "present_in": [
        "2026-01-01T00:00:00Z",
        "2026-01-02T00:00:00Z"
      ],
      "timeline": {
        "2026-01-01T00:00:00Z": {
          "similarity_score": 0.83,
          "reasons": [
            "high_token_overlap",
            "shared_normalized_phrase",
            "shared_anchor_text"
          ]
        },
        "2026-01-02T00:00:00Z": {
          "similarity_score": 0.87,
          "reasons": [
            "high_token_overlap",
            "shared_normalized_phrase",
            "shared_anchor_text",
            "low_edit_distance"
          ]
        }
      },
      "status": "stable"
    }
  ]
}
```

---

## 🧠 What These Examples Show

### 1. Derivation

```text
claims → similarity detection → DuplicateCandidateSet
```

---

### 2. Perception (DAL)

```text
A and A′ displayed side-by-side
no merging
no mutation
```

---

### 3. Temporal Perception (ML)

```text
A′₁ + A′₂ → persistence and drift
```

---

## 🜇 What Does Not Happen

None of these steps:

* rewrite claims
* merge duplicates
* select “best” versions
* suppress alternatives

---

## ∴ One-line Summary

These examples demonstrate how the system can **make similarity visible across space and time without ever turning that visibility into authority**.
