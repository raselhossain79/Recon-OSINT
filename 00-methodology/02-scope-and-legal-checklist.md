# 02 — Scope & Legal Checklist

Gate-check before any information gathering starts. Nothing in this vault should run before this file is filled out for the target.

## Pre-engagement (fill this in before touching anything)

| Item | Status | Notes |
|---|---|---|
| Written authorization / signed contract or program page confirmed | | |
| In-scope domains listed | | exact FQDNs, not assumptions |
| In-scope IP ranges listed | | CIDR notation |
| In-scope mobile apps listed | | package name / bundle ID |
| Out-of-scope assets listed explicitly | | third-party integrations, staging vs prod, acquired-but-unintegrated companies |
| Active scanning permitted? | Y/N | some programs are passive/OSINT-only |
| Rate limit / request-per-second cap | | if specified, respect it in every active tool's flags |
| Testing window (dates/times) | | |
| Data handling rule for PII/credentials found | | what to do if you hit breach data or live creds |
| Disclosure process / contact | | |

## During recon — re-check on every new asset
An asset found via subdomain enum, cert transparency, or org-OSINT is **not automatically in scope**. Before adding anything to the asset inventory:
1. Does it match an in-scope domain/IP pattern exactly, or is it a guess?
2. Is it explicitly excluded (common for staging, dev, or third-party-hosted subdomains)?
3. If ambiguous, flag it as "needs scope clarification" in the inventory rather than silently including or excluding it.

## Before scanning starts
Re-verify the full asset list against the original scope document one final time — this is Step 8 in `01-engagement-workflow.md` and is repeated deliberately, because recon naturally expands the asset list beyond what you started with.

## Legal sensitivity tiers (informal, use judgment + program rules)
- **Low risk**: passive OSINT, cert transparency, public search engines
- **Medium risk**: active port/service scanning, content discovery (generates target-side logs)
- **High risk**: credential testing against found breach data, dark-web OSINT, anything touching PII — always requires explicit scope language, not implied permission
