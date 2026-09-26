# Initial Engineering Assignment

Repository: `lhpoulin-cmyk/human-resources-daemon`

This is the **only active assignment for the initial engineering pass**.

Do not inspect or act on unrelated Helix remediation trackers, workstation checkpoints, portfolio repositories, or other repositories unless this repository explicitly references them as a dependency.

## Objective

Establish a minimal, rigorous, testable foundation for a human-authority-first HR process system.

## Required deliverables

1. Choose a small implementation stack and document the rationale.
2. Create explicit schemas for:
   - case;
   - evidence item;
   - event;
   - claim/assertion;
   - request;
   - response;
   - unresolved dependency;
   - human decision;
   - proposed model action.
3. Implement deterministic validation for those schemas.
4. Add a provider-neutral AI boundary. No business logic may depend on Claude-specific conversational state.
5. Add synthetic fixtures demonstrating:
   - one clean single-topic case;
   - one communication that conflates multiple topics;
   - conflicting records;
   - a missing issuance/revision date;
   - an unresolved payment or responsibility handoff;
   - a proposed communication requiring human approval.
6. Add tests enforcing the mandatory invariants in `CLAUDE.md`.
7. Document the case state machine and authority boundaries.
8. Add `CONTRIBUTING.md` requiring synthetic data in committed tests/examples.
9. Add an appropriate `.gitignore`.
10. Keep the first implementation deliberately small.

## Execution rules

- Work only inside this repository for this assignment.
- Read `CLAUDE.md`, `README.md`, `docs/PROJECT-BRIEF.md`, and `docs/ARCHITECTURE.md` before implementation.
- Do not ingest real HR, medical, disability, benefits, legal, or personally identifying records.
- Do not alter licensing terms.
- Prefer deterministic, inspectable mechanisms over autonomous behavior.
- Consequential actions must remain human-controlled.

## Completion condition

The first pass is complete when a new developer can:

1. clone the repository;
2. run one documented setup/test command;
3. execute the full test suite successfully;
4. inspect the synthetic example cases;
5. understand where model inference stops and human authority begins.

When finished, provide a concise implementation report containing:
- stack selected;
- files/directories added;
- tests added and their results;
- any unresolved design questions;
- the exact command used to run the test suite.
