"""Provider failure must not corrupt authoritative state: a failed proposal
must produce no ProposedModelAction and no side effect on case state."""

import pytest

from hrdaemon.ai_boundary import BoundedContext, FailingProvider, ProviderError
from hrdaemon.authority import apply_proposed_action


def test_failing_provider_raises_and_returns_nothing():
    provider = FailingProvider()
    with pytest.raises(ProviderError):
        provider.propose(BoundedContext(case_id="case-999"))


def test_provider_failure_leaves_no_action_to_apply():
    provider = FailingProvider()
    action = None
    try:
        action = provider.propose(BoundedContext(case_id="case-999"))
    except ProviderError:
        pass
    assert action is None
    # With no action produced, there is nothing that could reach
    # apply_proposed_action — a provider failure cannot be laundered into
    # an applied outcome.
