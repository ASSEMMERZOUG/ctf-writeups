# Expressway

Hack The Box · Linux · 10 December 2025

An IKEv1/XAUTH VPN on UDP 500. The pre-shared key was weak enough to crack
offline, and the credentials the VPN handed out were accepted by SSH. Root was
a `sudo` version from before the NSS fix.

**Chain**

1. Weak IKEv1 pre-shared key — cracked offline
2. XAUTH credentials recovered, reused for SSH as `ike`
3. `sudo` 1.9.17 — CVE-2025-32463, `-R` and an NSS library, root

[Report (PDF)](expressway_pentest_report.pdf)
