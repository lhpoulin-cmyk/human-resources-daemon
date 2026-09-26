"""Provider-neutral AI boundary.

No business logic elsewhere in this repository may depend on any
vendor-specific conversational state (message ids, chat/session history,
provider-specific tool-call formats, etc). Every provider receives a
`BoundedContext` (plain, serializable data) and returns a
`ProposedModelAction` (also plain and serializable). Both are defined here,
independent of any specific model vendor.

A proposal is always inference. It is never evidence, and it never mutates
case state by itself — see `hrdaemon.authority`.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass(frozen=True)
class BoundedContext:
    """The only input a provider may see: an explicit, bounded slice of case
    material. No hidden history, no full case object, no vendor session."""

    case_id: str
    facts: tuple[str, ...] = ()
    claims: tuple[str, ...] = ()
    unresolved_questions: tuple[str, ...] = ()
    instruction: str = ""


@dataclass(frozen=True)
class ProposedModelAction:
    """The only output a provider may return. Mirrors, but is independent
    of, the `proposed_action` schema so the boundary has no schema
    dependency on any single vendor's response shape."""

    kind: str
    summary: str
    rationale: str
    supporting_evidence_refs: tuple[str, ...] = ()
    is_inference: bool = True
    requires_human_approval: bool = True
    provider_name: str = ""
    provider_version: str | None = None


class ProviderError(Exception):
    """Raised when a provider cannot produce a proposal.

    A provider failure must never corrupt or partially apply case state:
    callers must treat this as "no proposal produced", nothing else.
    """


class AIProvider(ABC):
    """Provider-neutral interface. Implementations may wrap any vendor SDK,
    but must not leak vendor-specific state past this boundary."""

    @abstractmethod
    def propose(self, context: BoundedContext) -> ProposedModelAction:
        raise NotImplementedError


class EchoProvider(AIProvider):
    """Deterministic, offline provider used for tests and local development.
    Performs no network access and returns the same output for the same
    input every time."""

    name = "echo-provider"
    version = "1.0.0"

    def propose(self, context: BoundedContext) -> ProposedModelAction:
        summary = (
            f"Draft based on {len(context.facts)} fact(s) and "
            f"{len(context.claims)} claim(s) for case {context.case_id}."
        )
        return ProposedModelAction(
            kind="draft_communication",
            summary=summary,
            rationale="Deterministic echo of the bounded context provided; not independently verified.",
            supporting_evidence_refs=context.facts,
            is_inference=True,
            requires_human_approval=True,
            provider_name=self.name,
            provider_version=self.version,
        )


class FailingProvider(AIProvider):
    """A provider that always fails, used to exercise provider-failure
    handling without any real network dependency."""

    name = "failing-provider"
    version = None

    def propose(self, context: BoundedContext) -> ProposedModelAction:
        raise ProviderError("simulated provider failure: no proposal produced")
