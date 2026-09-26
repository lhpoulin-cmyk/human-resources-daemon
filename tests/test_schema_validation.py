"""Every synthetic fixture must validate against its schema, and the
validator must reject deliberately malformed instances."""

import pytest

from hrdaemon.validation import SchemaValidationError, validate
from .conftest import load_json


@pytest.mark.parametrize(
    "entity_type,path",
    [
        ("case", ("clean_single_topic", "case.json")),
        ("case", ("conflated_topics", "case.json")),
        ("case", ("conflicting_records", "case.json")),
        ("case", ("missing_revision_date", "case.json")),
        ("case", ("unresolved_handoff", "case.json")),
        ("case", ("proposed_communication_approval", "case.json")),
        ("unresolved_dependency", ("missing_revision_date", "unresolved_dependency.json")),
        ("unresolved_dependency", ("unresolved_handoff", "unresolved_dependency.json")),
        ("proposed_action", ("proposed_communication_approval", "proposed_action.json")),
        ("human_decision", ("proposed_communication_approval", "human_decision.json")),
    ],
)
def test_fixture_validates_against_schema(entity_type, path):
    instance = load_json(*path)
    validate(entity_type, instance)  # raises on failure


@pytest.mark.parametrize(
    "entity_type,path",
    [
        ("evidence_item", ("clean_single_topic", "evidence.json")),
        ("evidence_item", ("conflated_topics", "evidence.json")),
        ("evidence_item", ("conflicting_records", "evidence.json")),
        ("evidence_item", ("missing_revision_date", "evidence.json")),
        ("evidence_item", ("unresolved_handoff", "evidence.json")),
        ("evidence_item", ("proposed_communication_approval", "evidence.json")),
    ],
)
def test_evidence_list_fixture_validates(entity_type, path):
    for item in load_json(*path):
        validate(entity_type, item)


def test_conflicting_records_claims_validate():
    for claim in load_json("conflicting_records", "claims.json"):
        validate("claim", claim)


def test_missing_required_field_is_rejected():
    with pytest.raises(SchemaValidationError):
        validate("case", {"case_id": "x"})


def test_unknown_status_is_rejected():
    case = load_json("clean_single_topic", "case.json")
    case = dict(case, status="deleted_forever")
    with pytest.raises(SchemaValidationError):
        validate("case", case)


def test_additional_properties_are_rejected():
    evidence = load_json("clean_single_topic", "evidence.json")[0]
    evidence = dict(evidence, raw_ssn="not-allowed")
    with pytest.raises(SchemaValidationError):
        validate("evidence_item", evidence)


def test_evidence_item_must_be_marked_synthetic():
    evidence = load_json("clean_single_topic", "evidence.json")[0]
    evidence = dict(evidence, is_synthetic=False)
    with pytest.raises(SchemaValidationError):
        validate("evidence_item", evidence)


def test_proposed_action_cannot_disable_human_approval():
    action = load_json("proposed_communication_approval", "proposed_action.json")
    action = dict(action, requires_human_approval=False)
    with pytest.raises(SchemaValidationError):
        validate("proposed_action", action)


def test_proposed_action_cannot_claim_to_be_non_inference():
    action = load_json("proposed_communication_approval", "proposed_action.json")
    action = dict(action, is_inference=False)
    with pytest.raises(SchemaValidationError):
        validate("proposed_action", action)


def test_human_decision_requires_named_role():
    decision = load_json("proposed_communication_approval", "human_decision.json")
    decision = dict(decision, decided_by_role="")
    with pytest.raises(SchemaValidationError):
        validate("human_decision", decision)
