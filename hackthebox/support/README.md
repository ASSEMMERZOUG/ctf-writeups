# Support

Hack The Box · Windows · 8 April 2026

Active Directory, and four small mistakes in a row. Nothing here needed an
exploit against a memory corruption or a missing patch: a share that let
anybody read it, a password in a compiled binary, another one in an LDAP
attribute, and one permission too many on the Domain Controller object.

**Chain**

1. Anonymous SMB access to a non-default share
2. Hardcoded encrypted credentials in a .NET binary, recovered from it
3. A plaintext password sitting in an LDAP user attribute
4. `GenericAll` on the Domain Controller object → Resource-Based Constrained
   Delegation → Domain Admin

[Report (PDF)](support_pentest_report.pdf)
