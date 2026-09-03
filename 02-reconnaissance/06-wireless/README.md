# Wireless Recon (Optional)

Mostly relevant for internal/physical-network pentest engagements — rare in pure web/API bug bounty work. Kept as an optional category; expand only if an engagement's scope includes on-site wireless assessment.

## Techniques (only applicable with physical/on-site scope and explicit authorization)

### SSID enumeration and rogue AP detection
```
airodump-ng wlan0mon
```
Passively lists all visible SSIDs, associated clients, and signal strength in range — the starting point for identifying the target's legitimate corporate network versus any unauthorized rogue access points nearby.

### WPA/WPA2 handshake capture for offline analysis
```
airodump-ng --bssid TARGET_BSSID -c CHANNEL -w capture wlan0mon
aireplay-ng --deauth 5 -a TARGET_BSSID wlan0mon
```
Capturing a handshake for offline cracking attempts requires explicit written authorization covering physical wireless testing specifically — general web/API pentest scope does not imply this.

## Why this stays minimal in the vault
Given the focus on web/API pentest and bug bounty work, wireless assessment is unlikely to come up. This file exists as a placeholder/reference in case an engagement's scope ever expands to include an on-site component — expand it with deeper technique detail only if and when that actually happens, rather than maintaining depth here preemptively.
