"""Consequential actions and consequential state transitions require an
explicit, attributable human decision. Neither evidence nor model output
alone can authorize them."""

import pytest

from hrdaemon.ai_boundary import BoundedContext, EchoProvider, ProposedModelAction
from hrdaemon.authority import ApprovalError, apply_proposed_action, is_draft_only
from hrdaemon.state_machine import TransitionError, is_consequential, transition
from .conftest import load_json


def test_proposed_action_cannot_be_applied_without_human_decision():
    provider = EchoProvider()
    action = provider.propose(BoundedContext(case_id="case-006", facts=("ev-050",)))
    with pytest.raises(ApprovalError):
        apply_proposed_action(action, case_id="case-006", human_decision=None)


def test_proposed_action_applies_once_a_human_decision_is_recorded():
    action_data = load_json("proposed_communication_approval", "proposed_action.json")
    decision = load_json("proposed_communication_approval", "human_decision.json")
    action = ProposedModelAction(
        kind=action_data["kind"],
        summary=action_data["summary"],
        rationale=action_data["rationale"],
        supporting_evidence_refs=tuple(action_data["supporting_evidence_refs"]),
        is_inference=action_data["is_inference"],
        requires_human_approval=action_data["requires_human_approval"],
        provider_name=action_data["generated_by"]["provider_name"],
        provider_version=action_data["generated_by"]["provider_version"],
    )
    outcome = apply_proposed_action(action, case_id="case-006", human_decision=decision)
    assert outcome.applied is True
    assert outcome.approved_by_role == "hr_role"
    assert outcome.decision_id == "dec-050"


def test_human_decision_without_named_role_cannot_approve():
    action = EchoProvider().propose(BoundedContext(case_id="case-006", facts=("ev-050",)))
    with pytest.raises(ApprovalError):
        apply_proposed_action(
            action,
            case_id="case-006",
            human_decision={"decision_id": "dec-x", "decided_by_role": ""},
        )


def test_consequential_transition_requires_human_decision():
    with pytest.raises(TransitionError):
        transition("review", "resolved", human_decision=None)


def test_consequential_transition_succeeds_with_human_decision():
    result = transition(
        "review", "resolved", human_decision={"decided_by_role": "hr_role"}
    )
    assert result == "resolved"


def test_non_consequential_transition_needs_no_decision():
    assert not is_consequential("open", "waiting")
    assert transition("open", "waiting") == "waiting"


def test_illegal_transition_is_rejected_even_with_a_decision():
    with pytest.raises(TransitionError):
        transition("closed", "open", human_decision={"decided_by_role": "hr_role"})


def test_draft_communication_is_flagged_draft_only_before_approval():
    action = EchoProvider().propose(BoundedContext(case_id="case-006", facts=("ev-050",)))
    assert is_draft_only(action) is True
