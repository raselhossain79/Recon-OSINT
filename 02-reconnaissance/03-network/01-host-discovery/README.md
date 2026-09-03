# Host Discovery

Confirming which hosts in a range are actually live before spending time on deep port/service scanning — always run this first on any IP range, never scan a whole CIDR blindly with a full port scan.

## Techniques
```
nmap -sn -iL candidate_ips.txt -oG ping_sweep.txt
```
`-sn` disables port scanning entirely and just checks host liveness (ICMP + a few common TCP probes as fallback since many networks block raw ICMP) — fast, low-footprint way to filter a large candidate list down to actually-live hosts.

For larger ranges (ASN-derived CIDR blocks from `01-osint/01-priority-technical/01-domain-infra-osint/`):
```
masscan -p80,443 10.0.0.0/16 --rate=1000 -oG masscan_live.txt
```
Using masscan against just ports 80/443 as a fast liveness proxy is often more practical than a true ICMP sweep on cloud-hosted ranges, where ICMP is frequently filtered but web ports respond.

## Extracting the live list
```
grep "Up" ping_sweep.txt | cut -d' ' -f2 > live_hosts.txt
```

## Workflow
1. Take the candidate IP range (from ASN/BGP lookup or from resolved subdomain IPs)
2. Run nmap `-sn` sweep, or masscan against a couple of common ports for cloud-hosted ranges
3. Extract confirmed-live hosts only
4. Pass the reduced list into `02-port-service-scan/` — never run a full `-p-` scan against an unconfirmed range, it wastes enormous time on dead hosts

## Output
Live host list feeds directly into `02-port-service-scan/`.
