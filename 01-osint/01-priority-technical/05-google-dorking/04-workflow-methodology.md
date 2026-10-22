# Google Dorking Workflow & Methodology

---

## Penetration Testing Phases & Dorking Role

### Phase Overview

```
┌─────────────────────────────────────────────────────────────┐
│                  PENETRATION TESTING PHASES                  │
├─────────────────────────────────────────────────────────────┤
│ 1. Scoping & Planning                                        │
│ 2. Reconnaissance (OSINT + Technical)  ← Dorking here        │
│ 3. Scanning & Enumeration               ← And here           │
│ 4. Vulnerability Assessment                                  │
│ 5. Exploitation                                              │
│ 6. Post-Exploitation & Privilege Escalation                 │
│ 7. Reporting & Remediation                                  │
└─────────────────────────────────────────────────────────────┘
```

### Where Dorking Fits

**Primary:** Phase 2 (Reconnaissance) – Low-risk, information gathering
**Secondary:** Phase 3 (Scanning & Enumeration) – Target identification refinement

---

## Complete Dorking Workflow (Step-by-Step)

### Stage 1: Pre-Dorking Preparation (5–10 minutes)

**Goal:** Scope confirmation, proxy setup, tool readiness.

#### 1.1 Confirm Scope & Authorization

```
☐ Written authorization obtained?
☐ Scope documented (domains, ASN ranges, IP CIDR)?
☐ Out-of-scope identified (third-party services, unrelated domains)?
☐ Rules of engagement reviewed (timing, frequency limits)?
☐ Legal review completed (CFAA, RIPA, local laws)?
```

**Checklist:**
- Get scope in writing before starting
- Confirm with client if using proxies/automation (may trigger alerts)
- Document all findings with timestamps

#### 1.2 Proxy & Infrastructure Setup

**Why proxies?**
- Avoid IP ban from Google's anti-bot systems
- Distribute requests across multiple IPs
- Reduce likelihood of CAPTCHA triggers

**Setup:**
```bash
# Option 1: Free proxy list (less reliable)
curl https://www.proxy-list.download/api/v1/get?type=http -o proxies.txt

# Option 2: Paid proxy service (recommended for professional work)
# - Bright Data, Oxylabs, Smartproxy
# - Register, download API credentials

# Option 3: Rotating proxy service
# - Requires subscription; not needed for one-time scans

# Test proxy connectivity
for proxy in $(cat proxies.txt | head -5); do
    curl -x $proxy https://ipinfo.io -s | jq .ip
done
```

#### 1.3 Tool Preparation

```bash
# Install Python dependencies
pip install selenium requests beautifulsoup4 python-dotenv

# Download ChromeDriver (Selenium requirement)
# https://chromedriver.chromium.org/ (match your Chrome version)

# Verify installation
python3 03-dork-automation.py --help
```

---

### Stage 2: Initial Reconnaissance Dorking (20–40 minutes)

**Goal:** Gather baseline information about target infrastructure.

#### 2.1 Subdomain Discovery

**Why first?** Subdomains are entry points; more targets = more attack surface.

```bash
# Command
python3 dork-automation.py \
  -t example.com \
  --categories subdomain_discovery \
  --delay 5 \
  --format json \
  -o stage2-subdomains.json

# Expected findings
- api.example.com (API endpoints)
- staging.example.com (Test environment)
- mail.example.com (Mail server)
- vpn.example.com (VPN portal)
- internal.example.com (Internal services)
```

**Manual validation:**
```bash
# Verify discovered subdomains resolve
for subdomain in api staging mail internal; do
    nslookup $subdomain.example.com
done

# Document IP addresses for next phase (scanning)
```

#### 2.2 Technology Stack Identification

**Why?** Different tech = different vulnerabilities and dork patterns.

```bash
# Generic tech markers
site:example.com "powered by" | "built with" | "running on"

# Specific searches
site:example.com filetype:json intext:"framework"  # Web framework
site:example.com inurl:wp-content                  # WordPress
site:example.com inurl:wp-admin
site:example.com filetype:xml intext:"namespace"   # ASP.NET hints
site:example.com inurl:web.config                  # IIS
```

**Document findings:**
```
Technology Stack for example.com:
- Web Framework: Django/Flask/Laravel/ASP.NET
- Database: MySQL/PostgreSQL/MSSQL (from error pages)
- Web Server: Apache/Nginx/IIS
- CMS: WordPress/Joomla/Drupal (if applicable)
- CDN: Cloudflare/Akamai
- Hosting: AWS/Azure/GCP/Self-hosted
```

