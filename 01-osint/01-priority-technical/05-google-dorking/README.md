# Google Dorking Module

## Overview

Comprehensive reference library for **Google Dorking** — a reconnaissance technique using advanced search operators to discover exposed information, misconfigurations, and sensitive files on target infrastructure.

This module is part of the **Recon-OSINT-Vault** penetration testing and bug bounty reconnaissance toolkit.

---

## What is Google Dorking?

Google Dorking leverages Google's advanced search operators to find:

- **Exposed credentials** (API keys, database passwords, private keys)
- **Configuration files** (.env, settings, database configs)
- **Backup & archive files** (SQL dumps, encrypted backups)
- **Access points** (admin panels, login forms, API endpoints)
- **Directory listings** & misconfigurations
- **Leaked source code** (GitHub, publicly-accessible repos)
- **Cloud storage** exposure (S3, Azure Blob, GCS)
- **Technology stack information** (framework, version, dependencies)
- **Employee & organizational data** (email, documents, metadata)

**Legality:** Dorking itself is legal (you're using Google's public search); *what you do with findings* determines legality. Always obtain written authorization before targeting.

---

## Module Structure

```
01-google-dorking/
├── README.md                           # This file
├── 00-when-to-use-what.md             # Decision guide: which categories per engagement type
├── CHEATSHEET.md                       # Comprehensive operator & syntax reference
├── 01-google-dorks-by-target.md       # Organized dorks by reconnaissance goal
├── 02-alternative-search-engines.md   # Bing, DuckDuckGo, Yandex, GitHub, Shodan, Censys
├── 03-dork-automation.py              # Python automation tool
├── 04-workflow-methodology.md         # Pentest/red team workflow & methodology
├── examples/
│   ├── example-dorks-custom.txt       # Sample custom dork file
│   ├── example-proxies.txt            # Sample proxy list format
│   └── example-findings-report.md     # Sample findings report
└── quick-reference.md                 # Single-page quick lookup
```

---

## Which Categories Do I Actually Use?

**You never run every category on every engagement.** This repo is a reference library — scope and engagement type decide what's relevant. See **`00-when-to-use-what.md`** for the full decision guide, broken down by:

- Web application pentest
- API / Web+API pentest (your primary focus area)
- Red team / full organization assessment
- Bug bounty (narrow scope, program rules apply)

**Read that file first** before running the automation script or picking dorks from the target-category list below.

---

## Quick Start

### 1. For Manual Dorking

Use **CHEATSHEET.md** as your reference:
- All operators explained with examples
- Real-world dorks organized by target type
- Common pitfalls and workarounds
- Comparison table for alternative search engines

```bash
# Example: Find exposed .env files on example.com
site:example.com filetype:env

# Example: Find admin panels
site:example.com inurl:admin intitle:"login"

# Example: Search alternative engines (Shodan)
port:3306 product:MySQL country:US
```

### 2. For Automated Dorking

Use **03-dork-automation.py** for large-scale reconnaissance:

```bash
# Install dependencies
pip install selenium requests beautifulsoup4

# Generate and run dorks for example.com
python3 03-dork-automation.py -t example.com -o results.txt

# Use custom dorks file with proxies
python3 03-dork-automation.py -t example.com -c custom-dorks.txt \
  -p proxies.txt --delay 5 --format json

# Specific categories only
python3 03-dork-automation.py -t example.com \
  --categories subdomain_discovery,config_files --delay 3
```

### 3. For Workflow Integration

Use **04-workflow-methodology.md** to integrate dorking into your pentest phases:

- **Stage 1:** Preparation (5–10 min)
- **Stage 2:** Subdomain discovery (20–40 min)
- **Stage 3:** Sensitive information hunting (30–60 min)
- **Stage 4:** Access point discovery (20–40 min)
- **Stage 5:** Directory & file enumeration (10–20 min)
- **Stage 6:** Cloud & third-party services (10–20 min)
- **Stage 7:** Findings compilation (10 min)

**Total time: 1.5–3 hours per target** (varies by organization size)

---

## File Descriptions

### CHEATSHEET.md
**Comprehensive reference for all operators and syntax**

- **Basic Operators:** `site:`, `inurl:`, `intitle:`, `intext:`, `filetype:`, etc.
- **Advanced Operators:** Quotes, wildcards, `-` exclusion, `|` OR, parentheses
- **Syntax Modifiers:** Case sensitivity, URL encoding, TLDs, numeric ranges
- **Practical Patterns:** 15+ categories with real-world examples
- **Evasion & Optimization:** CAPTCHA avoidance, automation tips
- **Common Pitfalls:** Mistakes to avoid and how to fix them
- **Quick Reference Table:** All operators at a glance

