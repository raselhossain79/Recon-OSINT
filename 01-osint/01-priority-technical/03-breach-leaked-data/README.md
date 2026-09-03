# Breach & Leaked Data OSINT

Highest legal/ethical sensitivity in the entire vault. Read `00-methodology/02-scope-and-legal-checklist.md` again before acting on anything found through this file — "found publicly" does not automatically mean "safe to use."

## Techniques

### Breach-notification services
- Have I Been Pwned domain search (`haveibeenpwned.com/DomainSearch`) — requires domain ownership verification for full results, but the public breach list itself (which breaches exist, roughly how many accounts) is useful even without verification
- DeHashed / similar paid services — only use if the engagement scope and budget explicitly cover this; treat any credential data retrieved as sensitive regardless of source

### Paste-site monitoring
- Search Pastebin, Ghostbin, and similar sites for the target's domain name or known internal hostnames
- Automated: `psbdmp.ws` API for historical Pastebin search by keyword

### What to actually do with found credentials
1. Never attempt to log in with found credentials unless the engagement scope explicitly authorizes credential testing.
2. Record the exposure itself as a finding (e.g., "N employee credentials found in a 2019 third-party breach, still appear to follow the current password policy pattern") — the exposure is the reportable issue, not proof you tested it.
3. If scope does authorize credential testing, that testing belongs in the scanning/exploitation repo, not this vault — this vault stops at discovery.

## Workflow
1. HIBP domain search → breach count and rough scope of exposure
2. Paste-site search → any live/recent leaks specific to the target
3. Cross-reference exposed email formats against `04-email-username-osint/` findings

## Output
Feeds into `00-methodology/06-asset-inventory-template.md` as a risk note, and into the eventual report as a finding in its own right — exposed credential volume is frequently a reportable issue even before any testing happens.
