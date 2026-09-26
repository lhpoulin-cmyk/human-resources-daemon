# Architecture Direction

This is a starting contract, not a finished architecture.

## Layers

### Evidence layer
Stores source material and metadata without silently converting interpretation into fact.

### Case layer
A bounded process container containing topics, parties, requests, events, evidence references, unresolved questions, deadlines, decisions, and communications.

### State layer
Represents process state explicitly rather than inferring it from prose each time. Transitions should be deterministic where possible and attributable to evidence or a human action.

### Analysis layer
AI and deterministic analyzers may summarize, classify, detect possible contradictions, identify missing fields, suggest questions, draft communications, and propose transitions. They do not silently commit consequential state changes.

### Authority layer
Defines what actions require human approval and who may approve them. Initial rule: consequential employment decisions and outbound communications remain human-controlled.

### Presentation layer
Interfaces must distinguish observed fact, source claim, model inference, unresolved question, and human decision.

## AI provider boundary

Define a provider-neutral interface. A provider receives bounded context and returns structured proposals. Business logic must not depend on vendor-specific conversational state.

## Data posture

Development starts with synthetic fixtures only. Real personal, medical, employment, or legal records must not be committed to the repository.

## Testing posture

Tests should prove that:

- provenance cannot disappear;
- claims cannot silently become facts;
- consequential transitions cannot bypass approval;
- source material is immutable or versioned;
- generated communications can identify supporting records;
- provider failure does not corrupt case state.
