# 04 — Master Tool Index

Single lookup table tying every phase to its tools. Update this whenever a new tool gets added anywhere in the vault — this file is meant to answer "what do I run right now" in one glance.

## Passive phase

| Purpose | Tool | Command | Notes |
|---|---|---|---|
| Subdomain aggregation | subfinder | `subfinder -d target.com -silent -all -recursive -o subs.txt` | `-all` hits every configured source; `-recursive` re-runs on found subdomains |
| Subdomain aggregation | amass | `amass enum -passive -d target.com -o amass_subs.txt` | `-passive` = zero active touch; slower but wider source coverage than subfinder |
| Cert transparency | crt.sh | `curl -s "https://crt.sh/?q=%25.target.com&output=json" \| jq -r '.[].name_value' \| sort -u` | Free, no rate limit issues, catches historical certs too |
| Internet-wide search | Shodan | `shodan search hostname:target.com` | Pre-indexed — zero direct requests to target |
| Internet-wide search | Censys | web UI or `censys search` CLI | Good cross-reference against Shodan, different crawl coverage |
| Code leak search | trufflehog | `trufflehog github --org=target-org` | Scans full commit history, not just current files |
| Historical URLs | gau | `gau target.com \| tee urls.txt` | Pulls from Wayback, Common Crawl, AlienVault OTX in one pass |

## Active phase (confirm scope allows this first)

| Purpose | Tool | Command | Notes |
|---|---|---|---|
| Host discovery | nmap | `nmap -sn -iL live_hosts_candidates.txt -oG ping_sweep.txt` | `-sn` = no port scan, just up/down |
| Port/service scan | nmap | `nmap -sV -sC -p- -T4 target_ip -oA full_scan` | `-sV` version detect, `-sC` default scripts, `-p-` all 65535 ports, `-T4` aggressive timing — drop to `-T2` if rate-limited scope |
| Fast large-range scan | masscan | `masscan -p1-65535 10.0.0.0/8 --rate=1000 -oG masscan_out.txt` | Use before nmap on huge ranges, then feed live IPs into nmap for depth |
| Subdomain brute-force (active) | ffuf (DNS mode) | `ffuf -w subdomains.txt -u https://FUZZ.target.com -mc 200,301,302` | Only if passive aggregation missed coverage |
| Content discovery | ffuf | `ffuf -w wordlist.txt -u https://target.com/FUZZ -mc 200,301,302,403 -t 40` | `-t` = thread count, tune down for rate-limited scope |
| Content discovery | gobuster | `gobuster dir -u https://target.com -w wordlist.txt -x php,bak,old` | `-x` appends extensions worth guessing |
| Screenshotting | gowitness | `gowitness file -f live_urls.txt --threads 5` | Visual triage across hundreds of hosts fast |
| WAF fingerprint | wafw00f | `wafw00f https://target.com` | Run before deciding whether origin-IP discovery is worth the effort |
| Origin IP via favicon | favUp | `python3 favUp.py -ff favicon.ico --shodan-cli` | Requires Shodan API key |

## Category-specific tools (see the relevant subfolder for full flag breakdowns)
- WordPress: WPScan
- GraphQL: InQL, graphql-cop
- Parameter discovery: arjun, x8
- Mobile: apktool, jadx, MobSF
- Cloud buckets: S3Scanner, cloud_enum

## Decision rule for tool selection
1. Is there a passive option that gets 80% of the same data? Use it first.
2. Does scope explicitly permit active touch for this asset? If unclear, don't run it — flag and ask.
3. Is the target rate-limited? If yes, drop thread counts and timing templates before running anything active.
