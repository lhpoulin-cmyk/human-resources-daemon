# human-resources-daemon

*A human-resources process daemon. Mostly friendly. Always watching the state machine.*

human-resources-daemon is an experimental, human-authority-first system for structuring HR communication, evidence, process state, and decision support.

The core idea is simple: many workplace communication failures are process failures that can be modeled, documented, checked, and improved without replacing human judgment.

## Design intent

The system should help a human operator:

- separate topics and cases cleanly;
- preserve provenance and chronology;
- distinguish facts, claims, requests, responses, and unresolved questions;
- identify process gaps and conflicting records;
- generate consistent, reviewable communications;
- maintain an auditable decision trail;
- keep consequential decisions under explicit human authority.

It is **not** intended to autonomously make adverse employment decisions, determine legal rights, diagnose people, or impersonate an HR professional.

## Project posture

Development begins with synthetic data only. Prefer deterministic state, explicit schemas, provenance, reversible operations, and human review at consequential boundaries. AI models are bounded inference providers, not authorities.

See [INITIAL-ENGINEERING-ASSIGNMENT.md](INITIAL-ENGINEERING-ASSIGNMENT.md) for the active first-pass assignment and [CLAUDE.md](CLAUDE.md) for governing implementation instructions.

## License

This project is licensed under the [PolyForm Noncommercial License 1.0.0](LICENSE.md).

**Commercial use requires a separate license from the copyright holder.** See [COMMERCIAL-LICENSE.md](COMMERCIAL-LICENSE.md).

Required Notice: Copyright 2026 Louis H. Poulin II
