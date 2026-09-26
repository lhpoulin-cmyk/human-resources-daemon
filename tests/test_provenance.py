"""Provenance must survive every transformation: every event and claim
traces back to at least one evidence item, and evidence never disappears
or gets silently backfilled (e.g. a missing document_date stays missing)."""

from hrdaemon.validation import validate
from .conftest import load_json


def test_every_event_traces_to_evidence():
    for scenario in (
        "clean_single_topic",
        "conflated_topics",
        "conflicting_records",
        "missing_revision_date",
        "unresolved_handoff",
        "proposed_communication_approval",
    ):
        case = load_json(scenario, "case.json")
        known_evidence = set(case["evidence_refs"])
        for event in case["events"]:
            assert event["evidence_refs"], f"event {event['event_id']} has no evidence"
            for ref in event["evidence_refs"]:
                assert ref in known_evidence, (
                    f"event {event['event_id']} cites evidence {ref} not listed on the case"
                )


def test_every_claim_traces_to_evidence():
    for claim in load_json("conflicting_records", "claims.json"):
        assert claim["evidence_refs"], f"claim {claim['claim_id']} has no evidence"


def test_missing_document_date_is_preserved_not_defaulted():
    evidence = load_json("missing_revision_date", "evidence.json")[0]
    validate("evidence_item", evidence)
    assert evidence["document_date"] is None


def test_unresolved_dependency_cites_the_evidence_that_created_it():
    dependency = load_json("missing_revision_date", "unresolved_dependency.json")
    validate("unresolved_dependency", dependency)
    assert "ev-030" in dependency["evidence_refs"]
    assert dependency["status"] == "open"


def test_conflicting_claims_each_keep_their_own_evidence():
    claims = load_json("conflicting_records", "claims.json")
    by_id = {c["claim_id"]: c for c in claims}
    assert by_id["claim-020"]["evidence_refs"] == ["ev-020"]
    assert by_id["claim-021"]["evidence_refs"] == ["ev-021"]
    # Contradictory claims must not be merged into a single record.
    assert by_id["claim-020"]["statement"] != by_id["claim-021"]["statement"]
