# DevHub

Hack The Box · Linux · 21 October 2026

A development tool left answering on a routable port, with no login and an
endpoint that starts whatever command it is handed. From the shell it gave us,
the analyst's Jupyter token was sitting in the process list, and the account
that token belonged to could read the source of the one service running as root.
That service carried an undocumented admin tool that returned root's private SSH
key.

**Chain**

1. CVE-2026-23744 — MCPJam Inspector 1.4.2 executed `serverConfig.command` from
   an unauthenticated `POST /api/mcp/connect`; the reply is a 500, the command
   runs anyway.
2. `ps` showed `jupyter-lab --ServerApp.token=<token>`, readable by any local
   user, with Jupyter bound to `127.0.0.1:8888`.
3. The token opened a Jupyter terminal as `analyst`: `user.txt` and
   `~/.opsmcp_key`.
4. `/opt/opsmcp/server.py` — owned by `analyst`, running as root — registered
   hidden tools `ops._debug_mode` and `ops._admin_dump`.
5. `ops._admin_dump {"target": "ssh_keys", "confirm": true}` returned
   `/root/.ssh/id_rsa`. SSH as root.

[Report (PDF)](devhub_pentest_report.pdf)
