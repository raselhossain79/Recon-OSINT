# Dorking on Alternative Search Engines

Alternative search engines offer different indexing strategies, less aggressive bot detection, and unique data. Critical for comprehensive reconnaissance.

---

## Bing Dorking

### Supported Operators

| Operator | Syntax | Example | Notes |
|----------|--------|---------|-------|
| `site:` | `site:domain.com` | `site:example.com` | Same as Google |
| `inurl:` | `inurl:keyword` | `inurl:admin` | Same as Google |
| `intitle:` | `intitle:keyword` | `intitle:"Index of"` | Same as Google |
| `intext:` | Limited support | `intext:"password"` | Works but less reliable |
| `filetype:` | `filetype:ext` | `filetype:pdf` | Same as Google |
| `contains:` | `contains:filetype` | `contains:exe` | Finds URLs hosting file |
| `ip:` | `ip:address` | `ip:192.168.1.1` | Search by IP (unique to Bing) |
| `url:` | `url:keyword` | `url:admin` | Similar to inurl, sometimes better |

### Bing-Specific Advantages

1. **`ip:` Operator** – Direct IP reconnaissance
   ```
   ip:203.0.113.0                  # Direct IP search
   ip:203.0.113.0/24               # CIDR range (limited support)
   ```

2. **`contains:` Operator** – Find URLs hosting specific files
   ```
   contains:php
   contains:aspx
   contains:pdf
   ```

3. **Less aggressive rate-limiting** compared to Google
   - Can run more queries per hour
   - Headless automation tolerated better

4. **Different Crawler** – Indexes pages Google misses
   ```
   site:example.com filetype:pdf  # May find different PDFs than Google
   ```

### Practical Bing Dorks

```
# Subdomain enumeration
site:example.com inurl:admin
site:*.example.com

# IP-based reconnaissance
ip:203.0.113.1
ip:203.0.113.0
contains:php                            # PHP files anywhere

# File discovery (often better than Google for certain file types)
site:example.com filetype:log
site:example.com filetype:sql
site:example.com filetype:bak

# API discovery
site:example.com inurl:api
site:example.com inurl:swagger

# Cloud storage
ip:203.0.113.0 filetype:json            # From specific IP range
```

### Bing Quirks

- `intitle:` sometimes returns less results than Google (different relevance algorithm)
- `cached:` not supported (use alternative: visit url directly, or use Wayback)
- Quotes `""` work but sometimes inconsistently
- `-` exclusion operator sometimes weaker than Google

---

## DuckDuckGo Dorking

### Supported Operators

| Operator | Syntax | Example | Notes |
|----------|--------|---------|-------|
| `site:` | `site:domain.com` | `site:example.com` | Full support |
| `inurl:` | `inurl:keyword` | `inurl:admin` | Full support |
| `intitle:` | `intitle:keyword` | `intitle:"Index of"` | Full support |
| `intext:` | `intext:keyword` | `intext:"password"` | Full support |
| `filetype:` | `filetype:ext` | `filetype:pdf` | Full support |
| `lang:` | `lang:language` | `lang:en` | Language filtering |
| `region:` | `region:code` | `region:us` | Regional filtering |

### DuckDuckGo Advantages

1. **No tracking** – Respects privacy, less aggressive blocking
2. **Regional results** – `region:` operator helps in geo-targeting
3. **No personalization** – Results same for all users
4. **Good for automation** – Less CAPTCHA triggering

### Practical DuckDuckGo Dorks

```
# Basic reconnaissance
site:example.com inurl:admin
site:example.com filetype:pdf

# Regional variants
site:example.co.uk                      # UK domain
site:example.com.au                     # AU domain
region:us site:example.com              # US results

# Privacy-focused dorking (DDG indexes leaked sites others won't aggressively index)
site:example.com "password" filetype:txt
site:example.com intext:"API_KEY"

# Combined regional + file type
lang:en site:example.com filetype:docx  # English docs on example
region:us site:*.example.com            # US subdomains
```

### DuckDuckGo Quirks

