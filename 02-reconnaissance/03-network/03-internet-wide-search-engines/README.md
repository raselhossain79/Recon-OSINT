# Internet-Wide Search Engines

Pre-indexed data about exposed services — zero direct requests to the target since you're querying a third party's existing scan/crawl data. Worth checking early in the passive phase, often surfaces infrastructure standard subdomain enumeration misses entirely.

## Shodan
```
shodan search hostname:target.com
shodan search org:"Target Company Name"
shodan search ssl:target.com
```
- `hostname:` filters by resolved hostname
- `org:` filters by the organization name registered against the IP's ASN — useful for catching infrastructure that doesn't resolve under the main domain at all
- `ssl:` matches by the domain present in an SSL certificate, catches hosts serving the target's cert on non-obvious IPs

Favicon hash search (ties directly into `01-web/03-origin-ip-discovery/`):
```
shodan search http.favicon.hash:FAVICON_HASH
```

## Censys
Web UI or `censys search` CLI — similar filters to Shodan (`services.tls.certificates.leaf_data.subject.common_name`, etc.) but with different crawl coverage and update frequency; always cross-check both since results don't fully overlap.

## ZoomEye / FOFA
Regional alternatives with sometimes meaningfully different coverage, particularly for infrastructure hosted outside North America/Europe. Worth a pass especially if OSINT indicated the target's infrastructure or hosting provider is region-specific.

## What this typically surfaces that other techniques miss
- Exposed development/staging servers with real IPs and no CDN in front
- IoT or management interfaces (routers, cameras, industrial control panels) registered under the target's ASN
- Databases or admin panels directly exposed on non-standard ports, invisible to standard web-focused subdomain enumeration

## Workflow
1. Shodan hostname + org + ssl queries
2. Censys cross-check with equivalent filters
3. ZoomEye/FOFA pass if target has non-US/EU infrastructure signals
4. Favicon hash search if origin-IP discovery is in progress

## Output
Any exposed infrastructure found feeds into the asset inventory as a new network-type entry, and into `01-host-discovery/` if it represents a new IP range not previously identified.
