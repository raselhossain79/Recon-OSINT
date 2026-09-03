# Dark Web OSINT

Requires the most caution of any technique in this vault — both legally and operationally.

## Techniques

- Tor-based search engines (Ahmia, DarkSearch) for organization name mentions
- Marketplace/forum monitoring for targeted credential or data-sale listings referencing the target

## Before doing any of this
1. Confirm engagement scope explicitly covers dark-web monitoring — this is rarely implied by general "OSINT" scope language and often needs separate written authorization.
2. Use isolated infrastructure (see `06-opsec-for-investigator/`) — never access dark-web resources from infrastructure tied to your real identity or the client's network.
3. Treat anything found as intelligence to report, not something to purchase, download in bulk, or interact with beyond passive observation.

## Realistic use case
For most web/API bug bounty and standard pentest work, this technique essentially never applies. It's included here for completeness and for the rare engagement (large enterprise, post-breach investigation) where it's explicitly requested.
