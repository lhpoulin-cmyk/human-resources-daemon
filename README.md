# human-resources-daemon

*A human-resources process daemon. Mostly friendly. Always watching the state machine.*

human-resources-daemon is an experimental, human-authority-first system for structuring HR communication, evidence, process state, and decision support.

The core idea is simple: many workplace communication failures are process failures that can be modeled, documented, checked, and improved without replacing human judgment.

## Design intent

The system should help a human operator:

- separate topics and cases cleanly;
- preserve provenance and chronology;
- distinguish facts, claims, requests, responses, and unresolved questions;
- identify process gaps and conflicting records;
- generate consistent, reviewable communications;
- maintain an auditable decision trail;
- keep consequential decisions under explicit human authority.

It is **not** intended to autonomously make adverse employment decisions, determine legal rights, diagnose people, or impersonate an HR professional.

## Project posture

Development begins with synthetic data only. Prefer deterministic state, explicit schemas, provenance, reversible operations, and human review at consequential boundaries. AI models are bounded inference providers, not authorities.

See [INITIAL-ENGINEERING-ASSIGNMENT.md](INITIAL-ENGINEERING-ASSIGNMENT.md) for the active first-pass assignment and [CLAUDE.md](CLAUDE.md) for governing implementation instructions.

## Stack

Python 3.11+, [`jsonschema`](https://pypi.org/project/jsonschema/) for
deterministic schema validation, and `pytest` for tests. No framework, no
database, no network calls, no build step — the first pass is a small,
inspectable library plus synthetic fixtures.

This was chosen because the first-pass deliverable is fundamentally about
explicit schemas, deterministic validation, and a provider-neutral
boundary; a library with a test suite proves those properties directly,
without a web framework or persistence layer adding surface area that
isn't needed yet.

## Setup and test

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/pytest
```

## Layout

- `schemas/` — one JSON Schema per entity type (case, evidence item,
  event, claim/assertion, request, response, unresolved dependency, human
  decision, proposed model action).
- `hrdaemon/` — the library: `validation.py` (schema validation),
  `ai_boundary.py` (provider-neutral AI interface), `state_machine.py`
  (case state transitions), `authority.py` (human-approval gate).
- `fixtures/` — synthetic example cases, one directory per scenario. See
  `CONTRIBUTING.md` for the synthetic-data rule.
- `tests/` — schema, provenance, evidence/inference separation, human
  approval, provider failure, and draft-only-outbound tests.
- `docs/STATE-MACHINE.md` — the case state machine and which transitions
  require human approval.
- `docs/AUTHORITY-MODEL.md` — the AI provider boundary and the
  human-approval authority gate.

## License

This project is licensed under the [PolyForm Noncommercial License 1.0.0](LICENSE.md).

**Commercial use requires a separate license from the copyright holder.** See [COMMERCIAL-LICENSE.md](COMMERCIAL-LICENSE.md).

Required Notice: Copyright 2026 Louis H. Poulin II