**When to use:** Anytime you need to understand an operator or craft a dork manually.

---

### 01-google-dorks-by-target.md
**Organized dork collections by reconnaissance goal**

16 major categories:

1. **Subdomain & Asset Discovery** — Find all target infrastructure
2. **Exposed Configuration** — .env, .conf, .ini, .xml files
3. **Exposed Credentials** — Passwords, API keys, SSH keys, tokens
4. **Backup & Archive Files** — SQL dumps, .zip, .bak, .old
5. **Directory Listings** — Misconfigured web servers
6. **Debug & Error Pages** — Stack traces, exception details
7. **Login & Admin Panels** — CMS, control panels, databases
8. **Exposed Credentials (Lists)** — User databases, employee info
9. **Cloud Storage** — S3, Azure, GCS exposure
10. **API Documentation** — Swagger, GraphQL, Postman
11. **Source Code Leaks** — PHP, JavaScript, Python, Java, IaC
12. **CI/CD & DevOps** — Jenkins, GitLab, GitHub Actions, monitoring
13. **Metadata & OSINT** — Documents, author info, timestamps
14. **Employee & Organizational** — Directories, email, contact info
15. **Vulnerable Parameter Patterns** — SQLi, file inclusion, SSRF, open redirect
16. **Third-Party Dependencies** — npm, pip, Maven, Bundler

Each category includes:
- Multiple dork variations
- Real-world examples
- What to expect in findings
- How to validate results
- Next steps (what to do with findings)

**When to use:** Pick category matching your reconnaissance goal, copy dorks, adapt to target.

---

### 02-alternative-search-engines.md
**Dorking beyond Google**

Covers:

- **Bing** — IP-based search (`ip:` operator), less rate limiting
- **DuckDuckGo** — Privacy-focused, regional filtering, smaller index
- **Yandex** — Russian-language targets, unique content, `rhost:` operator
- **GitHub** — Secret hunting, credential discovery, code leaks
- **Shodan** — Internet-facing devices, banners, CVE matching
- **Censys** — Certificate transparency, port scanning, ASN queries
- **FOFA** — Chinese index, geographic diversity

For each engine:
- Supported operators & differences
- Advantages over Google
- Practical dorks with examples
- Engine-specific quirks
- Comparison table
- Recommendation workflow

**When to use:** 
- Google rate-limited? → Try Bing
- Hunting secrets? → GitHub dorking
- Looking for exposed devices? → Shodan
- Eastern European target? → Yandex

---

### 03-dork-automation.py
**Python tool for automated dorking**

Features:

- **Dork Generation:** Template-based or custom file input
- **Execution:** Google search via requests or Selenium
- **Rate Limiting:** Configurable delay + random jitter
- **Proxy Support:** Rotate through proxy list
- **Result Collection:** Parse Google results, extract URLs
- **Output Formats:** TXT, CSV, JSON
- **Built-in Templates:** 7 categories covering common pentesting targets

**Built-in Categories:**
1. Subdomain discovery
2. Configuration files
3. Backup files
4. Credentials
5. Admin panels
6. Exposed files
7. Cloud storage

**Usage:**

```bash
# Basic
python3 03-dork-automation.py -t example.com

# With custom dorks & proxies
python3 03-dork-automation.py -t example.com \
  -c custom-dorks.txt -p proxies.txt --delay 5

# Specific categories
python3 03-dork-automation.py -t example.com \
  --categories subdomain_discovery,config_files

# Export as JSON
python3 03-dork-automation.py -t example.com --format json
```

**Requirements:**
```bash
pip install selenium requests beautifulsoup4 python-dotenv
```

**When to use:** Large-scale reconnaissance, multiple targets, when manual dorking is infeasible.

---

### 04-workflow-methodology.md
**Pentest & red team dorking workflow**

Covers:

- **Penetration Testing Phases** — Where dorking fits in the full scope
- **7-Stage Workflow:**
  1. Pre-dorking preparation
  2. Initial reconnaissance (subdomains, tech stack)
  3. Sensitive information hunting (configs, credentials, backups)
  4. Access point discovery (admin panels, APIs)
  5. Directory & file enumeration
  6. Cloud & third-party services
  7. Compilation & prioritization
