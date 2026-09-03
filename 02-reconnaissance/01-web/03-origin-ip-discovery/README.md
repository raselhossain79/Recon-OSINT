# Origin IP Discovery / WAF Bypass

Most bug bounty targets sit behind Cloudflare or a similar CDN/WAF. Finding the real origin server IP matters for two reasons: it exposes the raw host with no firewall/rate-limiting in front of it, and it prevents you from wasting an entire engagement testing the WAF instead of the actual application.

## Technique 1 — Favicon hashing
Organizations frequently reuse the same favicon across all their infrastructure, including origin servers not yet fronted by the CDN. The favicon hash becomes a fingerprint searchable on Shodan.
```
python3 favUp.py -ff favicon.ico --shodan-cli
python3 favUp.py --web https://target-behind-cloudflare.com -sc
```
`-ff` takes a local favicon file; `--web` fetches it directly from the live site first. `-sc`/`--shodan-cli` triggers the Shodan lookup using the hash (requires a configured Shodan API key).

```
favirecon -u https://target.com/ -v
```
Lightweight single-target favicon recon, useful for a quick check without setting up favUp's dependencies.

```
cat subs.txt | python3 favfreak.py
```
FavFreak checks favicon hashes across an entire subdomain list at once — flags any subdomain whose favicon hash matches the main site but whose resolving IP is *not* a known CDN IP range. That mismatch is your strongest origin-IP candidate.

## Technique 2 — Historical DNS / SSL certificate history
Origin IPs used before CDN adoption frequently persist in historical DNS records even after the domain moves behind Cloudflare.
- SecurityTrails historical DNS lookup for the domain
- Censys/Shodan certificate search for the exact SSL certificate serial/fingerprint currently in use — if the same cert appears on a non-CDN IP, that's a strong origin candidate

```
python3 originIPHunter.py -d target.com
```
Queries multiple public sources for historical IPs in a single pass.

## Technique 3 — Direct IP confirmation
Once you have a candidate IP, confirm it's the real origin (not a coincidence) by sending a request with the Host header spoofed:
```
curl -s -H "Host: target.com" https://CANDIDATE_IP/ -k
```
If the response matches the real site's content, you've confirmed the origin. **This is active recon — it directly touches a candidate host — log it in the note-taking template.**

## Workflow
1. WAF detection first (`04-firewall-waf-detection/`) — only worth pursuing origin-IP discovery if a WAF/CDN is actually in front of the target
2. Favicon hash → Shodan search
3. FavFreak across full subdomain list for mismatches
4. Historical DNS/cert cross-check
5. Confirm candidate with Host-header curl request (active, log it)

## Output
Confirmed origin IP goes into the asset inventory as a separate high-priority entry — testing against it directly (with scope permission) bypasses WAF-level rate limiting and filtering that would otherwise mask real findings.
