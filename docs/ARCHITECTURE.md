# ARCHITECTURE.md — MettleForge Derived

## 🧭 Overview

MettleForge Derived is a **separate, non-authoritative derivation system** that operates adjacent to the monorepo.

It introduces a new layer into the broader system:

```text
A   = authoritative truth (mettleforge)
A′  = derived artifacts (this repository)
LF  = perception layer (LaForge)
```

The system is intentionally **tri-partite**, with strict separation between:

* truth
* derivation
* perception

---

## 🜇 High-Level Flow

```text
A (truth artifacts)
   ↓
derivation functions
   ↓
A′ (derived artifacts)
   ↓
Derived Artifact Lens (read-only)
   ↓
LaForge (perception only)
```

Key constraint:

```text
A′ never modifies A
A′ is never ingested into LF
```

---

## ∞ Authority Separation

This architecture enforces **separation of powers for meaning**:

| Layer           | Role              | Authority         |
| --------------- | ----------------- | ----------------- |
| A (mettleforge) | Truth system      | authoritative     |
| A′ (derived)    | Derivation system | non-authoritative |
| LF (LaForge)    | Perception system | non-mutating      |

---

## 🧱 Core Components

### 1. Derivation Functions

Located in:

```text
derived/
```

Examples:

* `duplicate_candidates_v1.py`
* future derivations (structural, density, etc.)

These functions:

* read from A
* produce A′
* never modify A

---

### 2. Derived Artifact Schemas

Located in:

```text
schemas/
```

Schemas:

* define structure of A′ artifacts
* enforce validation (fail-closed)
* remain separate from truth schemas

Example:

```text
duplicate_candidate_set.v1.schema.json
```

---

### 3. Derived Artifact Space (DAS)

Physical storage:

```text
/derived/duplicate_candidates/v1/<run_id>.json
```

Properties:

* durable
* deterministic
* diffable
* non-authoritative

DAS is:

```text
not cache
not truth
not runtime memory
```

---

### 4. Validation Layer

All outputs pass through:

```text
generate → validate → write
```

Validation is:

* schema-enforced
* fail-closed
* non-corrective

---

### 5. Perception Layers (Lenses)

#### Derived Artifact Lens (DAL)

* reads A′
* displays A and A′ in parallel
* prevents ingestion

#### Multiplicity Lens (ML)

* compares A′ across time
* reveals persistence, emergence, drift
* produces no new artifacts

---

## 🜇 System Boundaries

### Allowed Flows

```text
A  ──read──▶ A′
LF ──read──▶ A
LF ──read──▶ A′
```

### Forbidden Flows

```text
A′ → A        ❌
A′ → LF       ❌ (implicit)
LF → A′       ❌ (mutation)
```

---

## ∞ Design Principles

### 1. Derivation Without Authority

Derived artifacts must never:

* override truth
* compete with truth
* influence truth

---

### 2. Observation Without Action

Perception layers must:

* reveal structure
* avoid interpretation-as-decision
* remain non-binding

---

### 3. Determinism

All derivation must be:

```text
same input → same output → same bytes
```

---

### 4. Explicitness

All relationships must be:

* explainable
* inspectable
* reproducible

---

### 5. Fail-Closed Structure

Invalid artifacts must:

```text
fail
not repair
not degrade silently
```

---

## 🧠 Relationship to Neighbor Systems

### Relationship to `mettleforge/` (A)

* read-only dependency
* no imports
* no writes
* no structural coupling

### Relationship to LaForge (LF)

* read-only surface
* explicit selection only
* no ingestion into runtime
* no effect on model behavior

---

## 🜇 Evolution Path

This repository may evolve by adding:

* new derivation primitives (A → A′)
* new schemas
* new lenses (A′ → perception)

It must not evolve toward:

* authority
* mutation
* decision-making

---

## ∴ One-line Summary

This architecture enables the system to **observe patterns in truth without ever becoming a system that decides what those patterns mean**.