---

### Stage 3: Sensitive Information Hunting (30–60 minutes)

**Goal:** Discover exposed secrets, credentials, and misconfigurations.

#### 3.1 Configuration File Exposure

```bash
# High-priority dorks
python3 dork-automation.py \
  -t example.com \
  --custom-dorks config-dorks.txt \
  --delay 5

# Where config-dorks.txt contains:
site:example.com filetype:env
site:example.com filetype:conf
site:example.com filetype:json intext:api_key
site:example.com filetype:config
site:example.com inurl:.git/config
site:example.com inurl:settings.php
```

**Example findings:**
```
# .env file exposure
DB_HOST=db.internal.example.com
DB_USER=admin
DB_PASS=SuperSecure123!
API_KEY=sk_live_51234567890abc
STRIPE_SECRET=rk_live_51234567890abc
PRIVATE_KEY=-----BEGIN PRIVATE KEY-----...
```

**Severity assessment:**
- Database credentials: CRITICAL
- API keys: HIGH (can authenticate as app)
- Private keys: CRITICAL (can decrypt data, sign requests)
- 3rd-party tokens (Stripe, AWS): HIGH

#### 3.2 Backup & Archive File Recovery

```bash
# SQL dumps are valuable – full database copies
site:example.com filetype:sql
site:example.com filetype:sql.bak
inurl:backup filetype:sql

# Compressed archives may contain entire source/database
site:example.com filetype:zip
site:example.com filetype:tar.gz
inurl:backup filetype:zip
```

**What to look for in SQL dumps:**
```sql
-- User tables (passwords in plaintext, hashed, or encryption)
INSERT INTO users (id, username, password_hash, email, role) VALUES (...)

-- Configuration tables (API keys, secrets)
INSERT INTO config (key, value) VALUES ('stripe_secret_key', '...')

-- Session tables (active sessions, tokens)
INSERT INTO sessions (user_id, token, expires) VALUES (...)
```

#### 3.3 Git Repository Exposure

```bash
# GitHub history often contains secrets developers later removed
site:example.com inurl:.git/config
site:example.com ".git/HEAD"

# Or search GitHub directly:
# https://github.com/search?q=example.com+password
# https://github.com/search?q=org:example-corp+API_KEY
```

**Extract repo if exposed:**
```bash
git clone https://example.com/.git/
# OR
git-dumper https://example.com/.git/ ./dumped-repo
cd dumped-repo && git log --oneline
```

**Secrets to search:**
```bash
# In dumped repo:
grep -r "password" . --include="*.py" --include="*.js"
grep -r "SECRET" . --include="*.conf"
git log --all --source --remotes -S "password" -p
```

---

### Stage 4: Access Point Discovery (20–40 minutes)

**Goal:** Find login panels, admin interfaces, and service endpoints.

#### 4.1 Admin & Login Panels

```bash
# Automated discovery
site:example.com inurl:admin
site:example.com inurl:/login
site:example.com inurl:/signin
site:example.com inurl:wp-admin
site:example.com intitle:"Admin Panel"
site:example.com intitle:"Login"
```

**Typical findings:**
```
Example.com Admin Interfaces:
- https://example.com/admin/
- https://example.com/admin/login/
- https://example.com/administrator/
- https://example.com/phpmyadmin/
- https://cpanel.example.com/
- https://webmail.example.com/
```

**Next steps:**
- Try default credentials (admin/admin, admin/password)
- Check if login page is exposed (may reveal technology)
- Look for password reset endpoints (potential account takeover)
- Check for forgotten password functionality

#### 4.2 API Documentation & Endpoints

```bash
# API discovery
site:example.com inurl:/api/
site:example.com inurl:swagger.json
site:example.com inurl:/graphql
site:example.com filetype:json intext:"swagger"

# GitHub API dorks (if they host API docs there)
org:example-corp inurl:api inurl:documentation
```

**Document API structure:**
```
API Endpoints Found:
- https://api.example.com/v1/users
- https://api.example.com/v1/products
- https://api.example.com/v2/admin
- https://example.com/graphql (GraphQL endpoint)

Authentication Method:
- Bearer token (Authorization: Bearer <token>)
- API key (X-API-Key header)
- OAuth 2.0
- mTLS certificates
```

