# Contributing

## Synthetic data only

Every fixture, example, and committed test file in this repository must be
synthetic. Do not commit real HR, medical, disability, benefits, legal, or
personally identifying records — not even redacted or anonymized real
records. Invent scenarios instead.

- Use role labels (`employee_role`, `manager_role`, `hr_role`,
  `payroll_role`), never real or real-sounding names.
- Use fictional dates, amounts, and scenarios.
- Mark synthetic evidence explicitly: `evidence_item` instances must set
  `"is_synthetic": true` (enforced by `schemas/evidence_item.schema.json`).
- Prefix raw synthetic source text with a visible marker, e.g.
  `[SYNTHETIC TEST FIXTURE — no real person or event]`, as in the files
  under `fixtures/*/raw/`.

If you're adapting a real situation for inspiration, change every
identifying detail — names, dates, department, amounts, and any other
detail that could make the source recognizable — before it goes anywhere
near a commit.

## Before opening a PR

1. Run the test suite: `pytest` (see `README.md` for setup).
2. If you added or changed an entity type, add or update its schema under
   `schemas/` and keep `additionalProperties: false` unless there's a
   specific reason to allow open-ended fields.
3. If you added a new kind of consequential action, wire it through
   `hrdaemon/authority.py` explicitly — do not add a bypass around human
   approval.
4. Do not weaken the license notices or alter the PolyForm license text.

## Scope discipline

This project's stated non-goals (see `docs/PROJECT-BRIEF.md`) are not
suggestions. Do not add employee scoring, personality profiling, or logic
that autonomously advances a consequential action. If a change seems to
require one of these, raise it as a design question rather than
implementing it.
