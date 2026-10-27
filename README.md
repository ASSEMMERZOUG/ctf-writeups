# CTF writeups

I break into machines on purpose, then write the report I would hand a client:
what I found, how I proved it, and how it should be fixed.

Sixteen Hack The Box machines, documented end to end — recon, the request that
proved each finding, the escalation, and the fix. I build them with
[pdfsmith](https://github.com/ASSEMMERZOUG/pdfsmith), the report engine in my
other repo: no LaTeX, no Word, no template borrowed from somewhere.

## Hack The Box

| Machine | OS | Solved | The chain, short version |
|---|---|---|---|
| [Odori](hackthebox/odori/) | Linux | Oct 2026 | Guest-readable backup share holding the disk image and the SFTP password in plaintext, a `ForceCommand` wrapper the confined account could overwrite, and a world-writable `__pycache__` behind a root cron |
| [Abducted](hackthebox/abducted/) | Linux | Oct 2026 | Print job name injected into a shell command, world-readable backup credential, a share that wrote as another user, then a systemd drop-in plus polkit |
| [DevHub](hackthebox/devhub/) | Linux | Oct 2026 | MCPJam Inspector RCE, Jupyter token in the process list, a hidden admin tool that dumps root's SSH key |
| [Principal](hackthebox/principal/) | Linux | Oct 2026 | `alg:none` inside a valid JWE, password reuse, then the SSH CA signed a certificate for root |
| [Fireflow](hackthebox/fireflow/) | Linux | Oct 2026 | Langflow RCE, a reused config password, an MCP server, root on the Kubernetes node |
| [Reactor](hackthebox/reactor/) | Linux | Oct 2026 | One crafted request into the Node.js app, its own secrets, then the admin account |
| [WingData](hackthebox/wingdata/) | Linux | Jul 2026 | Wing FTP Server RCE, cracked hash, `tarfile` used to write as root |
| [Nexus](hackthebox/nexus/) | Linux | Jul 2026 | Password in Gitea history, Krayin CRM RCE, Gitea template-sync path traversal |
| [Orion](hackthebox/orion/) | Linux | Jun 2026 | CraftCMS RCE, database credentials, reused password, telnetd auth bypass |
| [VariaType](hackthebox/variaType/) | Linux | Jun 2026 | Exposed `.git`, three CVEs in a row, `sudo` path traversal to root |
| [Facts](hackthebox/facts/) | Linux | Apr 2026 | Open MinIO bucket, two Camaleon CMS CVEs, `facter --custom-dir` |
| [CCTV](hackthebox/cctv/) | Linux | Apr 2026 | ZoneMinder SQLi, cracked bcrypt hash, motionEye running as root |
| [Support](hackthebox/support/) | Windows | Apr 2026 | Anonymous SMB, password in an LDAP attribute, RBCD to Domain Admin |
| [TwoMillion](hackthebox/TwoMillion/) | Linux | Apr 2026 | Invite-code bypass, broken access control in the API, OverlayFS privesc |
| [Cap](hackthebox/cap/) | Linux | Apr 2026 | IDOR on packet captures, FTP credentials in plaintext, `cap_setuid` |
| [Expressway](hackthebox/expressway/) | Linux | Dec 2025 | IKEv1 pre-shared key cracked offline, `sudo` NSS injection |
| [Soulmate](hackthebox/soulmate/) | Linux | Oct 2025 | CrushFTP admin creation, credentials in an Erlang script, root daemon |

Reports live in [`hackthebox/`](hackthebox/) — one folder per machine, a short
README, and the PDF.

## What is in a report

- Executive summary and a findings table with severity.
- Scope, methodology, and the services actually found.
- Each finding: where it lives, what it is, the request or command that proves
  it, and what it gives an attacker.
- Reproduction steps with screenshots.
- Remediation: what to change, not "validate your inputs".

## Notes

- A machine goes up here once it is retired. No walkthrough for a live box.
- Every flag in the screenshots is redacted. Passwords in the text are the ones
  the box ships with or that were cracked during the run — nothing here is a
  credential to anything real.

## About

Assem Merzoug — electrical engineering graduate working toward web and API
penetration testing. Bug bounty and CTFs, mostly web.
[GitHub](https://github.com/ASSEMMERZOUG)
