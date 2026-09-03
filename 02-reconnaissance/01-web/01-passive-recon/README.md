# Passive Web Recon

Zero direct-touch information gathering — establishes a baseline picture before any active technique runs. Always the first step in the web recon phase.

## Techniques

### Google dorking
Search operators to surface exposed files, panels, and misconfigurations already indexed by Google.
```
site:target.com filetype:pdf
site:target.com inurl:admin
site:target.com intitle:"index of"
site:target.com ext:sql | ext:env | ext:log
site:target.com inurl:wp-content/uploads filetype:sql
```
`intitle:"index of"` catches exposed directory listings; `ext:env` specifically hunts for leaked environment config files, one of the highest-value dork patterns for finding hardcoded secrets.

### Wayback Machine / archive.org
Historical snapshots reveal old endpoints, parameters, and pages that may still be live but no longer linked.
```
curl -s "http://web.archive.org/cdx/search/cdx?url=target.com/*&output=text&fl=original&collapse=urlkey" > wayback_urls.txt
```
Or use `waybackurls target.com` / `gau target.com` for a cleaner CLI pass across Wayback + Common Crawl + AlienVault OTX simultaneously.

### robots.txt and sitemap.xml
```
curl -s https://target.com/robots.txt
curl -s https://target.com/sitemap.xml
```
`Disallow:` entries in robots.txt are effectively a hint list of paths the target doesn't want indexed — often the most interesting paths to check manually. sitemap.xml gives a structured map of intended-public content, useful as a baseline to compare against what content-discovery later finds that *isn't* in the sitemap.

### Third-party leak sources
Already covered in depth in `01-osint/01-priority-technical/03-breach-leaked-data/` — cross-reference rather than duplicate here.

## Workflow
1. Dork pass (5–10 targeted queries, not a blind scattergun)
2. Wayback/gau pull → dedupe against dork results
3. robots.txt + sitemap.xml → compare disallowed paths against what's publicly linked

## Output
Feeds every URL/path found into `05-content-discovery/` for validation (many wayback URLs are dead — confirm which are still live) and into `04-tech-fingerprinting/` if any leaked file reveals stack details.
