# Subdomain Enumeration

Aggregating the full subdomain footprint before any active brute-forcing — passive sources first, active only to fill gaps.

## Passive aggregation

```
subfinder -d target.com -silent -all -recursive -o subfinder_subs.txt
```
- `-all` queries every configured source (VirusTotal, crt.sh, Shodan, etc. if API keys are configured — more keys = more coverage)
- `-recursive` re-runs subfinder against found subdomains to catch nested subdomains (`dev.api.target.com`)

```
amass enum -passive -d target.com -o amass_subs.txt
```
- `-passive` guarantees zero direct touch to the target, slower than subfinder but often finds different results due to different source weighting — always run both and merge

```
assetfinder --subs-only target.com > assetfinder_subs.txt
```

### Merge and dedupe
```
cat subfinder_subs.txt amass_subs.txt assetfinder_subs.txt | sort -u > all_subs.txt
```

### Certificate transparency (redundant with `01-osint/01-priority-technical/01-domain-infra-osint/` but worth re-running here as a merge source)
```
curl -s "https://crt.sh/?q=%25.target.com&output=json" | jq -r '.[].name_value' | sort -u >> all_subs.txt
```

## Active brute-force (only if passive coverage looks thin, and scope permits)
```
ffuf -w subdomains-wordlist.txt -u https://FUZZ.target.com -mc 200,301,302,403 -t 40
```
Use SecLists' `subdomains-top1million-5000.txt` as a baseline wordlist; build a custom addition using terms found during org-OSINT (internal product names, team names) for better hit rate than a generic list alone.

## Validation — confirm which subdomains are actually alive
```
cat all_subs.txt | httpx -silent -o live_subs.txt
```
httpx probes each entry with a real HTTP request — this is the first active-touch step in the chain, flag it as such in the note-taking log.

## Workflow
1. subfinder + amass + assetfinder in parallel → merge, dedupe
2. crt.sh merge pass
3. httpx liveness check (active — log it)
4. Only if coverage looks incomplete relative to org size: active ffuf brute-force

## Output
Live subdomain list feeds into `04-tech-fingerprinting/`, `05-content-discovery/`, `09-screenshotting-visual/`, and the asset inventory.
