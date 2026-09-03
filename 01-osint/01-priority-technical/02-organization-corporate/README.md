# Organization / Corporate OSINT

Mapping the organization itself — not its servers, but its structure, vendors, and public hiring signals. Directly useful for scope expansion and tech-stack hints, which is why this sits in the priority-technical tier rather than the optional one.

## Techniques

### Job postings analysis
Hiring ads are one of the most reliable, most overlooked sources of exact tech stack information. A posting requiring "AWS, Kubernetes, Django, PostgreSQL" tells you the backend stack before you've sent a single request.
- Check the company's own careers page, plus LinkedIn Jobs and Indeed for the org name
- Look specifically at "requirements" and "nice to have" sections — internal tool names sometimes leak here too (e.g., a specific internal API gateway product)

### Employee / org structure enumeration
- LinkedIn company page → "People" tab gives a rough headcount and role breakdown by department (useful for judging engagement scope size, and for the email-format guess in the next file)
- Org chart reconstruction is mostly relevant if social-engineering is in scope — for pure technical work, the department breakdown (how big is the eng/security team) is the main useful signal

### Vendor / supply-chain mapping
Third parties with system access are often the weakest link and sometimes explicitly out of scope but worth noting:
- Check the target's own privacy policy / terms of service — these frequently list data processors and vendors by name
- SSL certificate SAN fields on shared/CDN infrastructure sometimes reveal which CDN or WAF vendor is in use

### M&A / acquisition mapping
On larger targets, this is the single highest-value technique in this file. Acquired companies frequently keep separate infrastructure for months or years after acquisition, and that infrastructure is often missed by subdomain enum rooted at the main domain.
- Search "[company name] acquires" / "[company name] acquisition" news
- Crunchbase (`crunchbase.com`) — lists subsidiaries and acquisitions for most notable companies
- Check the target's own investor relations / press page for acquisition announcements

## Workflow
1. Job postings → tech stack hint list
2. LinkedIn org page → rough team size, department split
3. Privacy policy / ToS → vendor list
4. Crunchbase + news search → subsidiary/acquisition list

## Output
Tech stack hints → feed into `00-methodology/07-tech-stack-vuln-mapping.md` as candidates to confirm technically. Subsidiary/acquisition names → feed into `01-domain-infra-osint/` as new domains to run WHOIS/crt.sh against (subject to scope confirmation before adding to the asset inventory).
