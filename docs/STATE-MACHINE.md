# Case State Machine

Implementation: [`hrdaemon/state_machine.py`](../hrdaemon/state_machine.py).
Tests: [`tests/test_human_approval.py`](../tests/test_human_approval.py).

## States

Mirrors `status` in [`schemas/case.schema.json`](../schemas/case.schema.json):

- `open` — case has been created; no outstanding request or response yet.
- `waiting` — the case is blocked on a party, a dependency, or a deadline.
- `review` — the case has enough information for a human to consider a resolution.
- `resolved` — a human has recorded a resolution; the case is not yet closed.
- `closed` — terminal. No further transitions are allowed.

## Transitions

```
        ┌────────────┐
   ┌───►│    open    │◄───┐
   │    └─────┬──────┘    │
   │          │           │
   │    ┌─────▼──────┐    │
   └────┤  waiting   │    │
        └─────┬──────┘    │
              │            │
        ┌─────▼──────┐    │
        │   review   ├────┘
        └─────┬──────┘
              │ (human decision required)
        ┌─────▼──────┐
        │  resolved  │
        └─────┬──────┘
              │ (human decision required)
        ┌─────▼──────┐
        │   closed   │  (terminal)
        └────────────┘
```

Every edge drawn above is the *only* legal set of transitions —
`ALLOWED_TRANSITIONS` in `state_machine.py` is the single source of truth,
and `transition()` raises `TransitionError` for anything not listed there
(including from `closed`, which has no outgoing edges).

## Consequential transitions

Some transitions change the case's disposition and are marked
**consequential** in `CONSEQUENTIAL_TRANSITIONS`:

- `review -> resolved`
- `resolved -> closed`
- `open -> closed`
- `waiting -> closed`

A consequential transition can never be taken from evidence, a claim, or a
model proposal alone. `transition()` requires a `human_decision` argument
naming a `decided_by_role`; without one it raises `TransitionError`. This
mirrors the mandatory invariant in `CLAUDE.md`: *"Consequential actions
require explicit human approval."*

Non-consequential transitions (e.g. `open -> waiting`, `waiting -> review`)
represent ordinary process movement and do not require a recorded human
decision, though they are still expected to be tied to an event with
evidence at the case level.

## Why not fewer states?

`waiting` and `review` are kept distinct because they answer different
questions: `waiting` means "blocked on someone else," `review` means
"unblocked and ready for a human to decide." Collapsing them would lose
the distinction between "the state machine has nothing to do" and "the
state machine is asking a human to act."
