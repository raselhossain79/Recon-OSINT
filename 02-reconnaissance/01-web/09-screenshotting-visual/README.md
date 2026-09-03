# Screenshotting / Visual Recon

Bulk visual triage across large asset lists — the fastest way to spot high-value targets (login panels, admin interfaces, default install pages) without manually visiting hundreds of URLs one at a time.

## Tooling
```
gowitness file -f live_subs.txt --threads 5 -P screenshots/
```
`--threads 5` balances speed against not overwhelming the target with simultaneous requests; `-P` sets output directory.

```
aquatone -f live_subs.txt
```
Aquatone additionally clusters visually-similar pages together in its HTML report, which is useful for quickly spotting the one different-looking page among hundreds of near-identical default templates.

## What to look for in the results
- Login panels — flag immediately as high-priority in the asset inventory (auth surfaces get priority per `00-methodology/06-asset-inventory-template.md`)
- Admin/dashboard interfaces exposed without an apparent auth wall
- Default installation pages ("It works!", default Apache/nginx pages, default CMS install wizards) — these indicate a forgotten or misconfigured deployment, often lower-hardened than the main production app
- Error states (500 errors, stack traces visible on the screenshot) — worth a manual follow-up visit
- Visually distinct pages within a large wildcard-scope subdomain set — often indicates a genuinely different application/team rather than a template clone

## Workflow
1. Run gowitness or aquatone across the full live-subdomain list from `02-subdomain-enumeration/`
2. Review the generated report/gallery, sorted or grouped by visual similarity if using aquatone
3. Tag every login/admin/default-install/error-state result directly in the asset inventory with a priority flag

## Output
Visually-flagged high-priority assets get their Priority column bumped in `00-methodology/06-asset-inventory-template.md` — this is often the fastest single step in the whole recon phase for identifying where to focus manual testing time first.
