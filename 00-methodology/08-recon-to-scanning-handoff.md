# 08 — Recon → Scanning Handoff

The missing link most checklists skip entirely. This is what happens the moment information gathering ends and active testing begins.

## 1. Final data consolidation
Confirm every finding across every session is in `06-asset-inventory-template.md`. Nothing gets tested that isn't in this sheet — if it's only in a raw tool output file, it doesn't count yet.

## 2. Triage pass
Sort the inventory by Priority column, then within each priority tier, sort by Exposure level. Work top-down. Don't test everything with equal depth — most engagements don't have time for that, and it's the wrong allocation of effort anyway.

## 3. Pull in the vulnerability mapping
For every asset with entries in the "Known CVEs" column from step 07, decide: manual verification first, or straight to a targeted scanner/exploit check.

## 4. Tool selection per asset type
Use `04-master-tool-index.md` plus category-specific knowledge:
- WordPress-identified asset → WPScan with `--enumerate vp,vt` (vulnerable plugins/themes) as a first pass
- Tech-fingerprinted framework → matched nuclei templates (`nuclei -u target -tags <framework>`)
- Parameter-discovery output → sqlmap candidate list built from confirmed injectable-looking params

## 5. Manual vs automated split
| Automated (scanner-appropriate) | Manual (scanner-blind) |
|---|---|
| Known CVE checks | Business logic flaws |
| Generic injection points (SQLi, XSS fuzzing) | Authentication/authorization flow abuse |
| Mass subdomain/endpoint sweeps | Multi-step process manipulation (checkout flows, approval chains) |
| Default credential checks | Race conditions |

## 6. Final scope re-verification
Before the first scanner runs, re-check every asset in the inventory against the original scope document one more time. This is deliberately repeated from step 02 — recon expands the asset list past what you started with, and it's easy to forget that a subdomain found via cert transparency was never actually confirmed in-scope.

## Exit point
Once this checklist is done, the target moves out of this vault. Active testing, exploitation, and reporting live in a separate repo/workflow — this vault's job ends here by design, so it stays focused on information gathering only.
