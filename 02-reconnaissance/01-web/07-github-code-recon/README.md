# GitHub / Code Recon

Secrets and internal endpoints accidentally committed to source control — including in commit history that's no longer visible in the current file tree.

## Automated secret scanning
```
trufflehog github --org=target-org
```
Scans every repo under the org, including full commit history — a secret removed in a later commit but present in an earlier one is still found, since trufflehog walks the full git history rather than just the current HEAD.

```
gitleaks detect --source=. --report-path=gitleaks_report.json
```
Run locally against any cloned target-related repo for a second detection pass with different pattern rules than trufflehog — the two tools catch different subsets in practice, worth running both on high-value repos.

## Manual GitHub dorking
GitHub's native code search supports targeted queries:
```
org:target-org "api_key"
org:target-org "BEGIN RSA PRIVATE KEY"
org:target-org "target.com" extension:env
```
Check both the organization's own repos and forks — a secret committed once and later removed from the main repo can persist in a fork that never got the fix.

## What to check beyond the main branch
- Deleted-but-cached commits: GitHub retains dangling commits for a period even after force-pushes or deletions; tools like `git log --all` on a full clone (not a shallow clone) surface these
- Issue and PR discussion threads: developers sometimes paste config snippets or error logs containing secrets directly into GitHub issues, which standard code-scanning tools don't check since they only scan file content
- Gists: search separately, they're not covered by org-scoped repo scans

## Workflow
1. Identify the target's GitHub org/user presence (often found via employee LinkedIn profiles or the company's own engineering blog)
2. trufflehog + gitleaks pass across all public repos
3. Manual dork queries for common secret patterns
4. Check forks and gists separately
5. Skim recent issues/PRs for pasted config or logs

## Output
Any confirmed secret (API key, credential, internal endpoint) is a high-priority finding — record it in the asset inventory and flag for immediate scope-appropriate handling per `00-methodology/02-scope-and-legal-checklist.md`.
