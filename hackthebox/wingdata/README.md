# WingData

Hack The Box · Linux · 5 July 2026

A file-sharing site whose virtual host routing exposed an internal FTP web
client running Wing FTP Server 7.4.3 — a version with an unauthenticated remote
code execution flaw. The way back to root was a `sudo` rule for a backup-restore
script.

**Chain**

1. Virtual host → Wing FTP Server 7.4.3 web client, unauthenticated RCE
2. a user configuration file with a salted password hash, cracked offline
3. the password reused for SSH
4. `sudo` backup-restore Python script + `tarfile` → arbitrary write as root

[Report (PDF)](wingdata_pentest_report.pdf)