- **Red Team Approach** — Broader scope, organization-level reconnaissance
- **Best Practices** — Authorization, documentation, stealth, rate limiting
- **Metrics & Reporting** — What to measure, how to report findings
- **Timeline Example** — Expected duration per phase
- **Handoff to Next Phase** — What to deliver to scanning/enumeration teams

**When to use:** Starting a pentest or red team engagement; planning reconnaissance timeline; reporting findings.

---

### examples/ Directory

Sample files to get started:

- **example-dorks-custom.txt** — Template for custom dork file
- **example-proxies.txt** — Format for proxy list
- **example-findings-report.md** — Template for reporting findings

---

## Real-World Workflow Example

```bash
# 1. Confirm authorization
# ✓ Written scope received: example.com, *.example.com

# 2. Prepare environment
python3 -m pip install selenium requests beautifulsoup4 --quiet
# (Proxies optional; using residential proxy list for this example)

# 3. Generate initial subdomains
python3 03-dork-automation.py -t example.com \
  --categories subdomain_discovery \
  --delay 5 \
  -o stage2-subdomains.json

# Finding: 12 subdomains discovered
# - api.example.com
# - staging.example.com
# - internal.example.com
# - (9 more)

# 4. Search for sensitive files
cat << 'EOF' > quick-dorks.txt
site:example.com filetype:env
site:example.com filetype:sql
site:example.com inurl:.git/config
site:example.com filetype:pdf intext:"password"
EOF

python3 03-dork-automation.py -t example.com \
  -c quick-dorks.txt \
  --delay 5 \
  -o stage3-sensitive.json

# Finding: Critical .env file exposed
# Location: https://example.com/config/.env.backup
# Content: DB_PASSWORD=SecurePass123!, AWS_KEY=AKIA..., etc.
# Action: Immediately report to client, escalate severity

# 5. Map admin panels
site:example.com inurl:admin
site:example.com intitle:"Login"
site:example.com inurl:phpmyadmin

# Finding: /admin/ panel at example.com/admin/
# Finding: MySQL console at example.com/phpmyadmin/

# 6. Cloud service check
s3.amazonaws.com example
site:s3.amazonaws.com "example.com"

# Finding: Publicly-readable S3 bucket (example-uploads)
# Finding: 1.2 GB of customer data accessible

# 7. Prepare findings report
# - 12 subdomains
# - 1 CRITICAL: Exposed .env (credentials)
# - 1 CRITICAL: Public S3 bucket (data exposure)
# - 2 HIGH: Admin panels found
# - 3 MEDIUM: Staging environments
# Total impact: HIGH (immediate data access possible)

# 8. Deliver report to client
# Document all findings with URLs, timestamps, recommendations
```

---

## Key Principles

### Authorization First
- **Always** obtain written authorization before dorking a target
- Scope should specify domains, ranges, out-of-scope items
- Email confirmation acceptable; formal agreement better

### Document Everything
```markdown
Finding Entry:
- **Date/Time:** 2024-01-15 14:23:00 UTC
- **Dork Used:** site:example.com filetype:env
- **URL Found:** https://example.com/config/.env.backup
- **Risk Level:** CRITICAL
- **What We Found:** DB_PASS, AWS_KEY, STRIPE_SECRET
- **Action Taken:** Reported to client immediately
```

### Rate Limiting Discipline
```python
# Delays prevent CAPTCHA & bans
- 3–5 seconds minimum between queries
- Add random jitter (0–2 seconds)
- Use proxies for parallel execution
- If CAPTCHA appears: pause 2–4 hours
```

### Responsible Disclosure
```
❌ Don't: Download entire S3 buckets, modify files, test credentials
✅ Do: Report findings, provide URLs, suggest remediation
```

---

## Integration with Recon-OSINT-Vault

This module fits into the larger reconnaissance workflow:

```
Recon-OSINT-Vault/
├── osint/
│   ├── 01-google-dorking/          ← You are here
│   ├── 02-domain-infrastructure/   # Whois, DNS, registrars
│   ├── 03-org-corporate/           # Company info, employees
│   ├── 04-breach-data/             # Data leaks, credentials
│   └── 05-email-username/          # Email finding, username patterns
│
├── reconnaissance/
│   ├── 01-active-scanning/         # Nmap, port scanning
│   ├── 02-service-enumeration/     # Banner grabbing, version detection
│   ├── 03-web-enumeration/         # Dirsearch, content discovery
│   └── 04-api-reconnaissance/      # API testing, endpoint mapping
│
└── [workflow guides, tools, examples]
```

