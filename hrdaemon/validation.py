"""Deterministic schema validation.

Every entity in the system (case, evidence item, event, claim, request,
response, unresolved dependency, human decision, proposed model action) is
validated against an explicit JSON Schema file in `schemas/`. Validation is
pure and deterministic: same input, same result, no network access, no
hidden state.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError as _JsonSchemaValidationError

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = REPO_ROOT / "schemas"

_SCHEMA_CACHE: dict[str, dict[str, Any]] = {}
_VALIDATOR_CACHE: dict[str, Draft202012Validator] = {}


class SchemaValidationError(Exception):
    """Raised with every schema violation, not just the first."""

    def __init__(self, entity_type: str, errors: list[str]):
        self.entity_type = entity_type
        self.errors = errors
        message = f"{entity_type}: " + "; ".join(errors)
        super().__init__(message)


def load_schema(entity_type: str) -> dict[str, Any]:
    if entity_type not in _SCHEMA_CACHE:
        path = SCHEMA_DIR / f"{entity_type}.schema.json"
        if not path.exists():
            raise FileNotFoundError(f"no schema for entity type '{entity_type}' at {path}")
        _SCHEMA_CACHE[entity_type] = json.loads(path.read_text())
    return _SCHEMA_CACHE[entity_type]


def _validator_for(entity_type: str) -> Draft202012Validator:
    if entity_type not in _VALIDATOR_CACHE:
        schema = load_schema(entity_type)
        Draft202012Validator.check_schema(schema)
        _VALIDATOR_CACHE[entity_type] = Draft202012Validator(schema)
    return _VALIDATOR_CACHE[entity_type]


def validate(entity_type: str, instance: dict[str, Any]) -> None:
    """Validate `instance` against the named schema.

    Raises SchemaValidationError listing every violation found. Returns
    None (not the instance) — validation never mutates or coerces data.
    """
    validator = _validator_for(entity_type)
    errors: list[_JsonSchemaValidationError] = sorted(
        validator.iter_errors(instance), key=lambda e: list(e.path)
    )
    if errors:
        formatted = [f"{'/'.join(str(p) for p in e.path) or '<root>'}: {e.message}" for e in errors]
        raise SchemaValidationError(entity_type, formatted)


def is_valid(entity_type: str, instance: dict[str, Any]) -> bool:
    try:
        validate(entity_type, instance)
    except SchemaValidationError:
        return False
    return True


ENTITY_TYPES = (
    "case",
    "evidence_item",
    "event",
    "claim",
    "request",
    "response",
    "unresolved_dependency",
    "human_decision",
    "proposed_action",
)
