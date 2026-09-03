# Swagger / OpenAPI / GraphQL Leaks

Finding exposed API documentation is effectively finding a complete blueprint of the API surface in one request — always worth checking early.

## Swagger / OpenAPI discovery
Common default paths to check:
```
for path in swagger.json swagger-ui.html api-docs openapi.json openapi.yaml v2/api-docs swagger/v1/swagger.json; do
  curl -s -o /dev/null -w "%{http_code} /$path\n" https://target.com/$path
done
```
If found, the JSON/YAML output enumerates every endpoint, parameter, and expected data type — feed this directly into `01-endpoint-discovery/` and `03-parameter-discovery/`, since it makes both of those steps far more precise than guessing via wordlists.

## GraphQL introspection
If introspection is not explicitly disabled, a single query retrieves the entire schema — including fields and mutations never exposed in the actual frontend, which is a recurring source of hidden/internal functionality.
```
curl -s -X POST https://target.com/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ __schema { types { name fields { name } } } } "}'
```
For a cleaner automated pass:
```
python3 graphql-cop.py -t https://target.com/graphql
```
graphql-cop checks for introspection availability plus a set of common GraphQL misconfigurations (batch query support that could enable DoS, field suggestions leaking internal names even with introspection disabled) in one run.

InQL as a Burp Suite extension is the better choice if you're already working inside Burp — it generates a browsable schema map and pre-built query templates directly from introspection results.

## Workflow
1. Check standard Swagger/OpenAPI default paths
2. If found, parse the spec for the full endpoint/parameter list
3. Check for a GraphQL endpoint (`/graphql`, `/api/graphql`, `/query` are common paths)
4. If found, attempt introspection; if disabled, try field-suggestion-based schema guessing as a fallback (graphql-cop covers this)

## Output
A found Swagger/OpenAPI spec or GraphQL schema essentially completes `01-endpoint-discovery/` and `03-parameter-discovery/` for that API in one step — prioritize checking this early in the API recon phase rather than last.
