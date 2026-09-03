# Social Media OSINT

Platform-specific search techniques for gathering public information relevant to the target organization or its staff.

## Techniques by platform

- **LinkedIn** — advanced search operators (`site:linkedin.com/in "target company"`) when direct platform search is rate-limited; useful for org-structure confirmation from `01-priority-technical/02-organization-corporate/`
- **Twitter/X** — advanced search operators (`from:`, `since:`, `until:`) for finding accidental internal-info leaks in employee posts (screenshots with visible internal tool names, complaints about specific internal systems)
- **Facebook/Instagram** — mostly relevant for physical-security or brand-protection engagements, low value for pure technical pentest
- **Telegram** — relevant if the target or its user base has known presence in Telegram groups/channels; search for leaked data mentions

## Use case for pentest work specifically
Beyond phishing-pretext research, the main technical value here is spotting accidental leaks — an employee screenshotting a dashboard that shows an internal hostname, or a support account replying with details about backend architecture in a public thread.
