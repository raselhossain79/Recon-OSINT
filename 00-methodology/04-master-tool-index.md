# 04 — Master Tool Index

Single lookup table tying every phase to its tools. For each tool: whether it's already in Kali, how to install it if not, whether it needs an API key, where to get that key, and where to put it.

## How to read the "Kali default?" column
- **Yes** — already installed on a standard Kali image, just run it
- **No** — needs manual install (clone/pip/go install), command given
- **Partial** — package exists in Kali repos but often an old version; manual install recommended for latest features

---

## Passive recon

| Tool | Purpose | Kali default? | Install | API key needed? | Where to get it | Where to put it | Why needed |
|---|---|---|---|---|---|---|---|
| **subfinder** | Subdomain aggregation | No | `go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest` | Optional (boosts results) | Free API keys from each source (VirusTotal, Censys, etc.) — sign up individually | `~/.config/subfinder/provider-config.yaml` | Without keys it still works using free sources; with keys it queries more sources and finds more subdomains |
| **amass** | Subdomain aggregation | Partial (old version in repos) | `sudo apt install amass` or `go install -v github.com/owasp-amass/amass/v4/...@master` for latest | Optional | Same idea as subfinder — per-source keys | `~/.config/amass/config.yaml` | Same reason — more sources = more coverage |
| **assetfinder** | Subdomain aggregation | No | `go install github.com/tomnomnom/assetfinder@latest` | No | — | — | Simple, no-key subdomain source, good to run alongside the above two |
| **crt.sh** | Certificate transparency lookup | N/A (web/curl query) | None — just `curl` | No | — | — | Free public service, no auth needed |
| **Shodan CLI** | Internet-wide search, favicon hash search | No | `pip3 install shodan --break-system-packages` | **Yes, required** | Sign up free at `shodan.io` → account page has your API key | `shodan init YOUR_API_KEY` (saves it to `~/.shodan/api_key`) | Shodan blocks meaningful search without an API key — free tier gives limited but usable query credits/month |
| **Censys CLI** | Internet-wide search, cross-check vs Shodan | No | `pip3 install censys --break-system-packages` | **Yes, required** | Sign up free at `censys.io` → API section in account settings | `censys config` (prompts and saves credentials locally) | Same as Shodan — API-gated, free tier has a query cap |
| **theHarvester** | Email/subdomain harvesting from search engines | Yes | Already installed | Optional (some sources need keys) | Hunter.io, Shodan keys plug in for extra sources | `/etc/theHarvester/api-keys.yaml` | Works without keys using free sources; keys unlock extra data sources like Hunter.io |
| **Hunter.io** | Email format discovery | N/A (web service) | None | Yes, for automation/API use | Free tier at `hunter.io` → API key in dashboard | Pass as a request parameter when scripting against their API | Free web UI works without a key for a few lookups/month; API automation requires the key |
| **trufflehog** | GitHub secret scanning (full commit history) | No | `pip3 install trufflehog --break-system-packages` or `go install github.com/trufflesecurity/trufflehog/v3@latest` | Optional (GitHub token raises rate limits) | GitHub → Settings → Developer settings → Personal access tokens | `export GITHUB_TOKEN=your_token` before running, or `trufflehog github --token=your_token` | Without a token you hit GitHub's low unauthenticated API rate limit fast when scanning a whole org |
| **gitleaks** | GitHub secret scanning (pattern-based, second pass) | No | `go install github.com/gitleaks/gitleaks/v8@latest` | No | — | — | Runs locally against a cloned repo, no API involved |
| **gau** | Historical URL pulling (Wayback + Common Crawl + OTX) | No | `go install github.com/lc/gau/v2/cmd/gau@latest` | No | — | — | Free public archive sources, no auth |
| **waybackurls** | Historical URL pulling (Wayback only) | No | `go install github.com/tomnomnom/waybackurls@latest` | No | — | — | Same, no auth |

---

## Active web/network recon

| Tool | Purpose | Kali default? | Install | API key needed? | Notes |
|---|---|---|---|---|---|
| **nmap** | Host discovery, port/service scan | Yes | Already installed | No | Core tool, always available |
| **masscan** | Fast large-range port scan | Yes | Already installed | No | — |
| **httpx** | Liveness check + tech-detect across host lists | No | `go install github.com/projectdiscovery/httpx/cmd/httpx@latest` | No | — |
| **ffuf** | Content/subdomain/parameter brute-forcing | Yes | Already installed | No | — |
| **gobuster** | Content discovery (alternative to ffuf) | Yes | Already installed | No | — |
| **gospider / hakrawler** | Crawling for link discovery | No | `go install github.com/jaeles-project/gospider@latest` | No | — |
| **wafw00f** | WAF/firewall fingerprinting | Yes | Already installed | No | — |
| **whatweb** | Tech fingerprinting | Yes | Already installed | No | — |
| **gowitness** | Bulk screenshotting | No | `go install github.com/sensepost/gowitness@latest` | No | — |
| **aquatone** | Bulk screenshotting with visual clustering | No | Download binary release from `github.com/michenriksen/aquatone/releases` | No | — |
| **wpscan** | WordPress enumeration | Yes | Already installed | **Yes, for vuln-DB annotation** | Free account at `wpscan.com` → API token in profile (25 requests/day free tier). Pass via `--api-token YOUR_TOKEN`. Without it, wpscan still enumerates plugins/themes/users, but results won't be auto-annotated with known CVEs |

