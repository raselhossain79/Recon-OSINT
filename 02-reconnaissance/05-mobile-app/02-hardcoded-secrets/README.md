# Hardcoded Secrets in Mobile Apps

A focused pass specifically for credential/secret patterns in decompiled mobile source — distinct from the general static-recon pass in `01-apk-ipa-static-recon/` because secret-hunting benefits from dedicated tooling and pattern coverage beyond a manual grep.

## Automated scanning
```
mobsf # runs as a local web service, upload the APK/IPA through the UI or via its REST API
```
MobSF runs a full automated static analysis pass and specifically flags hardcoded secrets, insecure storage patterns, and known-vulnerable third-party library versions in one report — the most efficient single tool for this file's purpose.

```
grep -rnE "(AKIA[0-9A-Z]{16})|(AIza[0-9A-Za-z\-_]{35})|(sk_live_[0-9a-zA-Z]{24})" jadx_output/
```
Pattern examples: `AKIA...` (AWS access key ID format), `AIza...` (Google API key format), `sk_live_...` (Stripe live secret key format) — extend this pattern list based on what third-party SDKs the app appears to use (visible from imported package names in the decompiled source).

## Where secrets typically hide beyond obvious string literals
- `strings.xml` / resource files (Android) — developers sometimes move "config" values here rather than inline in code, assuming (incorrectly) that resource files are less scrutinized
- Native library files (`.so` files) — secrets embedded in compiled native code aren't caught by source-level grep passes; requires `strings` command on the binary itself:
  ```
  strings libnative.so | grep -iE "key|secret|token"
  ```
- Build configuration remnants (`google-services.json`, `.env`-style files sometimes accidentally bundled into the app package itself)

## Workflow
1. Run MobSF for the automated baseline pass
2. Targeted regex grep for known secret-format patterns (AWS, Google, Stripe, generic JWT-looking strings) across decompiled source
3. Check `strings.xml`/resource files separately from code
4. Run `strings` against any bundled native `.so` files

## Output
Any confirmed hardcoded secret is a standalone high-priority finding — record which SDK/service it grants access to, since impact assessment depends entirely on what the key can do (a public Google Maps key is low severity; a live payment-processor secret key is critical).
