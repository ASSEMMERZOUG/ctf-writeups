# Fireflow

Hack The Box · Linux · 19 October 2026

A web application in front of a Langflow instance, and under both of them a
Kubernetes node. No account, no credentials, no information supplied: the public
"Open Agent" button handed over a `flow_id`, and Langflow was vulnerable to
CVE-2026-33017, which needs nothing else.

**Chain**

1. The landing page exposed a Langflow `flow_id`.
2. CVE-2026-33017 — unauthenticated remote code execution; shell as the web
   account.
3. A password from Langflow's configuration was reused for `nightfall`.
4. That home directory leaked credentials for a custom MCP server, which
   accepted a JWT with `alg: none`.
5. Kubelet `nodes/proxy` gave command execution on the node, as root.

[Report (PDF)](fireflow_pentest_report.pdf)
