# API Endpoint Discovery

Mapping the actual API surface — separate from web content discovery because API endpoints often follow different naming conventions and aren't linked from HTML at all.

## Sources

### From JS analysis (highest yield for SPA/modern web apps)
Already covered in `01-web/06-js-analysis/` — the fetch/axios base URLs and endpoint paths extracted there are usually the single richest source of API endpoints.

### From mobile app teardown
If a mobile app exists for the target, decompiled APK/IPA source frequently contains the full API endpoint list hardcoded, sometimes including internal/staging API hosts not exposed anywhere on the web frontend. See `05-mobile-app/01-apk-ipa-static-recon/`.

### Wordlist-based brute-force (active — log it)
```
ffuf -w api-endpoints-wordlist.txt -u https://target.com/api/FUZZ -mc 200,201,204,400,401,403 -t 30
```
Include 401/403 in match codes — an endpoint returning "unauthorized" still confirms the endpoint exists and is worth noting for later auth-testing, unlike a 404 which means it doesn't exist at all.
Use SecLists' `api/objects.txt` and `api/actions.txt` as a starting wordlist base, combined with resource-name guesses (`users`, `orders`, `admin`, matching whatever domain the app is in).

### Historical/archived discovery
```
gau target.com | grep "/api/" | sort -u
```
Reuses the passive URL pull from web recon, filtered specifically for API-looking paths.

## API versioning discovery
Once a base API path is found, check for older versions explicitly — these frequently lack current security patches or rate-limiting:
```
for v in v1 v2 v3 beta internal; do curl -s -o /dev/null -w "%{http_code} /$v/\n" https://target.com/api/$v/; done
```
An older version responding with 200 while the current version is `/v3/` is a strong signal to prioritize — legacy API versions are a recurring, high-value bug bounty pattern.

## Workflow
1. Extract endpoints from JS analysis output (passive, already gathered)
2. Extract endpoints from mobile teardown if an app exists
3. Passive gau/wayback filter for `/api/` paths
4. Active wordlist brute-force to fill gaps
5. Version-probe every discovered base path

## Output
Full endpoint list feeds into `02-swagger-graphql-leaks/`, `03-parameter-discovery/`, and the asset inventory as individual API-type entries.
