# Google Dorking Quick Reference (One-Page)

## Basic Operators

| Operator | Example | Purpose |
|----------|---------|---------|
| `site:` | `site:example.com` | Restrict to domain |
| `inurl:` | `inurl:admin` | Match in URL path |
| `intitle:` | `intitle:"Index of"` | Match in page title |
| `intext:` | `intext:"password"` | Match in page content |
| `filetype:` | `filetype:pdf` | Restrict file type |
| `ext:` | `ext:sql` | Alternative to filetype |
| `cache:` | `cache:example.com` | View cached version |
| `link:` | `link:example.com` | Find pages linking to |
| `"..."` | `"exact phrase"` | Exact phrase match |
| `*` | `"password is *"` | Wildcard (any word) |
| `-` | `admin -panel` | Exclude term |
| `\|` or `OR` | `filetype:pdf \| filetype:docx` | OR logic |
| `()` | `(pdf \| docx) site:example.com` | Grouping |

---

## Common Dorks (Ready to Use)

### 🔍 Subdomain & Asset Discovery
```
site:*.{target}
site:*.{target} inurl:admin
site:*.{target} inurl:api
site:*.{target} inurl:staging
site:*.{target} inurl:dev
```

### 🔐 Configuration & Credentials
```
site:{target} filetype:env
site:{target} filetype:conf
site:{target} intext:"API_KEY"
intext:"password" filetype:txt
intext:"DB_PASS" filetype:conf
```

### 📦 Backups & Archives
```
site:{target} filetype:sql
site:{target} filetype:bak
site:{target} filetype:zip
inurl:backup filetype:sql
```

### 🚪 Admin & Login Panels
```
site:{target} inurl:admin
site:{target} inurl:/login
site:{target} intitle:"admin panel"
site:{target} inurl:phpmyadmin
```

### 📂 Directory Listings & Exposed Files
```
intitle:"Index of" site:{target}
site:{target} inurl:.git
site:{target} inurl:.env
site:{target} filetype:log
```

### ☁️ Cloud Storage
```
site:s3.amazonaws.com {target}
site:blob.core.windows.net {target}
site:storage.googleapis.com {target}
```

### 📡 APIs & Documentation
```
site:{target} inurl:/api/
site:{target} inurl:swagger.json
site:{target} inurl:/graphql
site:{target} filetype:json intext:"swagger"
```

### 🐛 Debug & Error Pages
```
intext:"Stack Trace" site:{target}
intext:"Exception" filetype:log
intext:"You have an error in your SQL syntax"
```

### 💻 Source Code Leaks
```
intext:"<?php" filetype:php site:{target}
intext:"password =" filetype:py
site:{target} inurl:.git/config
```

### 👥 Employee & Email OSINT
```
site:{target} filetype:pdf inauthor:"{target}"
intext:"@{target}" filetype:pdf
site:{target} inurl:directory
intext:"employee" filetype:xlsx
```

---

## Search Engine Comparison

| Engine | Pros | Cons | Key Operator |
|--------|------|------|--------------|
| **Google** | Largest index, most docs | Heavy rate-limiting | `site:` |
| **Bing** | Less blocking, unique results | Smaller index | `ip:` |
| **DuckDuckGo** | Privacy, no personalization | Limited results | `lang:` |
| **Yandex** | Eastern European targets | Russian interface | `rhost:` |
| **GitHub** | Secret hunting, code | Repo-specific | `org:` |
| **Shodan** | Device fingerprinting, CVEs | Requires account | `port:`, `product:` |

---

## Attack Surface by Category

| What? | Dork Example | Risk |
|-------|--------------|------|
| Database backup | `site:{target} filetype:sql` | CRITICAL |
| API credentials | `site:{target} intext:"api_key"` | CRITICAL |
| SSH private key | `intext:"PRIVATE KEY"` | CRITICAL |
| .env file | `site:{target} filetype:env` | HIGH |
| AWS credentials | `intext:"AKIA" filetype:txt` | CRITICAL |
| Admin panel | `site:{target} inurl:admin` | HIGH |
| Directory listing | `intitle:"Index of"` | MEDIUM |
| Error page | `intext:"Stack Trace"` | MEDIUM |
| Email addresses | `site:{target} filetype:pdf` | LOW |
| Tech stack info | `site:{target} intext:"powered by"` | LOW |

---

## Best Practices

✅ **DO:**
- Use **`site:`** to scope to target domain
- Combine operators for precision
- Quote sensitive phrases: `"exact match"`
- Add **`-exclusion`** terms to reduce noise
- Use **delays (3–5 sec)** between automated queries
- **Document all findings** with timestamps
- Get **written authorization** first

❌ **DON'T:**
- Run all dorks at once (triggers CAPTCHA)
- Use personal IP without proxy
- Share raw findings publicly
- Download entire S3 buckets
- Test without written scope
- Brute-force found credentials immediately
- Modify/delete findings

---

## Workflow at a Glance

```
1. Subdomain Discovery      → site:*.{target}
2. Tech Stack Identification → site:{target} "powered by"
3. Config File Search       → site:{target} filetype:env
4. Backup File Hunt         → site:{target} filetype:sql
5. Admin Panel Mapping      → site:{target} inurl:admin
6. Directory Enumeration    → intitle:"Index of"
7. Cloud Service Check      → site:s3.amazonaws.com {target}
8. Findings Report          → Compile & prioritize
```

---

## Automation Quick Start

```bash
# Install
pip install selenium requests beautifulsoup4

# Run
python3 03-dork-automation.py -t example.com \
  --delay 5 --format json

# With custom dorks
python3 03-dork-automation.py -t example.com \
  -c custom-dorks.txt -p proxies.txt
```

---

## Common Pitfalls & Fixes

| Problem | Reason | Fix |
|---------|--------|-----|
| CAPTCHA every query | Rate limiting | Increase delay, use proxy |
| No results | Too restrictive | Broaden dork, test manually first |
| Too many results | Too broad | Add `-exclusion` or more filters |
| False positives | Operator behavior | Use quotes, combine operators |
| Results not current | Cached versions | Check `cache:` operator |

---

## Severity Levels

| Level | Examples | Action |
|-------|----------|--------|
| **CRITICAL** | DB creds, private keys, AWS keys | Report immediately, escalate |
| **HIGH** | API keys, admin panel, source code | Report today, prioritize fix |
| **MEDIUM** | Directory listing, staging env, error pages | Include in report, normal priority |
| **LOW** | Tech stack, email format, employee names | Document for context |

---

## Cheat Sheet Reference Map

**Need details?** See full CHEATSHEET.md for:
- All 15+ operator explanations
- 100+ practical dorks by category
- Syntax modifiers & edge cases
- Evasion & optimization techniques

**Need workflow guidance?** See 04-workflow-methodology.md for:
- 7-stage dorking workflow
- Timeline estimates
- Reporting templates
- Legal compliance checklist

**Need automation?** See 03-dork-automation.py for:
- Built-in dork templates
- Proxy rotation
- Rate limiting
- Output formatting (TXT, CSV, JSON)

---

## Useful Links

| Resource | URL |
|----------|-----|
| Google Advanced Search | https://www.google.com/advanced_search |
| Bing Advanced Operators | https://help.bing.microsoft.com/apex/index/18/en-us |
| Shodan Search | https://www.shodan.io/ |
| GitHub Search | https://github.com/search |
| Yandex Search | https://yandex.com/ |

---

**Save this page for quick operator lookup during reconnaissance.**

**Last Updated:** 2024-01-15 | **Version:** 1.0
