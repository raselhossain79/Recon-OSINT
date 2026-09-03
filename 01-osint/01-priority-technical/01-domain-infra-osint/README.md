# Domain & Infrastructure OSINT

Passive, zero-touch discovery of everything DNS/certificate/network-ownership related. This is the natural extension of subdomain enumeration — do this before or alongside `02-reconnaissance/01-web/02-subdomain-enumeration/`.

## Techniques

### WHOIS (current + historical)
```
whois target.com
```
Current WHOIS is often privacy-redacted, but historical WHOIS (via services like WhoisFreaks or SecurityTrails) can reveal old registrant emails, org names, and nameserver changes — useful for finding related domains registered by the same org/person.

### DNS history
Past A/MX/NS records can expose infrastructure the target has since migrated away from, including old hosting providers or acquired-company mail servers still pointing somewhere live.
- SecurityTrails (`securitytrails.com`) — free tier gives historical DNS lookups
- DNSDumpster (`dnsdumpster.com`) — free, visual DNS mapping, decent for a first pass

### Certificate transparency
Every publicly-trusted SSL cert is logged. This is one of the highest-signal passive subdomain sources available.
```
curl -s "https://crt.sh/?q=%25.target.com&output=json" | jq -r '.[].name_value' | sort -u
```
Note: results include wildcard entries and expired certs — dedupe and filter obvious noise (e.g., `*.target.com` literal wildcard strings) before feeding into the asset list.

### ASN / BGP-level network ownership mapping
For larger organizations, subdomain enum alone misses infrastructure that doesn't sit under the main domain at all (dedicated IP ranges, acquired company networks).
```
# Find the ASN
whois -h whois.radb.net -- '-i origin AS12345'
# Or via bgp.he.net web UI: search the org name directly
```
Once you have the ASN, pull the full announced IP range and treat it as a candidate scan range (subject to scope confirmation — an ASN owning a range does not automatically mean every IP in it is in scope).

## Workflow
1. WHOIS current + historical → note registrant org name and any sibling domains
2. crt.sh → dump all subdomains ever certified, dedupe
3. DNS history → flag any old infrastructure still resolving
4. ASN/BGP lookup (if target is large enough to have dedicated IP space) → candidate network range

## Output
Feeds directly into: `02-reconnaissance/01-web/02-subdomain-enumeration/` (subdomain list), `02-reconnaissance/03-network/` (IP ranges), and `00-methodology/06-asset-inventory-template.md` (everything confirmed in-scope).
