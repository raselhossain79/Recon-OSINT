# Email & Username OSINT

Establishing the target's naming conventions — needed later for any scope-authorized credential-based testing, and useful for identifying likely admin/developer accounts.

## Techniques

### Email format discovery
Common patterns to test against known employee names (from `02-organization-corporate/` LinkedIn research):
- `firstname.lastname@target.com`
- `firstnamelastinitial@target.com`
- `finitial+lastname@target.com`
- Tools: Hunter.io (free tier gives format confidence + a handful of verified addresses), theHarvester

```
theHarvester -d target.com -b all -l 200
```
`-b all` queries every configured source (search engines, PGP key servers, certificate transparency); `-l` caps result count.

### Public email harvesting from technical sources
- View source of key pages for mailto: links
- DNS TXT/SPF records sometimes reveal internal mail infrastructure providers (`v=spf1 include:_spf.google.com` tells you they're on Google Workspace, for example)
- PDF/DOCX metadata (see `01-osint/02-optional-investigative/04-document-metadata-osint/`) frequently contains author emails

### Username enumeration across services
Once an email format is confirmed, check whether the same local-part is reused as a username on GitHub, GitLab, or internal tools referenced elsewhere in recon — reused usernames across breach data and current infrastructure are a strong signal for targeted (in-scope, authorized) credential testing later.

## Workflow
1. theHarvester pass → raw email list + format guess
2. Confirm format against 2–3 known names from LinkedIn/org research
3. Check SPF/TXT records for mail infrastructure provider
4. Cross-reference resulting email local-parts against `03-breach-leaked-data/` findings

## Output
Confirmed email format + any harvested addresses go into the asset inventory notes and become the input list for scope-authorized credential testing during the actual testing phase.