---

### Stage 5: Directory & File Enumeration (10–20 minutes)

**Goal:** Identify web directories, exposed files, debug pages.

#### 5.1 Directory Listings

```bash
# Misconfigured web servers exposing directory contents
intitle:"Index of" site:example.com
intitle:"Index of" /admin site:example.com
intitle:"Index of" /backup site:example.com

# These expose filesystem structure:
/admin/
/backup/
/old/
/test/
/private/
```

**Manual browsing after dork:**
```bash
# Once you find directory listing, browse:
https://example.com/backup/

# Look for:
- Database backups (*.sql, *.db)
- Compressed archives (*.zip, *.tar.gz)
- Configuration files (*.conf, *.env, *.xml)
- Source code (*.php, *.py, *.js)
```

#### 5.2 Error & Debug Pages

```bash
# Error pages leak technology information
intext:"Stack Trace" site:example.com
intext:"Exception" filetype:log site:example.com
intext:"You have an error in your SQL syntax"
```

**Information extracted from error pages:**
```
PHP Stack Trace:
File: /var/www/html/index.php
Line: 123
Database Error: Connection failed to 'db.internal.example.com'

ASP.NET Error:
Source: System.Data.SqlClient
Message: Login failed for user 'appuser'
```

---

### Stage 6: Cloud & Third-Party Service Reconnaissance (10–20 minutes)

**Goal:** Identify cloud infrastructure, external services, CDN.

#### 6.1 Cloud Storage Exposure

```bash
# S3 buckets (AWS)
site:s3.amazonaws.com example
s3.example.com

# Azure Blob Storage
site:blob.core.windows.net example

# Google Cloud Storage
site:storage.googleapis.com example
```

**Test for misconfiguration:**
```bash
# Check if publicly readable
aws s3 ls s3://example-bucket-name/
aws s3 ls s3://example-bucket-name/ --recursive

# Download findings
aws s3 cp s3://example-bucket-name/ . --recursive
```

#### 6.2 Third-Party Service Integration

```bash
# Look for external service references
site:example.com "https://stripe.com"
site:example.com intext:"Stripe API"
site:example.com intext:"AWS_REGION"
site:example.com intext:"GCP_PROJECT"
```

**Document:**
```
Third-Party Services:
- Stripe (Payment processing)
- Sendgrid (Email)
- Twilio (SMS/Voice)
- Auth0 (Identity)
- Datadog (Monitoring)
```

---

### Stage 7: Compilation & Prioritization (10 minutes)

**Goal:** Organize findings by severity for next phases.

#### 7.1 Create Findings Summary

```markdown
# Google Dorking Findings Summary
## Target: example.com
## Date: 2024-01-15

### CRITICAL (Immediate Action)
- [ ] Exposed database backup (SQL dump)
- [ ] Hardcoded AWS credentials in .env
- [ ] Private SSH key in Git history

### HIGH
- [ ] API key exposed in source code
- [ ] Admin panel found at /admin/secret
- [ ] S3 bucket publicly readable

### MEDIUM
- [ ] Exposed error pages revealing tech stack
- [ ] Directory listing on /backup/
- [ ] Staging environment accessible

### LOW
- [ ] Tech stack identified (WordPress 6.1)
- [ ] Subdomains enumerated (10 found)
- [ ] Employee email format identified

### For Next Phase (Scanning & Enumeration)
- Scan subdomains discovered
- Test found admin panels with credentials
- Enumerate API endpoints
- Verify S3 bucket accessibility
```

---

## Red Team Dorking Workflow

Dorking for red team engagement differs (broader scope, no single domain):

### Red Team Phase: Target Organization Reconnaissance

**Goal:** Map entire organization's web presence.

```bash
# 1. Find all domains
site:*.example-corp.* inurl:whois  # Find registration info
google-dork: "example corporation" website

# 2. Enumerate all assets
site:example-corp.com
site:example-corp.co.uk
site:example-corp.co.in
site:*.example-corp.com

# 3. Subdomain proliferation (for broader scope)
site:*.example-corp.com -www inurl:admin
site:*.example-corp.com inurl:vpn
site:*.example-corp.com inurl:dev

# 4. Find leaked credentials by company
site:github.com "example-corp" password
site:pastebin.com "example-corp" credentials

# 5. Email harvest (for phishing campaign)
site:example-corp.com filetype:pdf
# Extract emails from PDFs via metadata
pdftotext filename.pdf -
```

