# Odori

Hack The Box · Linux · 26 October 2026

A backup share anyone could read, holding the material used to rebuild the
backup service — including the image of the Windows host that writes to it, and
a script inside that image with the SFTP password as a literal string. The
account that password opens is meant to be SFTP-only, confined by a wrapper it
owns. Then a root cron imports Python bytecode from a world-writable directory.

**Chain**

1. Anonymous SMB to `backup`: `info.txt` pointed at the disk image referenced in
   the machine description.
2. That image carries `C:\Scripts\backup.ps1`, which builds a `PSCredential` from
   `$SFTPPassword` written in the file. The BitLocker volume and its unlock
   material sat on the same share.
3. The recovered password opened `svc_backup`, restricted by
   `ForceCommand /opt/restrict` — a script owned and writable by `svc_backup`
   itself. Uploading a replacement that starts a shell removed the restriction.
   `user.txt`.
4. `/opt/archiver/app.py` runs from root cron every minute and imports `helper`;
   `/opt/archiver/__pycache__` was `drwxr-xrwx`.
5. A same-length edit to `helper.cpython-310.pyc` (`/usr/bin/tar` →
   `/tmp/bin/tar`) left the bytecode loadable; a two-line `/tmp/bin/tar` made
   `bash` setuid, and a file dropped in `/backup` with an old mtime triggered it.
   Root.

Note: the 18 GB disk image was not downloaded. The offline credential-recovery
step is reproduced from the machine's own documentation and is labelled as such
in the report; every step from the SFTP login onward was run against the live
host.

[Report (PDF)](odori_pentest_report.pdf)
