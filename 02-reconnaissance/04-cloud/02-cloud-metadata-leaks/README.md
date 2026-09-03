# Cloud Metadata & Misconfiguration Leaks

Mapping the target's cloud footprint and flagging exposed provider-level misconfigurations — separate from bucket-specific findings covered in `01-bucket-discovery/`.

## Cloud provider identification
- ASN lookup (from `01-osint/01-priority-technical/01-domain-infra-osint/`) often directly reveals the hosting provider (AWS, Azure, GCP, DigitalOcean) from the ASN organization name
- Response headers on identified assets sometimes reveal the provider directly (`X-Amz-*` headers, Azure-specific error page formatting)
- Reverse-IP lookups on discovered assets against known cloud provider IP ranges (AWS publishes its IP ranges publicly at `ip-ranges.amazonaws.com`)

## Cloud metadata endpoint exposure
Cloud instances expose an internal metadata service (`169.254.169.254` for AWS/most providers) that returns instance credentials and configuration — this is normally only reachable from *inside* the instance, but becomes a critical finding if an application is vulnerable to SSRF and can be tricked into requesting it. Recon-level scope here is limited to noting *that the target runs on a cloud provider with this metadata service model* — actual exploitation only happens later, during testing, if an SSRF vulnerability is found and confirmed in-scope.

## Publicly exposed cloud service dashboards
Check for accidentally-public management interfaces tied to discovered cloud infrastructure:
- Exposed Kubernetes dashboards (`/api/v1/namespaces/kube-system`, default port 8080/10250)
- Exposed Elasticsearch/Kibana instances with no auth (`_search` endpoint returning data with no credentials)
- Exposed Jenkins, GitLab CI, or similar CI/CD dashboards found during subdomain enumeration

```
nmap -p 8080,9200,5601,8443 --open live_hosts.txt
```
Quick targeted scan for common exposed-dashboard ports across the confirmed live host list.

## Workflow
1. Confirm cloud provider via ASN + header analysis
2. Note metadata-service model applicability as context for later SSRF testing (not tested directly here)
3. Targeted port scan for common exposed dashboard services across live hosts
4. Manually check any hit for authentication — many of these interfaces default to no-auth unless explicitly configured

## Output
Cloud provider identification feeds context into every other recon file; any exposed dashboard is a standalone high-priority asset inventory entry.
