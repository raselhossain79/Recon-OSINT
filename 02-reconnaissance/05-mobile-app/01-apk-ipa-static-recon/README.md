# APK / IPA Static Recon

Decompiling mobile apps for embedded API endpoints, hardcoded credentials, and internal infrastructure references — pure static analysis, no device/emulator execution or dynamic testing at this stage.

## Obtaining the app
- Android: download the APK directly via `apkpure.com`, `apkmirror.com`, or pull it from a rooted test device with `adb pull`
- iOS: requires either a jailbroken device with a tool like `frida-ios-dump`, or working from a `.ipa` if the engagement provides one directly — iOS static analysis is meaningfully harder to source than Android without device access

## Android decompilation
```
apktool d target-app.apk -o decompiled/
```
Produces readable smali code and, critically, the full `AndroidManifest.xml` (permissions requested, exported components, deep-link URL schemes).

```
jadx -d jadx_output/ target-app.apk
```
jadx produces near-Java-readable decompiled source, generally easier to manually review than raw smali for spotting hardcoded strings and API logic.

## What to search for in decompiled source
```
grep -rn "http" jadx_output/ | grep -v "schemas.android.com"
grep -rniE "api[_-]?key|secret|token|password" jadx_output/
```
- Hardcoded API base URLs — frequently reveal staging/internal API hosts never exposed on the public web
- Hardcoded API keys or tokens embedded directly in code (common mistake, high-value find)
- Certificate pinning implementation details — relevant later for dynamic testing setup, not exploitable at the static-recon stage but worth noting

## AndroidManifest.xml review
- `exported="true"` components (activities, services, broadcast receivers) are reachable by other apps on the device — a recon-stage flag for later manual attack-surface testing
- Deep-link URL schemes (`<data android:scheme="targetapp">`) — worth noting as a distinct entry point separate from the standard web API

## Workflow
1. Obtain the APK/IPA
2. apktool decompile for manifest review
3. jadx decompile for readable source review
4. grep pass for hardcoded URLs, keys, and secrets
5. Manual manifest review for exported components and deep-link schemes

## Output
Discovered API endpoints feed into `02-api/01-endpoint-discovery/`; hardcoded secrets are a standalone high-priority finding in the asset inventory.
