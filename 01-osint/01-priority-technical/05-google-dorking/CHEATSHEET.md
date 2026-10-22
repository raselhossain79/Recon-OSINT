# Google Dorking Cheatsheet: Complete Reference

## Table of Contents
1. [Basic Operators](#basic-operators)
2. [Advanced Operators](#advanced-operators)
3. [Syntax Modifiers](#syntax-modifiers)
4. [Practical Dork Patterns](#practical-dork-patterns)
5. [Evasion & Optimization](#evasion--optimization)
6. [Common Pitfalls](#common-pitfalls)

---

## Basic Operators

### `site:`
**Purpose:** Restrict results to a specific domain or subdomain.

```
site:example.com                    # All pages on example.com
site:example.com filetype:pdf       # PDFs only on example.com
site:*.example.com                  # All subdomains (wildcard works)
site:example.com -site:api.example.com  # Exclude specific subdomain
```

**Why it works:** Google's crawler indexes all subdomains separately; this forces scope.

**Real-world examples:**
```
site:github.com intext:"AWS_ACCESS_KEY"           # Exposed secrets on GitHub
site:example.com inurl:admin                      # Admin panels
site:s3.amazonaws.com filetype:json              # Exposed S3 buckets
```

---

### `inurl:`
**Purpose:** Match keywords in the URL path only, not page content.

```
inurl:admin                         # URLs containing /admin/
inurl:backup                        # Backup files in paths
inurl:config                        # Configuration in URLs
```

**Key difference from `intext:`:** Faster, more precise for URL structure hunting.

**Real-world examples:**
```
inurl:admin login
inurl:/wp-admin/                    # WordPress admin
inurl:backup.sql
inurl:/.env
inurl:staging                       # Staging environments
inurl:test
inurl:dev
```

---

### `intitle:`
**Purpose:** Match keywords in the HTML `<title>` tag only.

```
intitle:"Index of"                  # Directory listings
intitle:"admin panel"
intitle:"live dashboard"            # Monitoring tools exposed
intitle:"Camera"                    # Exposed cameras
intitle:"Cpanel"                    # Control panels
```

**Why it works:** Page titles are often descriptive of purpose.

**Real-world examples:**
```
intitle:"Index of" backup
intitle:"Apache" filetype:log
intitle:"MySQL" filetype:sql
intitle:"Dashboard" "Live Traffic"
```

---

### `intext:` / `allintitle:`
**Purpose:** Search page content for specific text.

```
intext:"password"                   # Pages mentioning password
intext:"confidential"               # Sensitivity markers
intext:"API key"
allintitle:"admin password"         # All words must be in title
```

**`allintitle:` vs `intitle:`:**
- `intitle:admin intitle:panel` = "admin" OR "panel" in title
- `allintitle:admin panel` = "admin" AND "panel" in title (stricter)

---

### `filetype:`
**Purpose:** Restrict results to specific file types.

```
filetype:pdf                        # PDF documents
filetype:xlsx                       # Excel spreadsheets
filetype:docx                       # Word documents
filetype:sql                        # SQL dumps
filetype:log                        # Log files
filetype:conf                       # Configuration files
filetype:env                        # Environment files
filetype:bak                        # Backup files
filetype:xml                        # XML files (configs, API responses)
filetype:json                       # JSON files
filetype:ini                        # INI config files
filetype:config                     # Generic config
```

**Strategy:** Combine with `site:` or `inurl:` for precision.

```
site:example.com filetype:sql
site:example.com filetype:bak
inurl:backup filetype:sql
```

---

### `ext:` (Alternative to `filetype:`)
**Purpose:** Match file extensions; often works where `filetype:` doesn't.

```
ext:sql                             # Functionally same as filetype:sql
ext:bak
ext:old
ext:tmp
ext:cache
ext:git
ext:env
```

**Why use `ext:` over `filetype:`?** Some files aren't indexed as formal types; `ext:` is broader.

---

### `cache:`
**Purpose:** View Google's cached version of a page.

```
cache:example.com                   # Cached homepage
cache:example.com/admin             # Cached specific page
```

**Practical use:** Pages deleted or modified; cached version may reveal old secrets.

```
cache:example.com/config.php        # Check old config values
cache:api.example.com/docs          # Old API documentation
```

---

### `link:`
**Purpose:** Find pages linking to a target.

```
link:example.com                    # All pages linking to example.com
link:example.com/api                # Pages linking to /api
```

**Limited utility in modern Google** (deprecated for most queries), but useful for link analysis.

---

### `related:`
**Purpose:** Find similar websites.

```
related:example.com                 # Sites similar to example.com
```

**Use case:** Competitor reconnaissance, finding similar platforms.

---

## Advanced Operators

### Quotes: `" "`
**Purpose:** Exact phrase matching.

```
"exact phrase here"                 # Must match exactly
site:example.com "admin password"   # Exact phrase on site only
```

**Why crucial:** Removes false positives from partial matches.

```
"AWS_ACCESS_KEY_ID"                 # Exact secret format
"RDS_PASSWORD"
"PRIVATE_KEY"
```

---

### Wildcards: `*`
**Purpose:** Placeholder for any single word or phrase.

```
"password is *"                     # Matches "password is 123", "password is secret"
site:example.com/*/admin            # Matches /user/admin, /api/admin, etc.
```

**Limitation:** Works inconsistently; quoted phrases work better.

---

### Minus/Exclusion: `-`
**Purpose:** Exclude terms or sources.

```
site:example.com -site:cdn.example.com  # Exclude CDN
"password" -"reset"                 # Exclude password reset pages
inurl:admin -inurl:panel            # Admin but not panel
```

**Practical use:**
```
filetype:log -"error" -"warning"    # Reduce noise in log searches
site:example.com filetype:sql -backup  # SQL files excluding backups
```

---

### OR: `|` or `OR`
**Purpose:** Logical OR (match any condition).

```
site:example.com (filetype:sql | filetype:bak)
inurl:admin | inurl:panel | inurl:dashboard
```

**Equivalent shorthand:**
```
site:example.com (filetype:sql OR filetype:bak)
```

---

### Parentheses: `( )`
**Purpose:** Group operators and control precedence.

```
(inurl:admin | inurl:panel) site:example.com
site:example.com (filetype:pdf | filetype:docx) "confidential"
```

---

## Syntax Modifiers

### Case Sensitivity
Google Dorking is **NOT case-sensitive** by default.

```
"PASSWORD" = "password" = "Password"  # All equivalent
```

---

### URL Path Encoding
Special characters in URLs are encoded; search both forms:

```
inurl:%20                           # Space (URL encoded)
inurl: space                        # Space (literal)
inurl:%2F/                          # Forward slash
inurl:admin%20panel                 # Encoded space in path
```

---

### Domain Extensions
Wildcard doesn't work for TLDs; search explicitly:

```
site:example.com | site:example.co.uk | site:example.in
```

**Or use subdomain wildcard:**
```
site:example.*                      # May work for all TLDs
```

---

### Numeric Ranges
Limited support; usually requires explicit enumeration.

```
"version 1.0" | "version 2.0" | "version 3.0"  # Enumerate versions
```

---

## Practical Dork Patterns

### Subdomain & Asset Discovery

```
site:*.example.com                  # All subdomains
site:example.com intext:"powered by"  # Tech stack hints
site:*.example.com inurl:admin
site:*.example.com filetype:xml     # Config files
```

### Exposed Configuration & Secrets

```
site:example.com filetype:env
site:example.com ".env" intext:"KEY"
inurl:config filetype:php
inurl:settings filetype:json
site:example.com filetype:conf
inurl:.git filetype:config

# Sensitive keywords
intext:"password = " filetype:conf
intext:"api_key" filetype:json
intext:"private_key" filetype:pem
intext:"AWS_SECRET_ACCESS_KEY"
```

### Backup & Archive Files

```
site:example.com filetype:sql
site:example.com filetype:bak
site:example.com filetype:old
site:example.com filetype:zip
inurl:backup filetype:sql
inurl:backup filetype:gz
ext:sql.bak
ext:tar.gz
```

### Directory Listings (Web Server Misconfiguration)

```
intitle:"Index of" site:example.com
intitle:"Index of" /admin
intitle:"Directory Listing"
"Parent Directory"
```

### Debug & Error Pages

```
intext:"You have an error in your SQL syntax"
intext:"stack trace"
intext:"debug mode"
inurl:debug filetype:log
intitle:"Exception Details"
intext:"Traceback" filetype:txt
```

### Login Panels & Admin Areas

```
inurl:admin
inurl:/login
inurl:wp-admin
inurl:cpanel
inurl:phpmyadmin
intitle:login site:example.com
intitle:"admin panel"
```

### Exposed Credentials

```
intext:"username" intext:"password" filetype:xlsx
intext:"username=" intext:"password=" filetype:txt
intext:"mysql_user" intext:"mysql_password"
intext:"db_username" intext:"db_password" filetype:php
```

### Cloud Storage Exposure

```
site:s3.amazonaws.com
site:storage.googleapis.com
site:blob.core.windows.net
inurl:s3.amazonaws.com filetype:json
"s3.amazonaws.com" filetype:xml
```

### API Documentation & Endpoints

```
inurl:/api/docs
inurl:swagger.json
inurl:/graphql
inurl:postman
intext:"API documentation"
inurl:v1/api
inurl:v2/api
```

### Source Code Leaks (Before GitHub)

```
intext:"<?php" filetype:php inurl:example.com
intext:"function admin" filetype:js
inurl:src filetype:java
```

### CI/CD & DevOps Exposure

```
inurl:jenkins
inurl:gitlab-ci
inurl:github.com/actions
intitle:Grafana inurl:example.com
intitle:Kibana dashboard
inurl:sonarqube
```

### Metadata & Document OSINT

```
filetype:pdf inauthor:"example.com"
filetype:docx intitle:"confidential"
inurl:2024 filetype:pdf site:example.com
```

---

## Evasion & Optimization

### Avoiding CAPTCHA & Rate Limits

1. **Rotate User-Agents & Proxies**
   - Google detects automated queries; use rotating proxies
   - Spread queries over time (not bulk in seconds)

2. **Use `cache:` Operator**
   - Load from cache to reduce fresh index queries
   - Avoids detection slightly longer

3. **Stagger Requests**
   - 5–10 second delays between queries
   - Use threading/async carefully (not parallel hammering)

4. **Vary Query Patterns**
   - Don't repeat identical dorks
   - Mix `site:` and `inurl:` for same goal
   - Change operator order occasionally

5. **Use Smaller Result Sets**
   - Deep pagination (page 50+) triggers captcha faster
   - Focus first 1–3 pages

### Automation Considerations

- Script with delays (see `04-automation/` for full details)
- Respect robots.txt
- Use headless browser (Selenium/Playwright) to handle JS rendering
- Alternate between search engines

---

## Common Pitfalls

### 1. **Operator Precedence**
Google doesn't support standard boolean logic; test dorks:

```
# Ambiguous
site:example.com | site:other.com filetype:pdf

# Clearer with parentheses (if supported)
(site:example.com | site:other.com) filetype:pdf
```

**Best practice:** Use separate queries, combine results.

---

### 2. **Over-Quoting**
```
# Bad: Too specific, may miss variations
"exact API documentation path"

# Better: Quote only critical phrase
inurl:api "documentation"
```

---

### 3. **Forgetting Context**
```
# Too broad
password

# Scoped
site:example.com intext:"password" filetype:conf
```

---

### 4. **Wildcard Abuse**
```
# Doesn't work well
site:*.com

# Use explicit:
(site:example.com | site:example.co.uk)
```

---

### 5. **False Positives with `intext:`**
`intext:` searches all page text, including comments, ads, footers.

```
# May return false positives
intext:"admin"

# Better
site:example.com inurl:admin intitle:"panel"
```

---

### 6. **Not Testing Operator Support**
Not all operators work consistently across regions/time. Test each:

```
# Test locally first
site:google.com inurl:careers filetype:pdf

# If works, apply to target
site:example.com inurl:careers filetype:pdf
```

---

## Quick Reference Table

| Operator | Syntax | Example | Use Case |
|----------|--------|---------|----------|
| `site:` | `site:domain.com` | `site:example.com` | Scope to domain |
| `inurl:` | `inurl:keyword` | `inurl:admin` | Find URLs with keyword |
| `intitle:` | `intitle:keyword` | `intitle:"Index of"` | Title-based search |
| `intext:` | `intext:keyword` | `intext:"password"` | Content-based search |
| `filetype:` | `filetype:ext` | `filetype:pdf` | File type restriction |
| `ext:` | `ext:ext` | `ext:sql` | Alternative to filetype |
| `cache:` | `cache:url` | `cache:example.com` | Cached version |
| `link:` | `link:url` | `link:example.com` | Backlinks |
| `"..."` | `"phrase"` | `"exact match"` | Exact phrase |
| `*` | `keyword * keyword` | `"admin * panel"` | Wildcard (single word) |
| `-` | `-keyword` | `-admin` | Exclude term |
| `\|` | `keyword1 \| keyword2` | `filetype:pdf \| filetype:docx` | OR operator |
| `()` | `(query1 \| query2)` | `(filetype:pdf \| filetype:docx)` | Grouping |

---

## Search Engine Operator Support Comparison

| Operator | Google | Bing | DuckDuckGo | Yandex |
|----------|--------|------|------------|--------|
| `site:` | ✅ | ✅ | ✅ | ✅ |
| `inurl:` | ✅ | ✅ | ✅ | ✅ |
| `intitle:` | ✅ | ✅ | ✅ | ✅ |
| `intext:` | ✅ | ~ (limited) | ✅ | ✅ |
| `filetype:` | ✅ | ✅ | ✅ | ✅ |
| `cache:` | ✅ | ✅ (as `cached:`) | ❌ | ❌ |
| `link:` | ~ (deprecated) | ✅ | ❌ | ✅ |
| Quotes `""` | ✅ | ✅ | ✅ | ✅ |
| `-` | ✅ | ✅ | ✅ | ✅ |

---

## Notes

- **Google regional differences:** Dorks may behave differently on google.com vs regional (google.co.uk, google.com.br). Test across regions for critical targets.
- **API Usage:** Google's official API (Custom Search API) has strict limits; dorking via browser/headless is still primary method.
- **Legal:** Always confirm authorization before searching targets. Dorking is reconnaissance; unauthorized recon is illegal.
