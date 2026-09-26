"""The authority boundary.

Defines what counts as a consequential action and enforces that such
actions can only be applied alongside an explicit, attributable human
decision. This module is the single place where a `ProposedModelAction`
(inference) can turn into a recorded outcome (fact of what was done).

Nothing here performs the action itself (e.g. actually sending an email);
it only records that a human authorized it. Outbound communications are
represented as drafts until this gate has been passed — see
docs/AUTHORITY-MODEL.md.
"""

from __future__ import annotations

from dataclasses import dataclass

from .ai_boundary import ProposedModelAction

# Kinds of proposed action that always require human approval before
# being applied. Currently this is all of them — the system does not
# support any autonomous action.
CONSEQUENTIAL_ACTION_KINDS = frozenset(
    {"draft_communication", "suggest_transition", "flag_contradiction", "suggest_question"}
)


class ApprovalError(Exception):
    pass


@dataclass(frozen=True)
class RecordedOutcome:
    """The durable record of what happened after a human decision."""

    action_kind: str
    case_id: str
    applied: bool
    approved_by_role: str | None
    decision_id: str | None
    action_summary: str


def apply_proposed_action(
    action: ProposedModelAction,
    *,
    case_id: str,
    human_decision: dict | None,
) -> RecordedOutcome:
    """Apply `action` only if accompanied by a qualifying human decision.

    Raises ApprovalError if the action requires approval (i.e. always, for
    every kind currently defined) and no valid human decision is present.
    A provider producing a proposal never bypasses this gate: even a
    trusted-looking proposal must be paired with a real human_decision
    record naming who decided.
    """
    if action.kind not in CONSEQUENTIAL_ACTION_KINDS:
        raise ApprovalError(f"unknown proposed action kind: {action.kind!r}")

    if action.requires_human_approval:
        if human_decision is None:
            raise ApprovalError(
                f"proposed action '{action.kind}' requires human approval; no human_decision provided"
            )
        decided_by = human_decision.get("decided_by_role")
        if not decided_by:
            raise ApprovalError("human_decision must name a decided_by_role; cannot attribute approval")

    approved_by = human_decision.get("decided_by_role") if human_decision else None
    decision_id = human_decision.get("decision_id") if human_decision else None

    return RecordedOutcome(
        action_kind=action.kind,
        case_id=case_id,
        applied=True,
        approved_by_role=approved_by,
        decision_id=decision_id,
        action_summary=action.summary,
    )


def is_draft_only(action: ProposedModelAction) -> bool:
    """Outbound communications proposed by a model are drafts until a human
    decision has been recorded. This is a pure predicate; nothing in the
    codebase should ever mark a draft as sent without going through
    `apply_proposed_action` first."""
    return action.kind == "draft_communication"
