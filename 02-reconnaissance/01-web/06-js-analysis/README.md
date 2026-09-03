# JavaScript Analysis

Client-side JS frequently contains API endpoints, internal hostnames, and secrets that developers assumed were "hidden" simply by being in minified code.

## Gathering all JS files
```
cat live_subs.txt | katana -jc -silent | grep "\.js$" | sort -u > js_files.txt
```
`-jc` (JS crawl) follows and extracts JS file references during the crawl, not just HTML links.

## Extracting endpoints and secrets
```
python3 LinkFinder.py -i https://target.com/main.js -o cli
```
LinkFinder specifically extracts URL-like strings (relative and absolute paths, API endpoints) from JS source, including minified files.

```
python3 SecretFinder.py -i https://target.com/main.js -o cli
```
Pattern-matches for common secret formats (AWS keys, Google API keys, JWT-looking strings, generic `api_key=` patterns) directly in JS source.

## Source map recovery
Minified JS often still ships a `.map` file reference in a trailing comment (`//# sourceMappingURL=main.js.map`). If the `.map` file is still accessible on the server, it reconstructs near-original, readable source — a significant find, since it turns black-box JS review into effectively white-box code review.
```
curl -s https://target.com/main.js | tail -1
# check for sourceMappingURL comment, then fetch the .map file directly
```

## Manual review focus areas
- Hardcoded API base URLs (often reveal internal/staging API hosts not found via subdomain enum)
- Comments left in by developers (`// TODO: remove before prod`, `// internal use only`)
- Feature flags or role-check logic implemented client-side (a strong signal for testing server-side enforcement of the same logic)

## Workflow
1. Crawl for all JS files across the live subdomain list
2. LinkFinder pass for endpoints
3. SecretFinder pass for hardcoded secrets
4. Check for accessible source maps on any file that looks build-tool-generated
5. Manual skim of anything flagged as interesting by the automated passes

## Output
Discovered endpoints feed into `02-api/01-endpoint-discovery/` and `05-content-discovery/`; any secrets found are a standalone high-priority finding for the asset inventory.
