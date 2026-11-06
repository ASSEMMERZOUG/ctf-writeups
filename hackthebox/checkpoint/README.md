# Checkpoint

Hack The Box · Windows · 29 October 2026

An Active Directory assessment where nothing was a software bug. The starting
account could rewrite the Recycle Bin's permissions and bring a deleted user
back from the dead; that user still had a password we already knew and could
write to the share a scheduled task installs VS Code extensions from. Root came
from a backup share holding the memory of a server that was running when the
snapshot was taken.

**Chain**

1. `WriteDacl` on `CN=Deleted Objects`, write on the tombstone of Mark Davies,
   `CreateChild` on `OU=Employees`
2. `set restore mark.davies` → the account returns and still accepts
   `Checkpoint2024!`
3. `mark.davies` writes `\\DC01\DevDrop`; a `.vsix` that runs on
   `onStartupFinished` is picked up by a scheduled task → shell as
   `ryan.brooks`, user flag
4. `\\DC01\VMBackups` holds a powered-on snapshot; the local Administrator hash
   in the `.vmem` is the domain Administrator's → pass-the-hash, root flag

[Report (PDF)](checkpoint_pentest_report.pdf)
