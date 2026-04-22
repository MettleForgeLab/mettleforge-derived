# USAGE.md — MettleForge Derived

## 🧭 Purpose

This document describes how to **use the derived layer (A′)** safely and correctly.

It focuses on:

* how to generate derived artifacts
* how to store them
* how to read them through LaForge
* what *not* to do

---

## 🜇 System Context

```text id="cs3jzn"
mettleforge/            = A   (authoritative truth)
mettleforge-derived/    = A′  (this repository)
LaForge                 = LF  (perception layer)
```

Flow:

```text id="d7n52r"
A  ──read──▶ A′
LF ──read──▶ A
LF ──read──▶ A′
```

---

## ∞ Basic Workflow

### Step 1 — Obtain Source Artifacts (A)

Provide a claims artifact from the monorepo.

Example:

```text id="h4qj1p"
claims.ndjson
```

Each record should include:

* `claim_id`
* `artifact_id`
* `statement`
* `normalized_statement`
* optional `anchors`

---

### Step 2 — Run Derivation

Execute explicitly (never automatically):

```bash id="s8gk0f"
python -m derived.duplicate_candidates_v1 \
  --claims path/to/claims.ndjson \
  --out /derived/duplicate_candidates/v1/<run_id>.json
```

---

### Step 3 — Validate + Write

The derivation pipeline enforces:

```text id="j7k4ld"
generate → validate → write
```

If validation fails:

```text id="k1p8xh"
artifact is rejected
```

No partial writes. No repair.

---

### Step 4 — Store in Derived Artifact Space

Output must be written to:

```text id="z3v9mb"
/derived/duplicate_candidates/v1/
```

Naming convention (recommended):

```text id="u5m8ps"
<artifact_sha>_<tool_sha>.json
```

---

### Step 5 — View via LaForge (DAL)

In LaForge:

* explicitly select a derived artifact
* view it alongside source claims

Presentation rules:

```text id="x9r2lf"
A (original)      |  A′ (derived)
------------------|------------------
unchanged         | annotated
authoritative     | NON-AUTHORITATIVE
```

---

### Step 6 — Use Multiplicity Lens (ML)

To compare multiple runs:

```text id="t2v6ae"
A′₁, A′₂, A′₃ → multiplicity_lens_v1
```

Reveals:

* persistence
* emergence
* disappearance
* explanation drift

Does not:

* select
* rank
* collapse

---

## 🜇 What You Can Do

You may:

* inspect similarity candidates
* compare claims across runs
* observe recurring patterns
* examine explanation changes

---

## 🚫 What You Must Not Do

Do not:

* treat A′ as truth
* merge or rewrite claims based on A′
* filter A using A′
* feed A′ into models
* use A′ to bias decisions

---

## 🧠 Interpretation Guidance

Derived artifacts say:

```text id="n4p2sv"
"these may be similar"
```

They do not say:

```text id="d8j7xt"
"these are the same"
"this one is better"
"this should replace that"
```

---

## 🜇 Mental Model

Think of A′ as:

```text id="k7w5rf"
a map of pressure, not a map of truth
```

---

## ∞ Determinism Expectations

Running the same derivation twice must produce:

```text id="g3s9jm"
identical files
```

If not:

* check input consistency
* check normalization
* check tool version

---

## 🧱 Error Handling

If validation fails:

* inspect schema errors
* fix input or derivation logic
* rerun

Never:

```text id="r2n8lf"
patch output manually
```

---

## 🜇 Adding New Derivations (Preview)

Future tools should follow:

```text id="z5m1ra"
A → A′
schema → validation → deterministic write
```

---

## ∴ One-line Summary

Use this system to **see patterns in truth artifacts without ever letting those patterns change the truth**.