- Results sometimes fewer than Google (smaller index)
- `intext:` works but with different relevance algorithm
- No `cache:` or `link:` operators
- Better for finding exposed content on smaller/niche sites

---

## Yandex Dorking

### Supported Operators

| Operator | Syntax | Example | Notes |
|----------|--------|---------|-------|
| `site:` | `site:domain.com` | `site:example.com` | Full support |
| `inurl:` | `inurl:keyword` | `inurl:admin` | Full support |
| `intitle:` | `intitle:keyword` | `intitle:"Index of"` | Full support |
| `url:` | `url:keyword` | `url:admin` | Alternative to inurl |
| `title:` | `title:keyword` | `title:admin` | Alternative to intitle |
| `text:` | `text:keyword` | `text:"password"` | Alternative to intext |
| `host:` | `host:domain.com` | `host:example.com` | Same as site: |
| `domain:` | `domain:com` | `domain:com` | TLD-based search |
| `lang:` | `lang:code` | `lang:ru` | Language code |
| `rhost:` | `rhost:domain` | `rhost:example.com` | Reverse – pages linking to domain |

### Yandex Advantages

1. **Unique content** – Strong indexing of Russian sites and Eastern European content
2. **Less western-centric** – Different crawler priorities
3. **`rhost:` operator** – Reverse link search (like backlinks)
4. **Larger index than DuckDuckGo**

### Practical Yandex Dorks

```
# Standard reconnaissance
site:example.com intitle:admin
site:example.com inurl:backup filetype:sql

# Russian-language target
lang:ru site:example.ru inurl:admin

# Link analysis (unique to Yandex)
rhost:example.com                       # Pages linking to example.com
rhost:example.com site:competitor.com   # Competitor mentions

# Domain-level search
domain:com inurl:admin "example"        # .com domains with admin and "example"

# Exposed files (Yandex good at indexing less cleaned-up sites)
site:example.com filetype:bak
site:example.com filetype:old
site:example.com filetype:tmp
```

### Yandex Quirks

- Results in Russian; use translation tools for large result sets
- Operator syntax sometimes differs (e.g., `url:` instead of `inurl:`)
- Regional focus on Russia/Eastern Europe; less relevant for Western targets
- Good for finding CVE details and security research in Russian

---

## GitHub Dorking

### Why GitHub Matters

GitHub is the world's largest code repository. Developers often commit secrets, credentials, and configuration directly.

### Supported Search Operators

| Operator | Syntax | Example | Notes |
|----------|--------|---------|-------|
| `repo:` | `repo:user/repo` | `repo:example/api` | Search in repo |
| `user:` | `user:username` | `user:alice` | Search by user |
| `org:` | `org:orgname` | `org:example-corp` | Search org repos |
| `path:` | `path:file/path` | `path:src/config` | Search file path |
| `language:` | `language:python` | `language:python` | Filter by language |
| `filename:` | `filename:app.py` | `filename:config.py` | Exact filename |
| `is:pr` / `is:issue` | `is:pr` | `is:pr` | Pull requests/issues |
| `created:` | `created:>2024-01-01` | `created:>2024-01-01` | Date range |
| `pushed:` | `pushed:>2024-01-01` | `pushed:>2024-01-01` | Last update |

### Critical GitHub Dorks (Secret Hunting)

```
# API Keys & Secrets
filename:.env
filename:.env.local
filename:config.json intext:"api_key"
filename:settings.py intext:"SECRET_KEY"

# AWS Credentials
filename:credentials
filename:.aws/credentials
intext:"AKIA" language:bash

# Database Credentials
intext:"password" filename:config.php
intext:"DB_HOST" intext:"DB_PASS"
intext:"mysql_user" intext:"mysql_password"

# Private Keys
filename:id_rsa
filename:id_dsa
intext:"-----BEGIN PRIVATE KEY-----"
intext:"-----BEGIN RSA PRIVATE KEY-----"

# OAuth Tokens
intext:"refresh_token" filename:config.json
intext:"client_secret" filename:.env
intext:"SLACK_BOT_TOKEN" filename:config

# Company-Specific Secrets
org:example-corp intext:"API_KEY"
org:example-corp filename:.env
repo:example/project intext:"password"

# CI/CD Pipeline Secrets
filename:.github/workflows intext:"secrets"
filename:.gitlab-ci.yml intext:"token"
filename:Jenkinsfile intext:"PASSWORD"

# Dangerous Patterns
intext:"password =" filename:py
intext:"api_key =" filename:js
intext:"AWS_SECRET" language:python
```

