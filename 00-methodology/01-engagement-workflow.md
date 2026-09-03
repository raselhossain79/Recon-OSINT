# 01 — Engagement Workflow

The exact order of operations for any engagement, from scope receipt to scanning handoff. This file is the map — every other file in the vault plugs into one of these steps.

## Step-by-step

### Step 1 — Scope intake
Read the full scope document / program page / signed contract before opening a single tool. Log everything into `02-scope-and-legal-checklist.md`. No exceptions — an asset discovered later "because it looked related" is not automatically in scope.

### Step 2 — Passive OSINT pass (priority-technical only)
Run through `01-osint/01-priority-technical/` in order: domain-infra → org-corporate → breach-data → email-username. Budget roughly 20–40 minutes per target here. This is not deep investigation — it's a fast pass that expands your asset list and gives you tech-stack hints before you touch anything actively.

### Step 3 — Passive web/network recon
Everything in `02-reconnaissance/` that doesn't send unusual traffic: certificate transparency, wayback pulls, Shodan/Censys queries, subdomain aggregation from public sources (subfinder/amass in passive mode), GitHub dorking. Zero or near-zero footprint on the target's own logs.

### Step 4 — Active recon
Only after Step 3 is exhausted, and only if scope explicitly allows active scanning. Host discovery → port/service scan → content discovery → screenshotting → tech fingerprinting confirmation. This step touches the target directly and can appear in logs — treat rate limits and timing seriously (see `04-master-tool-index.md` for rate-limit-aware flags).

### Step 5 — Category-specific deep dives
Depending on what Step 3–4 revealed, branch into `web/`, `api/`, `network/`, `cloud/`, `mobile-app/` deep-dive files as relevant. WordPress recon, GraphQL introspection, S3 bucket enumeration, APK teardown — whichever apply to the discovered asset types.

### Step 6 — Consolidation
Every finding across every step gets merged into `06-asset-inventory-template.md`. Nothing exists for testing purposes until it's in this sheet.

### Step 7 — Vulnerability mapping
Cross-reference the consolidated tech stack against known CVEs (`07-tech-stack-vuln-mapping.md`).

### Step 8 — Handoff
Triage, tool selection, manual/automated split, final scope re-check (`08-recon-to-scanning-handoff.md`). This is where the vault ends and active testing/exploitation begins (separate repo).

## Why this order specifically
- Passive-before-active minimizes footprint and avoids scope violations before you even understand the target.
- OSINT-before-deep-recon because org/domain intel often changes what counts as in-scope (subsidiaries, acquisitions) — better to know that before you spend hours enumerating.
- Consolidation-before-scanning is the step most checklists skip, and it's the single biggest cause of duplicate work and missed assets on larger engagements.
