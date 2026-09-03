# Parameter Discovery

Brute-forcing hidden or undocumented parameters on known endpoints — parameters not present in any documentation or frontend code, but still processed by the backend.

## Tooling
```
arjun -u https://target.com/api/users -m GET
arjun -u https://target.com/api/users -m POST
```
`-m` sets the HTTP method to test — run both GET and POST passes, since some parameters are only processed on one method and not the other.

```
x8 -u https://target.com/api/users -w params-wordlist.txt -X GET
```
x8 is generally faster than arjun for large wordlists and supports more granular output formatting for feeding into further automation.

## Wordlist strategy
- Start with SecLists' `burp-parameter-names.txt` as a generic base
- Cross-reference parameter names discovered in JS analysis (`01-web/06-js-analysis/`) — frontend code frequently references parameter names the backend accepts even if they're not currently used in any visible request
- Any Swagger/OpenAPI spec found in `02-swagger-graphql-leaks/` already gives you the documented parameter list — parameter discovery here is specifically for *undocumented* additions on top of that

## What a discovered hidden parameter usually indicates
- A debug/admin flag left in from development (`?debug=true`, `?admin=1`) — high-value find, test carefully within scope
- An internal filtering/sorting parameter not meant for public use, sometimes vulnerable to injection since it wasn't designed with external input validation in mind
- A parameter tied to an older API version or deprecated feature still processed by current backend code

## Workflow
1. Pull the documented parameter list from any found API spec first
2. Run arjun/x8 against key endpoints (prioritize the ones flagged high-value in the asset inventory) with a merged generic + JS-derived wordlist
3. Manually verify any hit — a tool reporting a parameter as "found" just means the response changed, not that it's necessarily meaningful; confirm the behavior difference makes sense

## Output
Confirmed hidden parameters go into the asset inventory notes per endpoint, and become priority candidates for manual testing at the scanning handoff stage — undocumented parameters are exactly the kind of thing automated scanners miss and manual testing catches.
