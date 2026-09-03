# Content Discovery

Finding paths, files, and endpoints not linked from the visible site — the step that usually produces the largest single expansion of attack surface per target.

## Passive first
```
gau target.com | tee gau_urls.txt
waybackurls target.com | tee wayback_urls.txt
cat gau_urls.txt wayback_urls.txt | sort -u > all_historical_urls.txt
```
Validate which are still live before treating them as real assets:
```
cat all_historical_urls.txt | httpx -silent -mc 200,301,302,403 -o live_historical.txt
```

## Active brute-force (log this — generates real traffic)
```
ffuf -w /usr/share/seclists/Discovery/Web-Content/raft-large-directories.txt -u https://target.com/FUZZ -mc 200,301,302,403 -t 40 -o ffuf_dirs.json
```
- `-t 40` = 40 concurrent threads — reduce to 10–15 for rate-limited scope
- `-mc` filters which status codes to report; 403 is worth including since it often reveals a real path that's just access-restricted, useful for later auth-bypass testing

```
gobuster dir -u https://target.com -w wordlist.txt -x php,bak,old,zip,sql -t 30
```
`-x` appends listed extensions to every wordlist entry — critical for catching backup files (`config.php.bak`), archived dumps (`backup.zip`), or exposed SQL exports that a plain directory wordlist would miss.

## Custom wordlist strategy
Generic wordlists (SecLists) get you the baseline. A custom wordlist built from terms already discovered — product names from job postings, internal tool names from tech-fingerprinting, path segments seen in JS analysis — consistently outperforms generic lists for finding target-specific hidden paths. Build this incrementally as recon progresses, don't treat wordlist selection as a one-time decision at the start.

## Crawling (for deeper link discovery beyond brute-force)
```
gospider -s https://target.com -o gospider_output -c 10 -d 3
```
`-d 3` = crawl depth 3 links from the seed URL; `-c 10` = concurrent requests.

## Workflow
1. Passive URL pull (gau + waybackurls) → validate liveness
2. Active brute-force with a general wordlist first
3. Once initial recon (tech-fingerprint, JS analysis) surfaces target-specific terms, run a second brute-force pass with a custom wordlist
4. Crawl for additional linked-but-not-dorked content

## Output
All confirmed-live discovered paths feed into `09-screenshotting-visual/` for triage and into the asset inventory as individual endpoints worth manual review.
