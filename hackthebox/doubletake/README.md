# DoubleTake

Hack The Box · Linux · 13 November 2026

An Alpine container whose SSH server links musl instead of glibc. A 300-byte
password makes musl's `crypt()` return `*`, the value shadow uses for accounts
that can never log in, so the second attempt on one connection authenticates as
`alpine` with no password. The home directory held a Firefox profile with the
web and SSH password in plain base64, and the web app's Deploy page forwarded
archives to Docker's archive endpoint — where Docker 29.5.0 ran the container's
own `xz` as host root.

**Chain**

1. nmap: 22 (OpenSSH 10.6, musl build) and 80 (nginx, Basic realm Zentara)
2. CVE-2026-123158: 300-byte password for `alpine` over one transport →
   second attempt authenticates → shell inside the container
3. `/home/alpine/.mozilla/firefox/zentara.default/logins.json`, encType 0 →
   base64 decodes to `bob:CorrectHorseBatteryStaple`
4. same password works over SSH as `bob` → user flag (bind-mounted from host)
5. Zentara status page: Docker 29.5.0; Deploy page accepts `.tar.gz`/`.tar.xz`
   with a target path
6. replace `/usr/bin/xz` in the container with a static binary (mount proc,
   chroot to `/proc/1/root`, reverse shell), upload it via `/deploy` with
   workspace `/`
7. upload any `.tar.xz` → Docker resolves and executes the trojan as host root
   (CVE-2026-41567) → root flag

[Report (PDF)](doubletake_pentest_report.pdf)
