# Reactor

Hack The Box · Linux · 11 October 2026

A Node.js application on TCP 3000 running framework versions below the fixed
release for a published flaw. One crafted request runs code before the
application checks who is asking, and after that every secret the application
holds is readable.

**Chain**

1. unauthenticated RCE in the web application — shell as the service account
2. its own database of user accounts and passwords, plus an internal API key
3. a staff password reused for SSH
4. root

[Report (PDF)](reactor_pentest_report.pdf)
