# WordPress Recon

Pure discovery/enumeration only — this file identifies what's running and what version; actual exploitation of identified WordPress vulnerabilities belongs in your existing WordPress pentest reference library, not here.

## Plugin and theme enumeration
```
wpscan --url https://target.com --enumerate ap,at,u --api-token YOUR_WPSCAN_TOKEN
```
- `ap` = all plugins, `at` = all themes, `u` = usernames
- `--api-token` connects to the WPScan vulnerability database directly, so results come back pre-annotated with known CVEs — this makes WPScan output feed almost directly into `00-methodology/07-tech-stack-vuln-mapping.md` with no extra cross-referencing step

For plugins not caught by passive script/stylesheet-path detection (i.e., installed but not actively loaded on the checked page), brute-force against a plugin-slug wordlist:
```
wpscan --url https://target.com --enumerate ap --plugins-detection aggressive
```

## Version fingerprinting
- `/readme.html` — often discloses the exact WordPress core version
- Meta generator tag in page source: `<meta name="generator" content="WordPress 6.4.2">`
- `/wp-includes/version.php` if directly accessible (rare, but happens on misconfigured installs)

## wp-json REST API enumeration
```
curl -s https://target.com/wp-json/wp/v2/users | jq
```
This endpoint frequently leaks valid usernames even when the classic `?author=1` enumeration method is blocked — always check both.

## XML-RPC check
```
curl -s -X POST https://target.com/xmlrpc.php -d '<?xml version="1.0"?><methodCall><methodName>system.listMethods</methodName></methodCall>'
```
If XML-RPC is enabled, note it — it's a common vector for brute-force amplification and DDoS pingback abuse, worth flagging even at the recon stage as a config-hardening finding.

## Classic username enumeration
```
curl -sI "https://target.com/?author=1"
```
Check the `Location` header in the redirect response — it typically reveals the username in the resulting URL slug.

## Exposed config/backup files
```
curl -s https://target.com/wp-config.php.bak
curl -s https://target.com/wp-config.php.save
```
Also check for `.sql` database dumps left in accessible upload directories — combine with the content-discovery wordlist pass (`05-content-discovery/`) using a WordPress-specific backup-filename wordlist.

## Workflow
1. wpscan full enumeration pass (plugins, themes, users) with API token for pre-annotated CVE data
2. Manual version confirmation via readme.html / meta tag as a cross-check
3. wp-json and classic author-enum for username discovery
4. XML-RPC status check
5. Backup/config file discovery pass

## Output
Plugin/theme/core versions with CVE annotations go straight into the asset inventory; discovered usernames feed into `01-osint/01-priority-technical/04-email-username-osint/` for credential-testing prep later.
