"""The case state machine.

States mirror `schemas/case.schema.json`'s `status` enum:
open -> waiting -> review -> resolved -> closed

Transitions are explicit and deterministic: only the edges listed in
ALLOWED_TRANSITIONS are legal. Transitions marked as consequential require
an attributable human decision; they can never be taken on evidence or
model inference alone.

See docs/STATE-MACHINE.md for the diagram and rationale.
"""

from __future__ import annotations

VALID_STATES = frozenset({"open", "waiting", "review", "resolved", "closed"})

ALLOWED_TRANSITIONS: dict[str, frozenset[str]] = {
    "open": frozenset({"waiting", "review", "closed"}),
    "waiting": frozenset({"open", "review", "closed"}),
    "review": frozenset({"waiting", "open", "resolved"}),
    "resolved": frozenset({"review", "closed"}),
    "closed": frozenset(),
}

# Transitions that change the case's disposition and therefore require an
# explicit, attributable human decision before they may be taken.
CONSEQUENTIAL_TRANSITIONS: frozenset[tuple[str, str]] = frozenset(
    {
        ("review", "resolved"),
        ("resolved", "closed"),
        ("open", "closed"),
        ("waiting", "closed"),
    }
)


class TransitionError(Exception):
    pass


def transition(current_status: str, target_status: str, *, human_decision: dict | None = None) -> str:
    """Return `target_status` if the transition is legal, else raise.

    `human_decision` must be provided (a dict with at least `decided_by_role`)
    for any transition in CONSEQUENTIAL_TRANSITIONS. It is not validated
    against the human_decision schema here — callers are expected to have
    already validated it via `hrdaemon.validation.validate("human_decision", ...)`.
    """
    if current_status not in VALID_STATES:
        raise TransitionError(f"unknown current status: {current_status!r}")
    if target_status not in VALID_STATES:
        raise TransitionError(f"unknown target status: {target_status!r}")
    if target_status not in ALLOWED_TRANSITIONS[current_status]:
        raise TransitionError(f"illegal transition {current_status!r} -> {target_status!r}")

    is_consequential = (current_status, target_status) in CONSEQUENTIAL_TRANSITIONS
    if is_consequential:
        if human_decision is None:
            raise TransitionError(
                f"transition {current_status!r} -> {target_status!r} is consequential and "
                "requires an explicit human decision"
            )
        if not human_decision.get("decided_by_role"):
            raise TransitionError("human decision must name a decided_by_role")

    return target_status


def is_consequential(current_status: str, target_status: str) -> bool:
    return (current_status, target_status) in CONSEQUENTIAL_TRANSITIONS
