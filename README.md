# MettleForge Derived



Derived artifact layer (A′).



Produces \*\*non-authoritative artifacts\*\* from monorepo truth (A).



---



## 🧭 Purpose



This repository implements a \*\*post-artifact observational layer\*\*.



It exists to:



* derive structural signals from truth artifacts

* make those signals visible

* preserve separation between \*\*truth, derivation, and interpretation\*\*



It does \*\*not\*\*:



* modify source artifacts

* participate in runtime execution

* introduce authority over A



---



## 🜇 System Placement



```text

mettleforge/            = A   (authoritative truth)

mettleforge-derived/    = A′  (derived artifacts)

LaForge                 = LF  (read-only perception)

```



Flow:



```text

A  ──read──▶ A′

LF ──read──▶ A′

```



There is \*\*no path\*\*:



```text

A′ → A

A′ → LF (ingestion)

```



---



## ∞ Core Properties



* deterministic (same input → same output → same bytes)

* schema-constrained (fail-closed validation)

* non-authoritative (explicitly marked)

* read-only relationship to A

* no mutation, no repair, no inference



---



## 🧱 Current Capabilities (v1)



### Duplicate Candidate Detection



Detects near-duplicate claims using \*\*lexical overlap\*\*.



Produces:



```text

DuplicateCandidateSet

```



Each candidate:



* pairwise (claim-to-claim)

* explainable (explicit reasons)

* non-authoritative

* deterministic identity



---



### Multiplicity Lens (view only)



Compares multiple derived artifacts over time.



Reveals:



* persistence of similarity

* emergence and disappearance

* shifts in explanation



Does not create new artifacts.



---



## 📁 Repository Structure



```text

derived/

&#x20; duplicate\_candidates\_v1.py

&#x20; multiplicity\_lens\_v1.py



schemas/

&#x20; duplicate\_candidate\_set.v1.schema.json

```



---



## 🧠 Conceptual Model



This layer introduces \*\*derivation without authority\*\*.



It allows the system to:



```text

observe structure

without rewriting structure

```



It is not:



* a correction system

* a ranking system

* a decision system



---



## ⚠️ Constraints (must hold)



This repository must never:



* write to `mettleforge/`

* import monorepo packages

* run inside core pipelines or services

* influence runtime behavior of LaForge

* treat derived artifacts as authoritative



---



\## 🧭 Execution



Run explicitly, never implicitly:



```bash

python -m derived.duplicate\_candidates\_v1 \\

&#x20; --claims <artifact\_path> \\

&#x20; --out <derived\_path>

```



---



\## 🜇 Artifact Discipline



All outputs:



* must pass schema validation

* must be byte-stable

* must include lineage

* must declare non-authoritative status



---



## ∴ One-line Summary



This repository allows the system to \*\*see patterns in its own structure without acting on them\*\*.



