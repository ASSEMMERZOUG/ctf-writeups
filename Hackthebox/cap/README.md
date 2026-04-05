# HTB: Cap

**Difficulty:** Easy  
**OS:** Linux  
**IP:** 10.129.26.105  
**Status:** ✅ Pwned

---

## Summary

Cap is an easy Linux machine hosting a network monitoring web dashboard. The application is vulnerable to IDOR, exposing packet captures from other users. One capture contains plaintext FTP credentials which grant SSH access. Post-exploitation reveals a misconfigured Linux capability on Python 3.8 (`cap_setuid`), allowing instant privilege escalation to root.

---

## Attack Chain

```
IDOR (/data/0) → Plaintext FTP creds in PCAP → SSH access → cap_setuid abuse → root
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
| 1 | IDOR — Unauthenticated PCAP access | Critical |
| 2 | Cleartext credentials in network capture | Critical |
| 3 | Misconfigured Linux capability (cap_setuid) | High |

---

## Tools Used

- `nmap` — port scanning
- `Wireshark` — PCAP analysis
- `linpeas.sh` — post-exploitation enumeration
- `getcap` — Linux capabilities audit

---

## Key Commands

```bash
# IDOR - access other user's capture
http://10.129.26.105/data/0

# Privilege escalation via cap_setuid
python3.8 -c 'import os; os.setuid(0); os.system("/bin/bash")'
```

---

## Files

| File | Description |
|------|-------------|
| `cap_pentest_report.pdf` | Full penetration test report |
| `output.txt` | Nmap scan results |
| `01_web_dashboard_idor_data3.png` | IDOR vulnerability screenshot |
| `02_wireshark_ftp_credentials.png` | Plaintext credentials in Wireshark |
| `03_web_ip_config_exposure.png` | IP config information disclosure |
