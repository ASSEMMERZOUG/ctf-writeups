# Abducted

Hack The Box · Linux · 26 October 2026

A printer shared with guests, and Samba puts the job name into a shell command
unquoted. From the shell it handed back, every step was a file that more people
could read or write than intended — a world-readable backup credential, a share
that writes as the wrong user, and a systemd drop-in directory a group could
write to.

**Chain**

1. Anonymous SMB listing exposed `HP-Reception` alongside `projects` and
   `transfer`.
2. CVE-2026-4480 — `print command = /usr/local/bin/printaudit %J %s` with
   `printing = sysv`; `%J` is the client-chosen document name, substituted
   unquoted. A job named `|sh` ran the spool body as shell, as `nobody`.
3. `/opt/offsite-backup/rclone.conf` was world-readable. `rclone reveal` decoded
   its obscured password — which was also `scott`'s login. SSH, `user.txt`.
4. The `transfer` share ran every write as `force user = marcus` with
   `allow insecure wide links` on: a symlink to `/home/marcus`, then
   `authorized_keys` written through the share, gave `marcus`.
5. `marcus` was in `operators`, which could write
   `/etc/systemd/system/smbd.service.d`, and polkit let operators reload the
   daemon and restart `smbd` without authenticating.
6. An `ExecStartPre` line copied `bash` and set it setuid root. Root.

[Report (PDF)](abducted_pentest_report.pdf)