### GitHub Best Practices

1. **Use multiple keywords** – `api_key`, `api_secret`, `API_KEY`, `apiKey`
2. **Check file extensions** – `.py`, `.js`, `.json`, `.env`, `.conf`
3. **Filter by recent** – `pushed:>2024-01-01` finds active repos
4. **Combine org + pattern** – `org:target-company intext:"database_password"`
5. **Check forks** – Popular repo forks often have leaked variations

### GitHub Dorking by Target Company

```
# Step 1: Find their GitHub org
site:github.com organization:target-company

# Step 2: Search their repos for secrets
org:target-company filename:.env
org:target-company intext:"password"
org:target-company filetype:json intext:"api_key"

# Step 3: Employee repos (often have personal dev work with company credentials)
user:employee-name@target-company intext:"target-company"
```

---

## Shodan Dorking

### Why Shodan?

Shodan is the "Google of the Internet of Things." It scans and indexes internet-facing devices, services, and banners.

### Supported Operators

| Operator | Syntax | Example | Notes |
|----------|--------|---------|-------|
| `host:` | `host:ip.address` | `host:203.0.113.1` | Exact IP |
| `net:` | `net:ip/cidr` | `net:203.0.113.0/24` | IP range |
| `country:` | `country:code` | `country:US` | ISO country code |
| `city:` | `city:name` | `city:London` | City name |
| `port:` | `port:number` | `port:22` | SSH, HTTP, custom ports |
| `product:` | `product:name` | `product:Apache` | Software/product |
| `version:` | `version:string` | `version:2.4.1` | Specific version |
| `os:` | `os:name` | `os:Linux` | Operating system |
| `hostname:` | `hostname:pattern` | `hostname:example.com` | Hostname pattern |
| `has_ipv6:` | `has_ipv6:true` | `has_ipv6:true` | IPv6 hosts |
| `http.component:` | `http.component:jQuery` | `http.component:jQuery` | Web component |
| `http.status_code:` | `http.status_code:200` | `http.status_code:200` | HTTP response |

### Practical Shodan Dorks

```
# Basic host reconnaissance
host:203.0.113.1
net:203.0.113.0/24

# Regional scanning
country:US city:New York
country:GB net:203.0.113.0/24

# Service enumeration
port:22 country:US                      # SSH servers in US
port:3306 product:MySQL                # Open MySQL instances
port:5432 product:PostgreSQL           # Open PostgreSQL
port:6379 product:Redis                # Open Redis (dangerous!)

# Vulnerability patterns
product:Apache version:2.2             # Old Apache versions
product:IIS version:6.0                # Old IIS
http.status_code:500                   # Error pages (info leak)

# Company-specific reconnaissance
hostname:example.com                    # All IPs for example.com
net:203.0.113.0/24 product:nginx       # Nginx servers in range

# Security-critical services
port:9200 product:Elasticsearch        # Open Elasticsearch
port:27017 product:MongoDB             # Open MongoDB
port:5984 product:CouchDB              # Open CouchDB
port:8086 product:InfluxDB             # Open InfluxDB

# VPN & Remote Access
product:OpenVPN
product:"Fortinet FortiGate"
product:Cisco ASA

# Camera & IoT Exposure
product:Webcam
product:Camera
product:RTSP

# Custom banner searching
"Example Company" city:London           # Banner text search
```

### Shodan Tips

