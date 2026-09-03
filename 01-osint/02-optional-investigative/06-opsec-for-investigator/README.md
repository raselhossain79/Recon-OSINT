# OPSEC for the Investigator

Protecting your own identity and operational security while performing OSINT — this is self-protection for the researcher, not a technique against the target.

## Practices

### Sock-puppet account hygiene
- Separate accounts fully from personal identity — different email provider, no shared phone number, no shared profile photo
- Never log into a sock-puppet account from the same browser session/IP as your personal accounts on the same platform (cross-linking risk via platform-side tracking)

### VM/VPN isolation
- Run investigation sessions inside a dedicated VM, not your daily-driver machine — keeps browser history, cookies, and cached logins fully separated
- VPN or dedicated investigation infrastructure so your real IP never touches target-adjacent or dark-web resources directly

### Avoiding accidental self-exposure
- Screenshots can leak your own timezone (via system clock in screenshot tools), browser fingerprint, or even reflections/desktop icons — crop and review before saving
- Locale/language settings on investigation browsers should be set generically, not to your actual region, if operating under a sock-puppet identity

### Infrastructure reuse rule
Never reuse investigation infrastructure (VMs, sock-puppet accounts, VPN endpoints) across unrelated engagements — a compromised or burned identity on one engagement shouldn't carry risk into the next.
