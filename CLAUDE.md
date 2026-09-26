# Claude Handoff — human-resources-daemon

You are taking over the initial engineering pass for **human-resources-daemon**.

## Mission

Turn the project brief and architecture direction into a small, rigorous, testable foundation for a human-authority-first HR process system.

The core design principle is that difficult workplace interactions are often easier to handle when modeled as process problems: isolate topics, preserve evidence, model state, surface unresolved dependencies, and keep consequential authority with humans.

This is **decision support**, not an autonomous HR decision-maker.

## Read first

Read in this order:

1. `README.md`
2. `LICENSE.md`
3. `COMMERCIAL-LICENSE.md`
4. `docs/PROJECT-BRIEF.md`
5. `docs/ARCHITECTURE.md`

Do not weaken licensing notices or alter the PolyForm license text.

## Initial engineering assignment

Establish a minimal but credible repository foundation.

### Deliverables

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
4. Add a provider-neutral AI boundary. No business logic may depend on Claude-specific conversation state.
5. Add synthetic fixtures demonstrating:
   - one clean single-topic case;
   - one email that conflates multiple topics;
   - conflicting records;
   - a missing issuance/revision date;
   - an unresolved payment or responsibility handoff;
   - a proposed communication requiring human approval.
6. Add tests enforcing the core invariants.
7. Add documentation for the case state machine and authority boundaries.
8. Add a `CONTRIBUTING.md` that requires synthetic data in committed tests/examples.
9. Add a `.gitignore` appropriate to the chosen stack.
10. Keep the first implementation deliberately small.

## Mandatory invariants

- Evidence is not inference.
- A source claim is not automatically a fact.
- Model output is not evidence.
- Provenance must survive every transformation.
- Consequential actions require explicit human approval.
- Provider failure must not corrupt authoritative state.
- Real HR, medical, disability, benefits, legal, or personally identifying records must not be committed.
- Outbound communications remain drafts until human-approved.
- Every derived assertion should be traceable to supporting evidence or explicitly marked as inference.
- Do not build employee scoring, personality scoring, or autonomous adverse-action logic.

## Product philosophy

Prefer boring, inspectable machinery over clever autonomy.

A useful internal pattern is:

`evidence -> normalized event/claim -> case state -> unresolved dependency -> proposed action -> human decision -> recorded outcome`

The system should help a person answer:

- What do we know?
- How do we know it?
- What is only claimed or inferred?
- What process is currently open?
- Who owns the next step?
- What is blocking resolution?
- What action is proposed?
- Who must approve it?
- What happened after approval?

## Tone

The repo name is tongue-in-cheek. The implementation should be professional, restrained, and auditable.

## First-pass completion test

Stop the first pass when a new developer can clone the repo, run one documented command, execute the test suite, inspect the synthetic example cases, and understand exactly where human authority enters the system.

Do not ingest real case material yet.