---

## Best Practices & Rules of Engagement

### Golden Rules

1. **Always have written authorization**
   - Email confirmation acceptable
   - Scope document essential
   - Update scope as discoveries expand

2. **Document everything**
   ```
   Finding Log Entry:
   - Date/Time: 2024-01-15 14:23:00 UTC
   - Dork: site:example.com filetype:env
   - URL Found: https://example.com/config/.env.backup
   - Content: DB credentials, API key
   - Risk: CRITICAL
   - Action: Reported to client immediately
   ```

3. **Responsible handling of findings**
   - Don't access or download unless necessary
   - Don't share findings (client only)
   - Don't attempt to modify or delete
   - Report severity accurately

4. **Rate limiting & stealth**
   - 3–5 second delay minimum between queries
   - Use proxies to distribute requests
   - Avoid bulk automation during peak hours
   - If CAPTCHA appears, pause for 2–4 hours

### Avoid These Mistakes

```
❌ Running all dorks in parallel (triggers rate limit)
❌ Using personal IP without proxy (traceable)
❌ Sharing raw findings publicly (breach of confidentiality)
❌ Testing without written scope (legal liability)
❌ Downloading entire S3 bucket without approval (excessive)
❌ Brute-forcing found credentials immediately (may alert)
```

---

## Metrics & Reporting

### Dorking Metrics

```
Metric                          Importance    Why?
────────────────────────────────────────────────────
Subdomains Discovered           High          Attack surface measure
Config Files Exposed            Critical      Direct risk
Active Services Found           High          Scan targets
Credentials Revealed            Critical      Immediate risk
Vulnerabilities Indicated       High          Exploitation path
```

### Sample Report Section

```markdown
## 2. Reconnaissance Results

### 2.1 Asset Discovery
- **Subdomains Found:** 23
  - api.example.com (API server)
  - staging.example.com (Staging env)
  - internal.example.com (Internal portal)
  - vpn.example.com (VPN gateway)
  - ... (19 more)

### 2.2 Exposed Credentials
- **Critical:** Database credentials in .env file
  - Location: https://example.com/.env.backup
  - Impact: Complete database access
  - Recommendation: Immediate remediation

### 2.3 Configuration Issues
- **High:** Directory listing enabled on /backup/
  - Location: https://example.com/backup/
  - Exposure: 5 SQL backup files
  - Recommendation: Disable directory listing

### 2.4 Technology Stack
- Web Server: Nginx 1.18
- Application: Django 3.2
- Database: PostgreSQL 12
- CDN: Cloudflare

### 2.5 Next Phase Targets
(For scanning & enumeration)
- 23 subdomains for active scanning
- 2 identified web applications for testing
- 3 API endpoints for fuzzing
```

---

## Timeline Example

Assuming a typical scope (single domain, no sensitive findings fast-tracked):

```
15:00 - Scope confirmation & authorization check ............... 10 min
15:10 - Proxy setup & tool installation .......................... 10 min
15:20 - Stage 2: Subdomain discovery ............................ 20 min
15:40 - Stage 3: Config file search ............................. 30 min
16:10 - Stage 4: Admin panel identification ..................... 20 min
16:30 - Stage 5: Directory enumeration .......................... 15 min
16:45 - Stage 6: Cloud service check ............................ 10 min
16:55 - Stage 7: Report compilation & findings prioritization ... 10 min
17:05 - COMPLETE (total: ~2 hours)

(If critical findings: interrupt, escalate, pause for client guidance)
```

---

## Handoff to Next Phase

After dorking completion:

**Deliverables to Scanning/Enumeration Team:**
```
1. Subdomain list (validated)
2. Technology stack documentation
3. API endpoints discovered
4. Admin interfaces identified
5. Cloud service references
6. Findings summary (severity-ranked)
```

**Do NOT hand off:**
```
- Raw credentials (report severity only)
- Actual database dumps
- Private keys or secrets
- Sensitive file contents
```

---

## Legal & Compliance Checklist

- [ ] Scope document signed by client
- [ ] Rules of engagement confirmed
- [ ] Authorized user list maintained
- [ ] All findings logged with timestamps
- [ ] No data exfiltrated (testing purposes only)
- [ ] Findings reported confidentially
- [ ] Remediation timeline documented
- [ ] Final cleanup: no artifacts left on targets
