# Project Brief

## Working name

**human-resources-daemon**  
Short name: **HR-Daemon**

## Problem

Human-resources interactions often fail because multiple topics, records, obligations, requests, and interpretations become conflated across messages and people. The resulting failure is frequently procedural before it is interpersonal.

## Core thesis

Interpersonal friction can often be reduced by locating the process failure:

1. establish what happened;
2. preserve provenance;
3. isolate the topic;
4. identify the current state;
5. identify the responsible human authority;
6. identify the unresolved dependency;
7. prepare a bounded next action;
8. record the result.

The software should make that loop easier without pretending that software is the authority.

## Initial capabilities

- Case and topic separation.
- Evidence/provenance ledger.
- Chronology reconstruction.
- Request/response tracking.
- Contradiction and missing-information detection.
- Communication drafting with factual traceability.
- Decision-support summaries.
- Human approval gates.
- Provider-neutral AI interface.
- Synthetic fixtures and acceptance tests.

## Non-goals

- Autonomous hiring, firing, discipline, accommodation, benefits, or legal determinations.
- Psychological profiling.
- Hidden employee scoring.
- Automatic advancement of consequential actions.
- Treating model output as evidence.

## Safety invariant

**A model may propose. A human must dispose.**

Consequential state changes require an attributable human decision.
