# CCTV

Hack The Box · Linux · 9 April 2026

A CCTV management panel that still had its default credentials. From there a SQL
injection in the same product handed over the password hashes, and a second
service on localhost — running as root, reachable by port forward — finished
the job.

**Chain**

1. ZoneMinder 1.37.63 — default administrator credentials
2. CVE-2024-51482 — authenticated SQL injection, bcrypt hashes out of the
   database
3. `mark`'s hash cracked with `rockyou.txt`, reused for SSH
4. motionEye on localhost, running as root; CVE-2025-60787, authenticated RCE,
   reached through an SSH port forward

[Report (PDF)](cctv_pentest_report.pdf)
