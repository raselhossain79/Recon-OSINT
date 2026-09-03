# Firewall / WAF Detection

Identifying WAF/firewall presence and vendor — this decides whether pursuing origin-IP discovery (`01-web/03-origin-ip-discovery/`) is worth the effort, and shapes expected behavior during later active testing (blocked payloads, rate-limit triggers).

## Tooling
```
wafw00f https://target.com
```
Sends a small set of probe requests with known WAF-triggering patterns and matches the resulting response signatures against a database of known WAF vendors (Cloudflare, Akamai, Imperva, AWS WAF, etc.).

## Manual confirmation
- Response header inspection: `Server: cloudflare`, `X-Sucuri-ID`, or similar vendor-specific headers appear directly in many cases even without active probing
- Send a deliberately WAF-triggering test payload (e.g., a basic `<script>` tag or `' OR '1'='1` in a query parameter) and observe whether the response is a generic error, a vendor-branded block page, or unusually fast (suggesting edge-level blocking before reaching the origin at all)

## Decision this feeds
| WAF detected? | Action |
|---|---|
| Yes, strong | Prioritize `01-web/03-origin-ip-discovery/` — testing directly against origin bypasses WAF-level filtering and gives more accurate results |
| Yes, weak/partial | Note it, but origin-IP discovery may be lower priority — some findings will still show through the WAF |
| No | Skip origin-IP discovery entirely, focus recon time elsewhere |

## Workflow
1. wafw00f automated pass
2. Manual header check as a cross-confirmation
3. Optional: single deliberate test payload to observe block behavior (log as active recon)
4. Decide whether origin-IP discovery is worth pursuing based on result

## Output
WAF vendor + confidence level recorded in the asset inventory; directly informs whether `01-web/03-origin-ip-discovery/` gets prioritized for this target.
