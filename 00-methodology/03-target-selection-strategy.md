# 03 — Target / Program Selection Strategy

Applies mainly to bug bounty (self-directed target choice); for contracted pentests the target is fixed and you skip to `01-engagement-workflow.md`.

## Program type trade-off

| Factor | VDP (Vulnerability Disclosure Program) | Paid bounty program |
|---|---|---|
| Competition | Low | High, especially on well-known programs |
| App hardening | Often lower | Often higher (already picked over) |
| Payout | None or swag | Cash, tiered by severity |
| Best for | Building process, earning private invites | Once you have a repeatable methodology |

Strategy: start VDP-heavy to build your recon → triage → report pipeline without financial pressure, then move into paid programs once your hit rate is consistent.

## Scope shape trade-off

- **Wildcard scope** (`*.target.com`) — large attack surface, but recon alone can eat days before you test anything. Only take this if you have time budget and enjoy asset-hunting.
- **Narrow, named-asset scope** — faster to a first finding, but more competition per asset since everyone else is looking at the same short list.

## Signals worth prioritizing once inside a target

- **Multi-role applications** (admin/manager/member/viewer tiers) — access-control and business-logic bugs cluster at role boundaries.
- **Free tier + paid tier** — the exact boundary between plans is a recurring source of broken access control / IDOR.
- **Import/export features, integrations, anything built on an existing feature** — these are bolted-on code paths, frequently under-tested by the original dev team.
- **Legacy or unmaintained-looking subdomains** — old tech stacks surface in `07-tech-stack-vuln-mapping.md` as known-CVE candidates fast.

## Anti-pattern to avoid
Jumping straight into a massive, heavily-hunted program (e.g. a major tech company) as a first target. Recon competition is brutal there and the app is already hardened against common findings — start smaller to calibrate your process first.
