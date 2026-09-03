# Technology Fingerprinting

Identifying CMS, framework, server software, and exact versions — this output feeds directly into `00-methodology/07-tech-stack-vuln-mapping.md`, so precision matters more here than almost anywhere else in the vault.

## Techniques

### Automated fingerprinting
```
whatweb -a 3 https://target.com
```
`-a 3` = aggressive mode, sends additional requests to confirm plugin/version guesses beyond passive header inspection — still relatively low-footprint but is active recon, not passive.

```
httpx -silent -tech-detect -title -status-code -l live_subs.txt -o tech_report.txt
```
Runs tech-detection across an entire subdomain list in one pass — the efficient choice once you have more than a handful of live hosts.

Wappalyzer browser extension or `wappalyzer-cli` for manual spot-checks on individual high-value assets.

### Manual version confirmation (higher precision than automated tools alone)
- HTTP response headers: `Server:`, `X-Powered-By:`, `X-Generator:`
- HTML source: `<meta name="generator">` tags (WordPress, Drupal, and many CMSs include this by default unless explicitly stripped)
- Error pages: forcing a 404 or 500 error sometimes reveals stack traces with exact framework/library versions (especially on non-production-hardened staging environments)
- Changelog/readme files: `/CHANGELOG.md`, `/readme.html`, `/package.json` if directly accessible

### JS framework detection
- Check for framework-specific global variables in browser dev console (`window.__NEXT_DATA__` for Next.js, `window.ng` for Angular, React DevTools detection)
- `/static/js/` or `/_next/` path patterns often reveal build tooling and sometimes version numbers in bundled filenames

## Workflow
1. httpx tech-detect across full live subdomain list (fast, one pass)
2. whatweb aggressive mode on flagged high-value assets for deeper confirmation
3. Manual header/meta-tag/error-page check on anything whatweb/httpx left ambiguous
4. Record exact version (not just product name) against each asset

## Output
Every confirmed tech + version goes directly into `00-methodology/06-asset-inventory-template.md` "Tech stack" column and becomes input for `00-methodology/07-tech-stack-vuln-mapping.md`.
