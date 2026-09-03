# 06 — Asset Inventory Template

The single consolidation point for the entire vault. Every technique in `01-osint/` and `02-reconnaissance/` feeds into this sheet. An asset that exists only in a tool's raw output file does not functionally exist for testing purposes — it has to land here first.

## Master sheet columns

| Column | What goes here |
|---|---|
| Asset | Domain / subdomain / IP / API endpoint / mobile package |
| Type | web / api / network / cloud / mobile |
| Discovery source | Which tool/technique found it (traceable back to the exact subfolder) |
| Tech stack | CMS/framework/server + version if known |
| Auth present? | Y/N — login-gated assets get flagged for manual testing later |
| Exposure level | Critical / High / Medium / Low (see guide below) |
| Priority | High / Medium / Low (see guide below) |
| Known CVEs (from step 07) | |
| Scope status | Confirmed in-scope / needs clarification |
| Notes | |

## Exposure level guide
- **Critical** — directly reachable, handles auth or sensitive data (login, payment, admin panel, API with write access)
- **High** — reachable, no obvious auth, but real functionality (forms, file upload, search with backend query)
- **Medium** — reachable, limited functionality (informational pages with minor interactivity)
- **Low** — static/marketing content only

## Priority guide (what to triage first at handoff)
1. High-value target: auth flows, payment, admin surfaces
2. Old/outdated tech stack: higher known-CVE probability
3. Wide attack surface: multi-role apps, integration points, import/export features
4. Everything else, time permitting

## Practical tip
Keep this as an actual spreadsheet (CSV/Google Sheet), not a markdown table, once an engagement has more than ~20 assets — markdown tables get unmanageable fast and you lose sortability, which matters a lot when triaging by priority column at handoff time.
