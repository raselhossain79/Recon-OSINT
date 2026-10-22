# When to Use What — Dork Selection Guide

> **Important:** This repo is a reference library, not a checklist. You never run every dork category on every engagement — scope and engagement type decide what's relevant. This file tells you exactly which categories to pick for each situation.

---

## Core Rule

**Scope defines selection.** A dork category only gets used if it matches:
1. What's actually in scope (domains, subdomains, orgs)
2. The engagement type (web pentest vs API pentest vs red team vs bug bounty)
3. What the client/program allows (some bug bounty programs exclude employee OSINT, social engineering recon, etc.)

If a category isn't relevant to scope, skip it entirely — running it wastes time and adds noise to your findings.

---

## By Engagement Type

### 1. Web Application Pentest (client-authorized, single domain/app)

**Use:**
- ✅ Exposed Configuration & Environment Files
- ✅ Backup & Archive Files
- ✅ Directory Listings & Misconfiguration
- ✅ Debug & Error Pages
- ✅ Login & Admin Panels
- ✅ Vulnerable Parameter Patterns
- ✅ Source Code Leaks (if client hosts public repos)

**Skip (usually out of scope):**
- ❌ Employee & Organizational Info (unless social engineering is in scope)
- ❌ Shodan/Censys device scanning (unless network pentest is also in scope)
- ❌ Cloud storage discovery (unless client confirms they use S3/Azure/GCS and wants it checked)

---

### 2. API / Web+API Pentest (your primary focus area)

**Use:**
- ✅ API Documentation & Endpoints (Swagger, GraphQL, Postman) — **highest priority**
- ✅ Exposed Configuration & Environment Files
- ✅ Exposed Credentials & Secrets (API keys, tokens)
- ✅ Source Code Leaks (JS files often expose API endpoints/keys)
- ✅ Vulnerable Parameter Patterns (SSRF, IDOR-adjacent parameter names)
- ✅ Third-Party & Dependency Files (package.json, requirements.txt — reveals API client libraries)

**Skip:**
- ❌ Subdomain discovery (run only lightly — just enough to find `api.`, `api-v2.`, `staging-api.` patterns)
- ❌ Employee/organizational OSINT
- ❌ Directory listings (lower priority unless API docs are statically hosted)

---

### 3. Red Team / Full Organization Assessment

**Use (in this order):**
1. ✅ Subdomain & Asset Discovery — **always first**, maps full attack surface
2. ✅ GitHub Dorking — org-wide secret hunting across all repos
3. ✅ Cloud Storage Exposure — S3/Azure/GCS buckets across the org
4. ✅ Employee & Organizational Info — needed for phishing/social engineering phase
5. ✅ CI/CD & DevOps Exposure — Jenkins, GitLab, monitoring dashboards
6. ✅ Shodan/Censys — network-level device and service discovery
7. Then cascade into the Web/API categories above for each discovered asset

**Skip:** Nothing is really "skip" here — red team scope is broad by design. But still only within the confirmed scope document (ASN ranges, named subsidiaries, etc.).

---

### 4. Bug Bounty (narrow scope, program rules apply)

**Use:**
- ✅ Exposed Configuration & Credentials (within listed scope domains only)
- ✅ Login & Admin Panels
- ✅ API Documentation & Endpoints
- ✅ Source Code Leaks / GitHub dorking (only if program explicitly allows OSINT on public repos)
- ✅ Vulnerable Parameter Patterns

**Skip — almost always out of scope for bug bounty:**
- ❌ Employee & Organizational Info (social engineering is banned on most programs)
- ❌ Shodan/Censys device scanning (usually "no active scanning outside listed assets" rule applies — dorking for shodan results on out-of-scope IPs is still a scope violation)
- ❌ Any subdomain not explicitly listed in the program's scope, even if `site:*.target.com` reveals it — **report it as an out-of-scope finding, don't test it**

**Always check the program's policy page first** — some explicitly prohibit dorking/OSINT entirely.

---

## By Target Type (Quick Lookup)

| Scope is... | Primary categories | Secondary categories |
|---|---|---|
| Single web app | Config files, admin panels, directory listing, error pages | Source code, parameters |
| REST/GraphQL API | API docs, credentials, source code (JS) | Third-party deps, parameters |
| Full domain + subdomains | Subdomain discovery first | Everything else, cascaded |
| Cloud-hosted infra confirmed | Cloud storage, config files | CI/CD, subdomain |
| GitHub org known | GitHub dorking | Source code leaks, credentials |
| Bug bounty program | Config, admin, API, parameters | Source code (if allowed) |
| Social engineering in scope | Employee/org info, email OSINT | Document metadata |

---

## What This Means for the Rest of the Repo

- **`01-google-dorks-by-target.md`** — treat as a menu, not a script. Pick the sections relevant per the tables above.
- **`03-dork-automation.py`** — use the `--categories` flag to run only what's relevant instead of all built-in templates:
  ```bash
  # API pentest example — only relevant categories
  python3 03-dork-automation.py -t example.com \
    --categories config_files,credentials,admin_panels

  # Don't do this unless it's a red team / full-org assessment:
  python3 03-dork-automation.py -t example.com   # (runs ALL categories by default)
  ```
- **`04-workflow-methodology.md`** — the 7-stage workflow already assumes web pentest scope; for API-focused work, reweight time toward Stage 4 (API discovery) and Stage 3 (credentials), and shrink Stage 2 (subdomains) and skip Stage 6 (cloud) unless relevant.

---

## One-Line Takeaway

**Default to the narrowest relevant set of categories for the engagement type, confirm against the written scope, and only broaden if the client/program scope explicitly covers more.**