---

## JS analysis & GitHub recon

| Tool | Purpose | Kali default? | Install | API key needed? | Notes |
|---|---|---|---|---|---|
| **katana** | JS-aware crawling | No | `go install github.com/projectdiscovery/katana/cmd/katana@latest` | No | — |
| **LinkFinder** | Extract endpoints from JS | No | `git clone https://github.com/GerbenJavado/LinkFinder.git` then `pip3 install -r requirements.txt --break-system-packages` | No | — |
| **SecretFinder** | Extract secrets from JS | No | `git clone https://github.com/m4ll0k/SecretFinder.git` then `pip3 install -r requirements.txt --break-system-packages` | No | — |

---

## API recon

| Tool | Purpose | Kali default? | Install | API key needed? | Notes |
|---|---|---|---|---|---|
| **arjun** | Hidden parameter discovery | No | `pip3 install arjun --break-system-packages` | No | — |
| **x8** | Hidden parameter discovery (faster) | No | `cargo install x8` (needs Rust installed) or download release binary | No | — |
| **graphql-cop** | GraphQL misconfig/introspection scanner | No | `git clone https://github.com/dolevf/graphql-cop.git` then `pip3 install -r requirements.txt --break-system-packages` | No | — |
| **InQL** | GraphQL schema explorer (Burp extension) | No | Install via Burp Suite's BApp Store directly inside Burp | No | Only useful if you already work inside Burp Suite |

---

## Cloud recon

| Tool | Purpose | Kali default? | Install | API key needed? | Notes |
|---|---|---|---|---|---|
| **cloud_enum** | Multi-cloud bucket/resource enumeration | No | `git clone https://github.com/initstring/cloud_enum.git` then `pip3 install -r requirements.txt --break-system-packages` | No | — |
| **S3Scanner** | S3-specific bucket scanning | No | `pip3 install s3scanner --break-system-packages` | No (AWS creds optional) | Anonymous checks work without AWS credentials; having a free-tier AWS account configured (`aws configure`) unlocks a few extra checks but isn't required |
| **GrayhatWarfare** | Indexed public bucket search | N/A (web service) | None | Yes, for API/bulk search | Free account at `buckets.grayhatwarfare.com` → API key in account settings | Web search works without login for basic use; API key needed for automated/bulk queries |

---

## Mobile recon

| Tool | Purpose | Kali default? | Install | API key needed? | Notes |
|---|---|---|---|---|---|
| **apktool** | APK decompilation (manifest, smali) | Partial | `sudo apt install apktool` (or download latest jar from apktool.org if repo version is outdated) | No | — |
| **jadx** | APK decompilation (readable Java-like source) | No | `sudo apt install jadx` or download from `github.com/skylot/jadx/releases` | No | — |
| **MobSF** | Automated mobile static analysis | No | `docker pull opensecurity/mobile-security-framework-mobsf` then `docker run -it -p 8000:8000 opensecurity/mobile-security-framework-mobsf` | No | Runs as a local web service at `localhost:8000` once the container is up — needs Docker installed |

---

## Network internal (SMB/SNMP)

| Tool | Purpose | Kali default? | Install | API key needed? | Notes |
|---|---|---|---|---|---|
| **enum4linux** | SMB enumeration | Yes | Already installed | No | — |
| **smbclient** | SMB null-session check | Yes | Already installed | No | — |
| **snmpwalk** | SNMP enumeration | Yes | Already installed (`snmp` package) | No | — |

---

## Origin IP discovery (manual install required for all three)

| Tool | Purpose | Install | API key needed? | Where to get it | Where to put it |
|---|---|---|---|---|---|
| **favUp** | Favicon hash → Shodan origin IP search | `git clone https://github.com/pielco11/fav-up.git` then `cd fav-up && pip3 install -r requirements.txt --break-system-packages` | **Yes** (Shodan) | Same Shodan key as above | Pass with `--shodan-cli` flag, or set up via `shodan init` once — favUp reuses the same saved key |
| **FavFreak** | Bulk favicon hash checking across subdomain lists | `git clone https://github.com/devanshbatham/FavFreak.git` — Go-based, needs `go build` inside the folder | No directly, but pairs with Shodan for the actual IP lookup step | — | — |
| **originIPHunter** | Historical-IP aggregation from multiple sources | `git clone` from its GitHub repo, install per its README (dependencies vary by version) | Varies — check the specific repo's README, some source integrations are API-gated | Per-source, listed in that tool's own README | Per-source | Different forks/versions of this tool exist with different dependencies — always check the specific repo's README at install time since flags/keys change between versions |

---

## Quick-reference: which API keys to set up first

If starting from zero, get these free-tier keys before your first real engagement — they're reused across the most tools in this vault:

1. **Shodan** (`shodan.io`) — used directly, and by favUp
2. **Censys** (`censys.io`) — cross-check against Shodan
3. **WPScan** (`wpscan.com`) — only if targets are likely to run WordPress
4. **GitHub personal access token** — raises trufflehog's rate limit significantly for org-wide scans

All four are free-tier available and take under 5 minutes each to sign up for.
