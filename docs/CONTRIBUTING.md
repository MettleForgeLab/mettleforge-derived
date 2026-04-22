# CONTRIBUTING.md — MettleForge Derived

## 🧭 Purpose

This repository is not a general software project.

It is a **bounded derivation layer** with strict constraints on behavior, authority, and interaction with neighboring systems.

Contributions are welcome—but only if they **preserve the system’s invariants**.

---

## 🜇 System Context

```text
mettleforge/            = A   (authoritative truth)
mettleforge-derived/    = A′  (this repo — derivation)
LaForge                 = LF  (read-only perception)
```

This repo exists **adjacent to**, not inside, the monorepo.

It must never become:

* part of the truth system
* part of runtime execution
* a source of authority

---

## ∞ Core Rule

> **This repository may derive. It may not decide.**

---

## 🧱 What Contributions Are Allowed

You may:

* add new **derivation functions** (A → A′)
* add new **schemas** for derived artifacts
* add new **perception lenses** (read-only views over A′)
* improve **determinism, clarity, or explainability**
* add tests and validation logic

All additions must remain:

```text
non-authoritative
deterministic
explicit
```

---

## 🚫 What Is Not Allowed

Do **not** introduce:

* mutation of source artifacts (A)
* write paths into the monorepo
* ranking, filtering, or prioritization logic
* “best result” selection
* merging or canonicalization
* implicit inference or hidden scoring
* runtime integration with LaForge
* automatic execution in pipelines or CI

If your change answers:

```text
“which one should we use?”
```

It does not belong here.

---

## 🜇 Boundary Rules (must hold)

### 1. No Backflow

```text
A′ → A   ❌
```

Derived artifacts must never modify or influence truth artifacts.

---

### 2. No Runtime Ingestion

```text
A′ → LF (implicit)   ❌
```

LaForge may read A′ only through explicit, read-only selection.

---

### 3. No Hidden Authority

All derivations must:

* expose reasoning (no black-box logic)
* use closed vocabularies where defined
* remain inspectable

---

### 4. No Coupling

Do not import or depend on:

```text
packages.datadiddler
packages.forgeos
packages.dadi
packages.nemoclaw
```

This repo must remain **structurally independent**.

---

## 🧠 Design Principles

### Determinism

Same input must produce:

```text
same output
same structure
same bytes
```

---

### Explicitness

If the system cannot explain:

```text
why two things are related
```

it must not claim that they are.

---

### Non-Authority

All outputs must clearly indicate:

```text
non_authoritative = true
```

---

### Fail-Closed Structure

* invalid artifacts must be rejected
* no auto-repair
* no silent correction

---

## 🧪 Testing Expectations

All new derivation logic should include:

* deterministic output tests
* schema validation tests
* edge case coverage (empty input, minimal overlap, etc.)

---

## 🧭 How to Add a New Derivation

1. Define the **function** (A → A′)
2. Define the **artifact schema**
3. Enforce validation (fail-closed)
4. Ensure deterministic output
5. Ensure no mutation paths exist
6. Document clearly

---

## 🜇 How to Add a New Lens

Lenses must:

* operate only on A′
* produce no persistent output
* introduce no interpretation beyond observation
* remain non-authoritative

---

## ∴ One-line Summary

Contribute only if your change **increases visibility without increasing authority**.
