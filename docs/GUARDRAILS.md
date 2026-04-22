# GUARDRAILS.md — MettleForge Derived

## 🧭 Purpose

This document defines the **hard enforcement rules** that keep the derived layer (A′) from drifting into authority.

These are not guidelines.
They are **structural guardrails**.

If they are weakened, the system will collapse:

```text
derivation → influence → mutation
```

---

## 🜇 Core Invariant

> **Derived artifacts must never gain authority over truth artifacts.**

Everything in this document enforces that single rule.

---

## ∞ System Context

```text id="b7nq2y"
mettleforge/            = A   (authoritative truth)
mettleforge-derived/    = A′  (this repository)
LaForge                 = LF  (read-only perception)
```

Allowed:

```text id="x7h9yo"
A  ──read──▶ A′
LF ──read──▶ A
LF ──read──▶ A′
```

Forbidden:

```text id="s0h7e2"
A′ → A        ❌
A′ → LF       ❌ (implicit ingestion)
LF → A′       ❌ (mutation)
```

---

## 🧱 Guardrail Categories

### 1. Path Isolation

Derived artifacts must never be written into monorepo paths.

**Rule:**

```python id="z6m8c2"
assert not output_path.startswith("/mettleforge/")
```

**Why:**

Prevents accidental mutation of truth artifacts.

---

### 2. Repository Separation

Derived code must not import monorepo packages.

**Forbidden:**

```text id="l3t4wr"
packages.datadiddler
packages.forgeos
packages.dadi
packages.nemoclaw
```

**Why:**

Prevents coupling that can reintroduce authority or hidden influence.

---

### 3. Schema Enforcement (Fail-Closed)

All derived artifacts must pass schema validation before write.

**Rule:**

```text id="p9f0vt"
generate → validate → write
```

**Never:**

```text id="u2l6xa"
generate → fix → write   ❌
```

**Why:**

Repair introduces hidden interpretation.

---

### 4. Non-Authoritative Flag (Mandatory)

All derived artifacts must declare:

```json id="t4q2sv"
"non_authoritative": true
```

**Why:**

Prevents ambiguity in downstream systems.

---

### 5. Determinism

Derived artifacts must be byte-stable.

**Rule:**

```text id="v8y3je"
same input → same output → same bytes
```

Implementation requirements:

* deterministic IDs
* sorted JSON keys
* no randomness

**Why:**

Ensures reproducibility and auditability.

---

### 6. No Backflow

Derived artifacts must never influence A.

**Prohibited behaviors:**

* writing into A
* modifying A
* filtering A
* ranking A

**Why:**

Backflow converts derivation into mutation.

---

### 7. No Runtime Ingestion

LaForge must treat A′ as view-only.

**Forbidden:**

* feeding A′ into model prompts
* storing A′ in runtime memory
* using A′ to bias outputs

**Allowed:**

* explicit display
* explicit comparison

**Why:**

Prevents perception from becoming influence.

---

### 8. Closed Reason Vocabulary

All derivations must use a **closed set of explanations**.

Example:

```text id="m1s8eq"
high_token_overlap
shared_normalized_phrase
shared_anchor_text
low_edit_distance
```

**Why:**

Prevents silent expansion of interpretive logic.

---

### 9. No Ranking or Selection

Derived artifacts must not:

* rank candidates
* choose preferred results
* suppress alternatives

**Why:**

Selection introduces authority.

---

### 10. No Merge or Canonicalization

Derived artifacts must not:

* merge claims
* create canonical forms
* collapse duplicates

**Why:**

Collapse is mutation disguised as interpretation.

---

### 11. Explicit Execution Only

Derivation must be manually or explicitly invoked.

**Forbidden:**

* automatic pipeline execution
* CI-triggered artifact generation
* background jobs

**Why:**

Prevents silent accumulation of influence.

---

### 12. Separate Schema Domain

Derived schemas must remain separate from truth schemas.

```text id="u6b4fn"
mettleforge/            → truth schemas
mettleforge-derived/    → derived schemas
```

**Why:**

Prevents schema-level authority confusion.

---

## 🧠 Failure Modes (What to Watch For)

### Drift Toward Authority

Symptoms:

* “helpful” ranking
* hidden prioritization
* implicit filtering

---

### Silent Coupling

Symptoms:

* imports from monorepo
* shared utilities creeping in
* cross-repo dependencies

---

### Interpretation Creep

Symptoms:

* expanding reason vocabulary
* opaque scoring logic
* embedding-based shortcuts without explanation

---

### Pipeline Infiltration

Symptoms:

* derivation triggered during build
* artifacts appearing without explicit invocation

---

## 🜇 Enforcement Strategy

Guardrails must be:

```text id="w4g3rf"
structural
not behavioral
```

Meaning:

* enforced by code, not discipline
* enforced by repo layout, not convention
* enforced by validation, not intention

---

## ∴ One-line Summary

These guardrails ensure the system can **see more without ever gaining the power to decide**.