1. **Always verify before testing** – Shodan results are public; verify authorization
2. **Combine operators** – `net:203.0.113.0/24 port:22 country:US`
3. **Use `country:` for scope** – Reduces results to geographic region
4. **Check `version:` for CVEs** – Match to known vulnerabilities
5. **Most exposed services** – Redis, Elasticsearch, MongoDB, Cassandra (no auth by default)

---

## Censys Dorking

### Why Censys?

Similar to Shodan; provides rich certificate data and active scanning.

### Supported Operators

| Query Type | Syntax | Example | Notes |
|----------|--------|---------|-------|
| `ip:` | `ip:203.0.113.1` | `ip:203.0.113.1` | IP address |
| `autonomous_system:` | `autonomous_system:AS1234` | `autonomous_system:AS1234` | ASN |
| `location_country_code:` | `location.country_code:US` | `location.country_code:US` | Country |
| `location_city:` | `location.city:London` | `location.city:London` | City |
| `services.port:` | `services.port:22` | `services.port:22` | Port |
| `services.service_name:` | `services.service_name:SSH` | `services.service_name:SSH` | Service |
| `autonomous_system_name:` | `autonomous_system_name:Verizon` | `autonomous_system_name:Verizon` | ISP/ASN name |

### Practical Censys Dorks

```
# IP and ASN scanning
ip:203.0.113.1
autonomous_system:AS1234

# Geographic targeting
location.country_code:US
location.city:London

# Service enumeration
services.port:22 location.country_code:US
services.service_name:HTTP location.city:London

# Certificate-based reconnaissance (unique to Censys)
# (Requires certificate data; search via certificate SHA-256)
```

### Certificate Transparency Log (CT) Search

Censys aggregates Certificate Transparency logs – find all subdomains from issued certificates:

```
# Via Censys web interface (not command-line operators):
- Search for "example.com" in certificates
- Returns all SANs (Subject Alternative Names)
- Effective subdomain enumeration without dorking
```

---

## FOFA Dorking (Chinese Index)

### Why FOFA?

FOFA is China's leading internet-wide scanner. Good for finding obscure and geographically-diverse targets.

### Supported Operators

```
ip=                                     # IP search
host=                                   # Domain search
port=                                   # Port number
body=                                   # Body content
header=                                 # HTTP header
title=                                  # Page title
domain=                                 # Domain
is_domain=true/false                   # Domain or subdomain
is_ipv6=true/false                     # IPv6 filter
country=                                # Country code
region=                                 # Region code
city=                                   # City name
```

### Example FOFA Dorks

```
host="example.com"
title="admin"
port="3306"
body="MySQL"
header="Server: Apache"
```

---

## Comparison Matrix: When to Use Which?

| Engine | Best For | Advantages | Limitations |
|--------|----------|------------|------------|
| **Google** | General dorking | Largest index, most docs | Aggressive rate limiting |
| **Bing** | IP-based recon | `ip:` operator, less blocking | Smaller index than Google |
| **DuckDuckGo** | Privacy-conscious scan | Less CAPTCHA, no tracking | Limited results |
| **Yandex** | Eastern European targets | Unique index, `rhost:` | Results in Russian |
| **GitHub** | Secret/credential hunting | Specific to code repos | Only public repos |
| **Shodan** | Internet-facing devices | Banner data, CVE matching | Requires registration, paid tiers |
| **Censys** | Certificate + port scanning | CT logs, detailed scanning | API-focused |
| **FOFA** | Geographic diversity | Covers regions others miss | Chinese interface, language barrier |

---

## Recommendation Workflow

1. **Start with Google** – Largest index, most comprehensive
2. **Complement with Bing** – Catches unique results, `ip:` operator
3. **Use GitHub** – Find secrets in target's repos
4. **Run Shodan/Censys** – Scan for exposed services (if authorized)
5. **Try Yandex** – If target has Eastern European presence
6. **Check FOFA** – Final sweep for geographically-diverse results

---

## Legal & Ethical Notes

- **Authorization required** for all reconnaissance
- **CFAA compliance** in US; similar laws in other jurisdictions
- **Rate limiting respect** – Don't hammer search engines
- **Responsible disclosure** if findings expose vulnerabilities
