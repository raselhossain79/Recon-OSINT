# Recon-OSINT

A structured, numbered reference library for the information-gathering phase of penetration testing and bug bounty work — everything that happens **before** a single scan or exploit is fired.

## Why this repo exists

Recon isn't "run subfinder, run nmap, done." Treated properly it's a staged intelligence process: passive before active, always narrowing signal-to-noise, and always ending in one consolidated asset list before scanning starts. Every numbered folder here maps to one stage of that process, in the order you actually work through it.

## Top-level structure (numbered = order of use)

```
00-methodology/       ← read first, every engagement
01-osint/              ← organization/domain intel
  01-priority-technical/    ← do this every time (~20-40 min/target)
  02-optional-investigative/← only if social-eng/phishing/physical is in scope
02-reconnaissance/     ← the main technical phase
  01-web/
  02-api/
  03-network/
  04-cloud/
  05-mobile-app/
  06-wireless/          ← optional, rarely applicable to web/API work
```

## Full workflow, start to finish

1. **`00-methodology/01-engagement-workflow.md`** — the master sequence; read this file first, it links to everything else in order.
2. **`00-methodology/02-scope-and-legal-checklist.md`** — confirm authorization and boundaries before touching anything.
3. **`01-osint/01-priority-technical/`** — quick pass: domain/DNS history, org/corporate intel, breach exposure, email format. Directly expands your asset list and gives tech-stack hints.
4. *(Only if scope includes social-engineering/phishing/physical work)* **`01-osint/02-optional-investigative/`** — people, social media, geolocation, dark web, document metadata.
5. **`02-reconnaissance/01-web/`** through **`06-wireless/`** — the main technical phase, passive techniques before active ones within each category. Work through whichever categories apply to your target's asset types.
6. **`00-methodology/06-asset-inventory-template.md`** — every finding from steps 3–5 gets consolidated here. Nothing counts as a real target until it's in this sheet.
7. **`00-methodology/07-tech-stack-vuln-mapping.md`** — cross-reference the consolidated tech stack against known CVEs.
8. **`00-methodology/08-recon-to-scanning-handoff.md`** — triage, tool selection, manual/automated split, final scope re-check. This is the exit point — active scanning and exploitation live in a separate repo.

## Conventions used throughout

- Every technique file states whether it's **passive** (no direct target touch) or **active** (generates real traffic, log it) — this distinction matters for scope compliance and for pacing.
- Every command includes a flag-by-flag explanation, not just the raw command — the goal is understanding why a flag is set, not copy-pasting blind.
- Every file ends with an explicit **Output** section stating exactly which other file/step the findings feed into — nothing is a dead end.
- Full English only throughout.
