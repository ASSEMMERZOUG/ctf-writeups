# Facts

Hack The Box · Linux · 19 April 2026

Six steps, no kernel exploit. The box was a CMS on top of S3 storage, and the
storage was open: an anonymous bucket you could write to, and later an internal
bucket holding someone's encrypted SSH key.

**Chain**

1. Anonymous MinIO access — the `randomfacts` bucket is public read/write
2. Camaleon CMS 2.9.0 at `/admin`; CVE-2024-46987, path traversal (LFI), reads
   `/etc/passwd` and `william`'s `user.txt`
3. CVE-2025-2304, mass assignment, promotes the account to administrator
4. Hardcoded S3 access key in the CMS Filesystem Settings
5. The internal bucket holds `trivia`'s encrypted SSH key; the passphrase cracks
6. `sudo facter` with `FACTORLIB` blocked, bypassed with `--custom-dir` — a Ruby
   fact runs as root

[Report (PDF)](facts_pentest_report.pdf)
