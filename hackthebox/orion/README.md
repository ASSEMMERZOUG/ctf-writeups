# Orion

Hack The Box · Linux · 28 June 2026

A corporate site on CraftCMS, with the CMS version visible from outside and a
critical no-login remote code execution flaw in it. The rest of the box was
configuration: a database password that was also an SSH password, and a local
service that let anyone in as root.

**Chain**

1. CraftCMS — unauthenticated RCE, foothold on the server
2. database credentials in a configuration file
3. a weak hash in that database, cracked offline, was reused for SSH
4. a local telnet service, abused to bypass authentication and reach root

[Report (PDF)](orion_pentest_report.pdf)
