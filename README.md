# Operator Registry — Hilbert-Pólya Falsification System

A standalone, installable research tool for auditing proposed Hilbert-Pólya operator candidates against a fixed set of falsification rules ("Manus v2" schema). It does not search for candidates and does not rank plausibility — every candidate added is audited against the same rules, every status is tied to a certification level, and every change is logged.

## Install on your phone (like a real app)

1. Open the site in your phone's browser (Safari on iOS, Chrome on Android).
2. **iOS:** Share button → "Add to Home Screen". **Android:** menu (⋮) → "Install app" / "Add to Home screen".
3. It appears on your home screen with its own icon and opens full-screen, fully offline.

## Verdicts

| Verdict | Meaning |
|---|---|
| `REJECTED` | A rejection rule fired — a no-go. |
| `CONDITIONAL_SURVIVOR` | Survives if its named unproved premises are proven. |
| `UNCERTIFIED_INDETERMINATE` | Not enough certified evidence to judge (e.g. floating-point-only negative eigenvalues). |
| `UNCONDITIONAL_SURVIVOR` | All seven required properties proved with valid certification. |
| `SCHEMA_VIOLATION` | Malformed record — blocked from classification entirely. |

## How it works

Each candidate carries seven property subsets — **trace, positivity, covariance, self-adjoint, compact resolvent, Weyl law, determinant** — each with a status paired to a certification level:

- `none` — no evidence yet
- `floating_point` — ordinary computation; suggestive, not certified
- `interval_arithmetic` — certified via rigorous interval/ball arithmetic (Arb, interval Cholesky, rigorous quadrature)
- `analytic_proof` — established by hand-derivation

The audit engine enforces the compatibility rule (a `proved`/`failed`/`indefinite` status cannot be backed by floating-point evidence — that conflation is exactly what v2 exists to catch) and applies rejection rules 1–7: circularity, certified positivity failure, Weyl-law/determinant failure, generic-statistics trace claims, schema violations, and tautological post-hoc constructions.

The registry ships with 9 seeded candidates (3 REJECTED, 1 CONDITIONAL_SURVIVOR, 5 UNCERTIFIED_INDETERMINATE). Their evidence files are linked from the candidate pages.

## Using it

- **Run Audit** re-classifies every candidate and records the run under *Runs & Saved*.
- **Download registry (JSON)** exports everything — candidates, statuses, logs, comments — for backup or sharing.
- **Add Candidate** creates a new record (stored in your browser), with JSON import for pasting existing records.
- Comments are stored locally in your browser.

## Sharing

Built-in **share buttons** use your phone's native share sheet (messages, email, etc.), with a copy-to-clipboard fallback on desktop:

- **↗ Share app** (top bar) — shares the app link so others can install it too.
- **↗ Share summary** (dashboard) — shares the latest audit report as plain text.
- **↗ Share** (candidate page) — shares a candidate's definition, verdict, and reason.
- **↗ share note** (each comment) — shares an individual note.

## Repository layout

- `index.html` — the complete app (registry data, audit engine, UI).
- `research/` — the source registry (`operator_candidates.json`), the Python reference audit engine (`audit_registry.py`), and the Manus v2 schema document.
- `docs/` — the research notes backing each candidate's statuses: no-go proofs, obstruction theorems, and construction notes. These are the same documents linked from the candidate pages' evidence sections.

## Technical notes

- Single-file app: `index.html` contains the registry data, the audit engine (a JavaScript port of the Python reference `audit_operator_registry.py`), and the UI. The engine's verdicts were verified to match the Python reference on all 9 seeded candidates.
- PWA: `manifest.webmanifest` + `sw.js` make it installable and fully offline-capable.
- No server, no account, no tracking. Open `index.html` directly from disk and it still works.
