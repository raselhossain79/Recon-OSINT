# 07 — Tech Stack → Known Vulnerability Mapping

The bridge between "what did recon find" and "what does scanning test." This step is pure intel work — it produces zero new requests to the target beyond what recon already made.

## Process

### Step 1 — Confirm exact version, not just the product name
"WordPress" isn't enough — you need "WordPress 6.4.2." Sources, in order of reliability:
- `/wp-json` REST API root (returns version in some configs)
- HTML meta generator tag (`<meta name="generator" content="WordPress 6.4.2">`)
- Changelog files left accessible (`/readme.html`, `/CHANGELOG.md`)
- HTTP response headers (`Server:`, `X-Powered-By:`)
- JS bundle comments / source maps

### Step 2 — Cross-reference against vulnerability databases
| Source | Best for |
|---|---|
| NVD (nvd.nist.gov) | Canonical CVE records, CVSS scoring |
| Exploit-DB | Working public exploit code, confirms exploitability not just theoretical risk |
| Vulners | Aggregates multiple feeds, good for fast lookup by product+version |
| WPScan vulnerability DB | WordPress-specific — plugin/theme CVEs, most general databases under-cover this |
| npm audit / Snyk | JS dependency vulnerabilities, relevant when JS analysis reveals package.json/lockfile exposure |

### Step 3 — Record directly against the asset
Every match goes into the "Known CVEs" column of `06-asset-inventory-template.md` — never keep this in a separate file, it needs to travel with the asset for triage.

### Step 4 — Flag severity for triage priority
- Unauthenticated RCE or critical CVE on an in-scope, reachable version → top of the priority queue at handoff
- Old CVE with no public exploit and requires specific misconfig → note it, but don't over-prioritize; verify manually later rather than assuming exploitability

## Common mistake to avoid
Treating "outdated version" as automatically vulnerable. Many CVEs require a specific configuration or authenticated context to be exploitable — this step identifies *candidates* to verify manually or with a targeted scanner during the actual testing phase, not confirmed bugs.
