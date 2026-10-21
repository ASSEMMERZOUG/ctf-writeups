# TwoMillion

Hack The Box · Linux · 5 April 2026

The web application imitates the platform it lives on, and the invitation code
was checked in the browser. The API behind it trusted the account too much:
a low-privilege user could promote itself to administrator and the admin console
had a command injection.

**Chain**

1. Invite-code bypass — an obfuscated `inviteapi.min.js` exposes a generate
   endpoint; the instruction comes back ROT13-encoded
2. Broken access control in the API — self-escalation to the admin role
3. OS command injection in the admin console — shell as `www-data`
4. Plaintext credentials in `.env`
5. CVE-2023-0386, OverlayFS, for root

Also: `PHPSESSID` set without `HttpOnly`, so any XSS steals the session.

[Report (PDF)](TwoMillion_pentest_report.pdf)
