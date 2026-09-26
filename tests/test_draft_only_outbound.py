"""Outbound communications remain drafts until a human has approved them."""

import pytest

from hrdaemon.ai_boundary import BoundedContext, EchoProvider
from hrdaemon.authority import ApprovalError, apply_proposed_action, is_draft_only
from hrdaemon.validation import validate
from .conftest import load_json


def test_draft_communication_flagged_pending_before_approval():
    action_data = load_json("proposed_communication_approval", "proposed_action.json")
    validate("proposed_action", action_data)
    assert action_data["status"] == "pending"
    assert action_data["decision_id"] is None


def test_draft_cannot_be_applied_without_approval():
    action = EchoProvider().propose(BoundedContext(case_id="case-006", facts=("ev-050",)))
    assert is_draft_only(action)
    with pytest.raises(ApprovalError):
        apply_proposed_action(action, case_id="case-006", human_decision=None)


def test_draft_only_becomes_a_recorded_outcome_after_approval():
    action = EchoProvider().propose(BoundedContext(case_id="case-006", facts=("ev-050",)))
    outcome = apply_proposed_action(
        action,
        case_id="case-006",
        human_decision={"decided_by_role": "hr_role", "decision_id": "dec-x"},
    )
    assert outcome.applied is True
    assert outcome.action_kind == "draft_communication"
