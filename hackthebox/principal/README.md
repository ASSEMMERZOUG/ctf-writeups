# Principal

Hack The Box · Linux · 21 October 2026

Nobody at the door asked who was coming in, and nobody signing a certificate
asked who it was for. The platform accepted an unsigned token as long as it sat
inside an encrypted envelope the server would open, and the key to build that
envelope was published without authentication. The dashboard we reached showed
a deployment password in plain text; the account it belonged to could read the
private key of the SSH certificate authority the host trusts.

**Chain**

1. CVE-2026-29000 — pac4j-jwt 6.0.3 accepted a `PlainJWT` (`alg: none`) wrapped
   in a JWE built with the publicly served key.
2. The dashboard enumerated the accounts and printed the deployment password.
3. Password reuse: SSH as that account.
4. The SSH CA private key was group-readable by `deployers`.
5. `TrustedUserCAKeys` with no `AuthorizedPrincipalsFile` — a certificate for
   principal `root` was one command away.

[Report (PDF)](principal_pentest_report.pdf)
