# API-Specific Fingerprinting

Identifying the API gateway/framework and understanding rate-limit behavior before testing begins — this shapes both tool selection and pacing for the active testing phase.

## Gateway/framework identification
Response headers frequently reveal the underlying gateway even when the application itself is fingerprint-resistant:
```
curl -sI https://target.com/api/users
```
Look for:
- `X-Kong-*` headers → Kong API Gateway
- `X-Amzn-*` / specific error page formatting → AWS API Gateway
- `Apigee-*` → Apigee
- Framework-specific error response shapes (e.g., a very specific JSON error schema) even without explicit headers — different frameworks have recognizably different default error formats

## Rate-limit behavior probing (passive observation, not aggressive testing)
Send a small burst of legitimate-looking requests and observe response headers and behavior, without attempting to actually trigger or bypass the limit at this stage:
```
for i in {1..10}; do curl -sI https://target.com/api/users | grep -i "ratelimit\|retry-after"; sleep 1; done
```
Common headers to watch for: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `Retry-After`. If none appear even after several requests, note that the API may lack visible rate limiting entirely — relevant both as a recon finding and as pacing guidance for later active testing.

## Why this matters for the handoff
Knowing the gateway in advance lets you select gateway-specific test cases at the scanning stage (e.g., Kong-specific admin API exposure checks) rather than generic ones. Knowing the rate-limit behavior in advance prevents accidentally triggering a block mid-engagement from running default-aggressive tool settings.

## Workflow
1. Header inspection on 2–3 representative endpoints for gateway signatures
2. Error-response shape comparison if headers are inconclusive
3. Light rate-limit probing, recorded but not stress-tested

## Output
Gateway identification feeds into `00-methodology/04-master-tool-index.md` tool selection; rate-limit findings feed directly into pacing decisions noted in `00-methodology/08-recon-to-scanning-handoff.md`.
