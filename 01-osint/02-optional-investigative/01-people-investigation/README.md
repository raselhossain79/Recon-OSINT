# People Investigation

Correlating identity information across platforms for specific individuals tied to the target organization (typically admins, developers, or executives, when relevant to a social-engineering scope).

## Techniques

### Username correlation
- Sherlock (`sherlock username`) — checks a given username across 300+ platforms simultaneously, reports which ones return a match
- Manual cross-referencing: if a GitHub username is known, check if the same handle appears on Twitter/X, Reddit, or forums — people frequently reuse handles across professional and personal accounts

### Phone number OSINT
- Reverse lookup services identify carrier and rough geographic region (rarely exact identity without a paid/law-enforcement-tier service)
- Useful mainly for confirming a number found elsewhere belongs to a real, active line before using it in a phishing-simulation pretext

### Email-to-identity mapping
- Once an email is confirmed (from `01-priority-technical/04-email-username-osint/`), reverse-search it against social platforms and breach databases to build a fuller picture of the individual, if the engagement scope calls for individually-targeted social engineering

## Ethical/legal note
This category has real potential for misuse outside authorized engagement scope. Only apply these techniques against individuals explicitly covered by signed engagement scope (e.g., "employees of Target Corp for phishing simulation purposes") — never against arbitrary individuals out of curiosity.
