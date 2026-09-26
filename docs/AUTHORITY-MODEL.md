# Authority Model

Implementation: [`hrdaemon/authority.py`](../hrdaemon/authority.py),
[`hrdaemon/ai_boundary.py`](../hrdaemon/ai_boundary.py).
Tests: [`tests/test_human_approval.py`](../tests/test_human_approval.py),
[`tests/test_draft_only_outbound.py`](../tests/test_draft_only_outbound.py),
[`tests/test_provider_failure.py`](../tests/test_provider_failure.py).

## The core rule

**A model may propose. A human must dispose.** (`docs/PROJECT-BRIEF.md`)

Nothing in this codebase allows a `ProposedModelAction` to change case
state, send a communication, or corroborate a claim by itself. Every
consequential effect passes through `authority.apply_proposed_action()`,
which requires a `human_decision` record naming who decided
(`decided_by_role`).

## Pipeline

```
evidence -> normalized event/claim -> case state
         -> unresolved dependency
         -> proposed action (AI boundary, always inference)
         -> human decision (authority gate)
         -> recorded outcome
```

Each arrow is a one-way, append-only step. Evidence is never rewritten in
place (`supersedes` links a revision to what it replaces); a proposed
action is never silently promoted to a recorded outcome.

## The AI provider boundary

`hrdaemon/ai_boundary.py` defines:

- `BoundedContext` — the only input a provider may see: explicit facts,
  claims, unresolved questions, and an instruction string. No provider
  receives an entire case object, prior conversational turns, or any
  vendor-specific session/message state.
- `ProposedModelAction` — the only output a provider may return. Always
  `is_inference=True` and `requires_human_approval=True`; these are not
  configurable by the provider (see the `const: true` constraints in
  `schemas/proposed_action.schema.json`).
- `AIProvider` — an abstract interface. `EchoProvider` is a deterministic,
  offline reference implementation used by tests and local development.
  `FailingProvider` exists solely to exercise failure handling.

Business logic in `hrdaemon/authority.py` and `hrdaemon/state_machine.py`
imports only `BoundedContext` and `ProposedModelAction` — never a specific
vendor SDK type. Swapping `EchoProvider` for a real model provider requires
no change to authority or state-machine code, only a new `AIProvider`
implementation.

## What requires human approval

Every `proposed_action.kind` currently defined
(`draft_communication`, `suggest_transition`, `flag_contradiction`,
`suggest_question`) is consequential and requires approval — there is no
autonomous-action category. `authority.CONSEQUENTIAL_ACTION_KINDS` is the
enumerable, single source of truth; adding a new proposal kind that skips
approval requires an explicit code change reviewers can see in a diff,
not a configuration flag.

## Outbound communications

A `draft_communication` proposal (`authority.is_draft_only()`) is always a
draft. It is represented with `status: "pending"` and `decision_id: null`
in `schemas/proposed_action.schema.json` until a `human_decision` is
recorded against it (`decision_id` set, `status` moves to `approved` or
`rejected`). Nothing in this repository has the ability to actually
transmit a communication; that is out of scope for this pass by design —
see `docs/PROJECT-BRIEF.md`'s non-goals.

## Provider failure

`AIProvider.propose()` may raise `ProviderError`. Because
`apply_proposed_action()` only ever operates on a `ProposedModelAction`
instance, a raised `ProviderError` means no action object exists to apply
— there is no partial or corrupted state to clean up. See
`tests/test_provider_failure.py`.

## What is explicitly out of scope

Per `docs/PROJECT-BRIEF.md` non-goals and the mandatory invariants in
`CLAUDE.md`, this codebase does not implement, and must not be extended to
implement without a separate explicit decision:

- autonomous hiring, firing, discipline, accommodation, benefits, or legal
  determinations;
- employee scoring or psychological/personality profiling;
- automatic advancement of consequential actions;
- treating model output as evidence.
