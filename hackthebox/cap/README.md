# Cap

Hack The Box · Linux · 4 April 2026

A network-security dashboard that let anyone download packet captures by
changing a number in the URL. Captures are full of credentials, and this one was
too — the FTP password was also the SSH password. Root came from a binary with
a capability it should not have.

**Chain**

1. IDOR — unauthenticated access to other users' `.pcap` files
2. Cleartext FTP credentials in a capture, reused for SSH
3. `cap_setuid` on the Python 3.8 binary — `os.setuid(0)`, and the process is
   root

[Report (PDF)](cap_pentest_report.pdf)
