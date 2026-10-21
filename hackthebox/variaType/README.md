# VariaType

Hack The Box · Linux · Medium · 14–16 June 2026

A typesetting platform built out of other people's libraries. No kernel exploit
anywhere: an exposed `.git`, three known CVEs, and a `sudo` rule, and the last
step is an SSH key in root's `authorized_keys`.

**Chain**

1. Exposed `.git` directory — hardcoded credentials in the history
2. path traversal, filter bypass — local file inclusion
3. CVE-2025-66034 — fonttools, arbitrary file write
4. CVE-2024-25082 — fontforge, command injection
5. CVE-2025-47273 — setuptools path traversal, reached through `sudo`

[Report (PDF)](variaType_pentest_report.pdf)
