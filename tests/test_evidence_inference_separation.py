"""A source claim is not automatically a fact, and model output is not
evidence. These tests enforce that separation at the schema and workflow
level."""

import pytest

from hrdaemon.ai_boundary import BoundedContext, EchoProvider, ProposedModelAction
from hrdaemon.validation import SchemaValidationError, validate
from .conftest import load_json


def test_claims_start_unverified_not_corroborated():
    for claim in load_json("conflicting_records", "claims.json"):
        assert claim["status"] == "unverified"
        assert claim["corroborated_by_decision_id"] is None


def test_claim_corroboration_is_a_workflow_concern_not_a_schema_one():
    # The schema only enforces shape, so a claim marked "corroborated" with
    # a made-up decision id is syntactically legal on its own. Proving that
    # the referenced human_decision actually exists is a cross-entity
    # invariant enforced by the workflow layer (hrdaemon.authority), not by
    # schema validation. This test documents that boundary.
    claim = load_json("conflicting_records", "claims.json")[0]
    claim = dict(claim, status="corroborated", corroborated_by_decision_id="dec-999")
    validate("claim", claim)


def test_model_proposal_is_never_evidence_typed():
    provider = EchoProvider()
    action = provider.propose(BoundedContext(case_id="case-999", facts=("ev-999",)))
    assert isinstance(action, ProposedModelAction)
    assert action.is_inference is True
    # A ProposedModelAction has no evidence_id and cannot be substituted
    # where an evidence_item is expected.
    assert not hasattr(action, "evidence_id")


def test_proposed_action_schema_forbids_is_inference_false():
    action = load_json("proposed_communication_approval", "proposed_action.json")
    action = dict(action, is_inference=False)
    with pytest.raises(SchemaValidationError):
        validate("proposed_action", action)
