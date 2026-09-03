# Port & Service Scanning

Deep scanning of confirmed-live hosts only — this is active recon that directly touches the target and can appear in logs; confirm scope permits it before running.

## Full scan
```
nmap -sV -sC -p- -T4 target_ip -oA full_scan
```
- `-sV` — service/version detection (critical output for `00-methodology/07-tech-stack-vuln-mapping.md`)
- `-sC` — runs nmap's default script set (safe scripts only, checks for common misconfigs)
- `-p-` — all 65535 ports, not just the top-1000 default; misses matter more than time cost for a thorough engagement
- `-T4` — aggressive timing; drop to `-T2` if the scope specifies a rate limit or the target is known to be sensitive to scan load
- `-oA` — output in all formats (normal, XML, grepable) for later parsing/automation

## Faster first pass on large scope
```
nmap -sV --top-ports 1000 -T4 target_ip -oA quick_scan
```
Run this first across every live host to get a fast overview, then follow up with the full `-p-` scan only on hosts that showed interesting results or are flagged high-priority.

## Targeted script scanning (once services are identified)
```
nmap --script=vuln -p 443 target_ip
```
The `vuln` script category actively checks for a set of known vulnerabilities matched to detected services — more aggressive than the default `-sC` set, run this deliberately against confirmed high-value targets rather than broadly.

## UDP considerations
UDP scanning is frequently skipped due to time cost but catches services TCP scans miss entirely (SNMP, DNS, some VPN services):
```
nmap -sU --top-ports 100 target_ip
```
Worth running at least a top-ports UDP pass on infrastructure-heavy targets.

## Workflow
1. Fast top-ports scan across all live hosts for a quick overview
2. Full `-p-` scan on hosts flagged interesting or high-priority
3. Targeted `--script=vuln` pass on confirmed high-value services
4. UDP top-ports pass if time/scope allows

## Output
Service + version data feeds directly into `00-methodology/07-tech-stack-vuln-mapping.md`; open ports feed into the asset inventory per host.
