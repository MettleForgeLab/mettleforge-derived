# RELATIONSHIPS.md — MettleForge Derived

## 🧭 Purpose

This document describes how the **derived layer (A′)** relates to its neighboring systems:

* the monorepo (`mettleforge/`) — truth
* LaForge — perception and interaction

It defines **what connects**, **what does not**, and **why**.

---

## 🜇 System Topology

```text id="7k4s2m"
mettleforge/            = A   (authoritative truth)
mettleforge-derived/    = A′  (derived artifacts)
LaForge                 = LF  (perception layer)
```

---

## ∞ Relationship Summary

| System          | Relationship to A′ | Direction   | Authority         |
| --------------- | ------------------ | ----------- | ----------------- |
| A (mettleforge) | source of input    | A → A′      | authoritative     |
| A′ (this repo)  | derivation output  | none inward | non-authoritative |
| LF (LaForge)    | read-only observer | LF ← A′     | non-mutating      |

---

## 🧱 Relationship to Truth (A)

### What A′ Does

```text id="6mp8d9"
reads A
derives structure
writes new artifacts
```

### What A′ Does Not Do

```text id="s3l1y0"
modify A        ❌
filter A        ❌
rank A          ❌
replace A       ❌
```

---

### Nature of the Relationship

```text id="q0vtul"
A → A′ is observational, not transformational
```

A′ is a **consequence of A**, not a component of A.

---

### Why This Matters

If A′ were allowed to influence A:

```text id="e9j4ks"
derivation → mutation
```

That would collapse the boundary between:

* truth
* interpretation

---

## 🧠 Relationship to LaForge (LF)

### What LF Does

```text id="6n2vha"
reads A
reads A′ (explicitly)
displays both
```

### What LF Does Not Do

```text id="q4xj8o"
ingest A′ into memory   ❌
feed A′ into models     ❌
bias outputs using A′   ❌
```

---

### Nature of the Relationship

```text id="r1j8pw"
A′ → LF is perceptual, not operational
```

A′ is visible inside LaForge, but **never used as input to behavior**.

---

### Why This Matters

Without this constraint:

```text id="r9lm3u"
perception → influence → mutation
```

The system would silently shift toward authority.

---

## 🜇 Relationship Between A and LF (via A′)

```text id="x6k8m0"
A   ──▶ LF        (normal interaction)
A   ──▶ A′        (derivation)
A′  ──▶ LF        (perception)
```

Crucially:

```text id="n7z3tb"
A′ never feeds back into A
A′ never drives LF behavior
```

---

## ∞ Derived Artifact Space (DAS)

A′ artifacts live in a separate domain:

```text id="g3b9tw"
/derived/
  duplicate_candidates/
    v1/
```

Properties:

* durable
* diffable
* lineage-bearing
* non-authoritative

---

## 🧱 Relationship to Derived Artifact Space

A′ artifacts are:

```text id="u2q4zl"
persistent
inspectable
non-binding
```

They are not:

```text id="y6s1wv"
truth
cache
runtime memory
```

---

## 🧠 Relationship to Time (Multiplicity Lens)

A′ artifacts can be compared across runs:

```text id="m9l2rq"
A′₁, A′₂, A′₃ → ML → temporal perception
```

This reveals:

* persistence
* emergence
* drift

But does not:

* prioritize
* select
* collapse

---

## 🜇 Relationship to Other Derivations (Future)

Future derivations (e.g. density, structural similarity) must:

* operate only on A
* produce new A′ artifacts
* remain independent of existing A′

```text id="q5v8hy"
A′₁ does not depend on A′₂
```

---

## ∞ Separation of Powers

This architecture enforces:

```text id="b2m7ak"
truth        → what is allowed to be true
derivation   → what is allowed to be seen as similar
perception   → what is allowed to be experienced
```

Each system:

* has its own domain
* cannot impersonate the others

---

## 🜇 Failure Conditions (Relationship Breaks)

The system is compromised if any of the following occur:

### A′ influences A

```text id="c6p3rf"
derived artifacts change truth   ❌
```

---

### A′ influences LF behavior

```text id="k8x2dv"
derived artifacts bias outputs   ❌
```

---

### LF mutates A′

```text id="d7z4mn"
runtime edits derived artifacts  ❌
```

---

### Cross-layer coupling

```text id="v3r8as"
shared code paths
implicit dependencies
```

---

## 🧭 Design Intent

This system is intentionally structured so that:

```text id="t4m1ql"
observation does not imply action
```

and:

```text id="r8v6yo"
visibility does not imply authority
```

---

## ∴ One-line Summary

This repository exists **between truth and perception**, allowing the system to observe structure without allowing that observation to become influence.
