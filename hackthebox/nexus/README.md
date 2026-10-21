# Nexus

Hack The Box · Linux · 2 July 2026

A static landing page, a self-hosted Gitea, and a Krayin CRM. The way in was
not a bug in the landing page: it was a password someone committed to a public
repository and then deleted, which is not deleting it.

**Chain**

1. A password exposed in a Gitea repository's git history
2. the same credentials opened the CRM
3. CVE-2026-38526 — unauthenticated file-upload RCE in Krayin
4. CRM configuration files held SSH credentials for `jones`
5. a root-owned Gitea template-sync service joined attacker input with an
   unsanitised `os.path.join()`, a path traversal, and wrote a key into
   `/root/.ssh/authorized_keys`

[Report (PDF)](nexus_pentest_report.pdf)