**Handoff:** Output from Google Dorking feeds into Active Scanning and Web Enumeration phases.

---

## Tips & Tricks

### Quick Testing
```bash
# Test a single dork without automation:
# (in browser)
site:example.com filetype:env

# Or via curl (simpler):
curl -s "https://www.google.com/search?q=site:example.com+filetype:env" \
  -H "User-Agent: Mozilla/5.0" | grep -oP 'href="([^"]+)"' | head -20
```

### False Positive Reduction
```bash
# Too broad (lots of noise)
site:example.com "password"

# Better (more specific)
site:example.com filetype:env intext:"DB_PASS"
site:example.com inurl:.env

# Even better (combine multiple signals)
site:example.com filetype:env inurl:config intext:"password"
```

### Rate Limit Recovery
```bash
# If you hit CAPTCHA:
1. Stop dorking immediately
2. Wait 2–4 hours
3. Resume with longer delays (10+ seconds)
4. Use proxies for subsequent queries
5. Alternate between search engines (Google → Bing → DuckDuckGo)
```

### Finding Validation
```bash
# Once you find a URL, validate it:
curl -I https://example.com/config/.env.backup  # Check HTTP status
curl https://example.com/config/.env.backup     # View content
file <downloaded-file>                           # Check file type
```

---

## Troubleshooting

### "403 Forbidden" on Found URL
- URL indexed by Google but no longer accessible
- Server denies direct access (requires referrer, auth, etc.)
- Permission was revoked after indexing
- **Action:** Report URL + error; client should verify manually

### CAPTCHA on Every Query
- IP flagged by Google (too many requests)
- Solution: Use proxy rotation, increase delays, use VPN
- Switch to Bing/DuckDuckGo temporarily

### No Results from Automation Script
- Target domain not indexed by Google yet
- Dorks too restrictive (no matches)
- Site blocks search engine crawlers (robots.txt)
- **Debug:** Try dorks manually in Google first

### Script Timeout on Large Result Sets
- Google may return 1000+ results per dork
- Increase `--timeout` (default 10 seconds)
- Limit result parsing to first 50 results

---

## Legal & Compliance

### In Scope
✅ Searching public, indexed information on Google
✅ Documenting findings for authorized targets
✅ Reporting vulnerabilities responsibly

### Out of Scope
❌ Unauthorized reconnaissance (no written scope)
❌ Downloading entire databases or file systems
❌ Modifying or deleting found data
❌ Sharing findings publicly without permission
❌ Using findings for extortion or blackmail

### Jurisdictional Considerations
- **US:** Computer Fraud & Abuse Act (CFAA) — depends on authorization
- **UK:** Computer Misuse Act — unauthorized access is illegal
- **EU:** GDPR — personal data discovery has compliance implications
- **Local laws vary widely** — check with legal counsel

**Always obtain written authorization before starting reconnaissance.**

---

## Contributing & Feedback

- Add new dork patterns as you discover them
- Document edge cases and workarounds
- Test alternative search engine operators
- Share findings (de-identified) to improve templates
- Report tool bugs & feature requests

---

## References & Further Reading

### Search Engine Documentation
- [Google Advanced Search](https://www.google.com/advanced_search)
- [Bing Advanced Operators](https://help.bing.microsoft.com/apex/index/18/en-us)
- [Shodan Operators](https://beta.shodan.io/search/examples)
- [GitHub Search Syntax](https://docs.github.com/en/search-github)

### Security Resources
- OWASP Testing Guide (Reconnaissance)
- NIST Cybersecurity Framework
- PTES (Penetration Testing Execution Standard)
- SANS Security Essentials

### Tools & Libraries
- [Selenium (browser automation)](https://www.selenium.dev/)
- [BeautifulSoup (HTML parsing)](https://www.crummy.com/software/BeautifulSoup/)
- [Requests (HTTP library)](https://requests.readthedocs.io/)
- [Git Dumper (git repository extraction)](https://github.com/arthaud/git-dumper)

---

## License

MIT License — See LICENSE file in Recon-OSINT-Vault root.

---

## Contact & Support

For questions, issues, or suggestions:
- Create an issue in the Recon-OSINT-Vault repository
- Reference the relevant file(s) and step(s)
- Include examples for reproducibility

---

**Last Updated:** 2024-01-15
**Version:** 1.0
**Status:** Complete & Documented
