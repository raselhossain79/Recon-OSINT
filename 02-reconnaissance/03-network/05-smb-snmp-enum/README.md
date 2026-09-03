# SMB / SNMP Enumeration

Relevant mainly for internal/network pentest engagements rather than external web/API bug bounty — include this pass if the engagement scope covers internal network segments or if external hosts unexpectedly expose these services (rare but happens on misconfigured cloud instances).

## SMB enumeration
```
nmap --script smb-enum-shares,smb-enum-users -p 445 target_ip
```
Checks for accessible shares and enumerable users without authentication.

```
smbclient -L //target_ip/ -N
```
`-N` attempts a null session (no credentials) — if it succeeds, share listing without authentication is itself a finding worth flagging.

```
enum4linux -a target_ip
```
Broader automated enumeration: shares, users, groups, password policy, and OS info in one pass.

## SNMP enumeration
```
nmap -sU -p 161 --script snmp-info,snmp-processes target_ip
```
```
snmpwalk -c public -v1 target_ip
snmpwalk -c private -v1 target_ip
```
Default community strings (`public` for read-only, `private` for read-write) are still surprisingly common in production. A working `private` string is a high-priority finding — it typically allows configuration changes, not just information disclosure.

## Workflow
1. Confirm SMB (445) or SNMP (161) are open from the earlier port scan
2. Null-session SMB check, then enum4linux for a full pass if null session succeeds
3. Default community string check against SNMP if open
4. Flag any successful null-session or default-credential access as a high-priority finding immediately — these are config issues, not deep vulnerabilities, and worth reporting even before further testing

## Output
Any successful enumeration goes into the asset inventory with a high exposure-level flag — unauthenticated SMB/SNMP access is a recurring, high-impact, low-effort-to-fix finding worth surfacing early.
