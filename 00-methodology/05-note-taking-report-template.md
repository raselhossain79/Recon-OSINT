# 05 — Note-Taking / Report Template

Structure for capturing findings live during recon, before they graduate into the asset inventory or a full vulnerability report.

## Per-target working notes

```
# Target: [name]
# Date started:
# Scope reference: [link/doc]
# Engagement type: [pure technical / includes social-eng]

## Assets discovered this session
- Asset:
- Discovery method (tool + command used):
- In-scope confirmed? (Y/N/needs clarification):
- Notes:

## Tech stack identified
- Component:
- Version (if determinable):
- Source of version info (header/error page/changelog/wp-json/etc.):
- Candidate CVEs to check in step 07:

## Active-recon log (anything that touched the target directly)
- Timestamp:
- Tool + exact command:
- Target endpoint:
- Response summary:

## Flags for follow-up
- [ ] Needs active verification (found passively, unconfirmed)
- [ ] Needs manual testing (business logic, auth flow)
- [ ] Scope-ambiguous — confirm before touching further
- [ ] High-value candidate (auth/payment/admin surface)
```

## Why an active-recon log matters
If a target's security team ever asks about traffic from your IP, you need an exact, timestamped record of every active command run — not a reconstruction from memory. This also protects you: if something breaks on the target's side during your testing window, you can immediately show what you did and didn't do.

## Migration rule
Anything under "Assets discovered" with scope confirmed = Y gets copied into `06-asset-inventory-template.md` at the end of each recon session — don't batch this until the very end of the engagement, it gets lossy.
