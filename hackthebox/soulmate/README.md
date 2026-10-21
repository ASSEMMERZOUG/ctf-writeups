# Soulmate

Hack The Box · Linux · Easy · 10 October 2025

A hidden virtual host with a CrushFTP version that lets an unauthenticated
visitor create an administrator account. A web shell, then a plaintext password
left in a startup script, then a service running as root that only listens on
localhost.

**Chain**

1. Virtual host discovery → CrushFTP 11.W.657
2. CVE-2025-31161 — unauthenticated admin account creation, PHP web shell,
   shell as `www-data`
3. Plaintext credentials in an Erlang startup script → `ben`
4. Erlang SSH daemon on localhost, running as root, commands executed as root

[Report (PDF)](soulmate_pentest_report.pdf)
