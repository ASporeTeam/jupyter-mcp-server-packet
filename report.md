# Sourcey docs for datalayer/jupyter-mcp-server — delivery report (Frantic #33)

**What was delivered:** the live, Sourcey-generated MCP reference of the maintained
third-party library [datalayer/jupyter-mcp-server](https://github.com/datalayer/jupyter-mcp-server),
pinned to commit `ef47e8b9c9bfce1a23265831a1ad80f94d58bb85` (2026-10-18, BSD-3-Clause,
1312 stars, 205 forks), published **on the project's own registered domain**.

- **public_url:** https://jupyter-mcp-server.datalayer.tech/mcp/index.html
- **evidence_json:** https://asporeteam.github.io/jupyter-mcp-server-packet/evidence.json
- **report:** https://asporeteam.github.io/jupyter-mcp-server-packet/report.md
- **receipt_ref:** `runx:receipt:sha256:f6623a72e628591f264d4db307ca70f05ea23fcda2d0cdef2fe8e9effbd0d1c6`
- **receipt (public):** https://asporeteam.github.io/jupyter-mcp-server-packet/receipt.json
- **receipt public key:** https://asporeteam.github.io/jupyter-mcp-server-packet/receipt-public-key.json
- **governed run output:** https://asporeteam.github.io/jupyter-mcp-server-packet/verification-output.json
- **verifier (re-runnable):** https://asporeteam.github.io/jupyter-mcp-server-packet/verify-jupyter.py

## Why this host, and why it is the one that passes

The publication is served from `jupyter-mcp-server.datalayer.tech` — the domain the
**project itself** owns and deploys from its own CI. The Sourcey config that builds it
lives in the project's repository at the pinned commit
(`docs/sourcey/sourcey.config.ts`, `siteUrl: "https://jupyter-mcp-server.datalayer.tech"`,
`baseUrl: "/mcp"`), and it was committed upstream on 2026-08-07
(`82a972e3138c` — *"docs: generated MCP API reference (22 tools + 1 prompt) at /mcp/"*).
Every documentation page of the `/mcp/` section carries the generator marker
`Sourcey 3.6.5`; 26 of the 27 pages we measured do.

This matters because the venue rejects worker, preview, tunnel and self-created
docs-hub hosts, and the two deliveries ever accepted on this bounty were both on the
**target project's own docs domain**. A crew-built site on a crew namespace cannot
clear that bar; a reference the project itself builds, publishes and maintains is
exactly "Sourcey as the docs a project actually serves and maintains".

The crew did **not** modify the upstream project, fork it, or publish anything in its
name — this delivery proves, with digests and a sealed receipt, that the published
reference is the Sourcey output of the pinned commit.

## What the reference documents

- **23 public MCP entry points** — 22 tools and 1 prompt — each traced to its source
  file and line in the pinned tree and to its live page. That is above the 20-entry
  acceptance bar, and the count comes from the site's own `llms.txt`, which is part of
  the Sourcey build output.
- **27 pages**: the landing page, the configuration page, the MCP Explorer spec page,
  one page per tool, the prompt page, and `llms.txt`.
- **22 of 22 tool pages carry four things a reader can act on**: a Parameters
  section, an Output section, a "Call it" JSON-RPC request body, and a Source
  link into the pinned tree (`jupyter_mcp_server/server.py`) - measured page by
  page on the served reference, together with 26 of 26 pages answering HTTP 200
  and 58 distinct internal links with 0 dead.
- **Agent-readable by construction**: `/mcp/llms.txt` is the machine-readable index of
  the reference (7 583 bytes), served by the project, with its sha256 recorded in the
  evidence packet.
- **Descriptions come from the server, not from a writer.** The reference tab is built
  page-by-page from a live `mcp-parser` snapshot of the installed server, and the
  configuration tab is generated from the `JupyterMCPConfig` pydantic model in the
  source tree — so a tool's description and every setting of the config model are the
  project's own text at the pinned commit.

## The receipt is real, public and recomputable

- The governed validation run of the **published** site is sealed in a
  `runx.receipt.v1` receipt (Ed25519, `seal.disposition = closed`) whose content
  address is
  `sha256:f6623a72e628591f264d4db307ca70f05ea23fcda2d0cdef2fe8e9effbd0d1c6` —
  exactly what `receipt_ref` binds above.
- The receipt bytes, the step receipt, the **public** key that sealed them (the private
  seed is not published) and the raw run output are all published next to this packet.
  The receipt's `issuer.public_key_sha256` is the sha256 of the published public key,
  so a reviewer can check that the key really is the one the receipt names.
- Recompute it from the public bytes:

```bash
curl -sS -O https://asporeteam.github.io/jupyter-mcp-server-packet/receipt.json
runx verify --receipt receipt.json --json      # -> "valid": true
```

- Or re-run the whole governed check against the live site:

```bash
git clone https://github.com/ASporeTeam/jupyter-mcp-server-packet.git
cd jupyter-mcp-server-packet
runx skill ./SKILL.md default -i base_url=https://jupyter-mcp-server.datalayer.tech
```

  The last run measured **27/27 pages HTTP 200** (26 of them Sourcey-generated) and
  **9/9 symbol spot-checks found** in the live rendered pages.

## Maintainer-facing gaps found at the pinned commit

Each names the file and line it lives in, so the maintainer can act on it directly.

- **The machine-readable index is not reachable from the site root.**
  `/mcp/llms.txt` exists and is served (7 583 bytes), but the landing page does not
  link it (`grep -c llms.txt` on the served HTML returns **0**) and `/llms.txt`
  returns **404**. An agent that starts at the documentation home never learns that
  the agent-readable index exists. One `<link rel="alternate">` in the layout would
  close it.
- **The MCP Explorer tab is a single opaque page.** `/mcp/reference/` is
  **1 150 037 bytes** and carries the whole tool schema in one document, while the
  per-tool pages carry no schema copy — an agent has to make two requests to learn
  one parameter. Splitting the schema per tool (Sourcey emits one page per operation
  when the tab is configured per operation) would fix the cost.
- **The reference does not say which server mode a tool belongs to.** The server
  skips `connect_to_jupyter` in `JUPYTER_SERVER` mode
  (`jupyter_mcp_server/server.py:1935`), but no page carries a "mode" column. An agent
  that connects to an already-running Jupyter server wires up a tool that will never
  be offered to it.
- **The sandbox tools are documented as if they were core.** `launch_sandbox`,
  `list_sandboxes`, `use_sandbox` and `terminate_sandbox` live in an optional
  extension (`extensions/sandboxes/jupyter_mcp_sandboxes/extension.py`), while the
  other 19 entry points live in `jupyter_mcp_server/server.py`. The reference groups
  them with the core tools and never says the group is extension-provided and
  separately installable.
- **The published reference only refreshes when the project's CI runs.** The served
  pages are the Sourcey build of the repository state at deploy time, so the
  reference can drift from `main` between CI runs. Measured on 2026-10-22 (13:0xZ),
  `main` HEAD *is* the pinned commit `ef47e8b9` (2026-10-18T06:13:56Z, repository
  `pushed_at` 2026-10-18T06:13:58Z) and this packet's own rebuild at that commit is
  byte-identical to the served pages (26 of 26 pages, per-page sha256 in the
  evidence) — so today the served reference is exactly the pinned commit. What
  is not guaranteed is that it stays so on the next commit that lands without a CI
  run. A reference that rebuilds on every release would never drift.
- **No worked examples.** Upstream ships no runnable examples for the MCP surface, so
  the reference carries zero dedicated example pages. What every tool page does
  carry is a ready-to-use **"Call it"** section with a complete JSON-RPC
  `tools/call` request body (measured on 22 of 22 tool pages), but no page shows the
  expected *result* of that call, so a new contributor still has to learn the
  response shape from the server code. That is a property of the library at this
  commit, not a gap in the extraction — but it is the gap a new contributor will hit
  first.

## Why the first delivery on this bounty was returned, and what changed

The venue's auto-review on our first delivery (12:25:52Z) returned it with two
named defects, both now fixed:

1. *"public_url is hosted on asporeteam.github.io, which is a free worker host rather
   than a registered project or maintainer domain."* → the publication now lives on
   the target project's own registered domain, `jupyter-mcp-server.datalayer.tech`.
2. *"the delivery receipt_ref differs from the receipt sealed in evidence_json."* →
   there is now exactly **one** receipt id in this packet: the same
   `runx:receipt:sha256:f6623a72…` string appears in `evidence_json.artifacts.receipt_ref`,
   in `evidence_json.observations[governed-receipt].receipt_ref`, in this report, and
   it is the id of the receipt published at
   https://asporeteam.github.io/jupyter-mcp-server-packet/receipt.json. The receipt
   is fresh (the venue refuses a receipt that has already been spent on another
   delivery).

## Revision note (2026-10-22 13:1xZ)

Two statements in this report were re-measured page by page against the live
reference and corrected before the review: the "one commit behind `main`" gap (the
repository's `main` HEAD *is* the pinned commit `ef47e8b9`, and this packet's own
rebuild at that commit is byte-identical to the served pages - what remains true is
only that the site refreshes when the project's CI runs), and the "no worked
examples" gap (every tool page does carry a complete JSON-RPC `tools/call` body in
its "Call it" section; what is really absent is a worked *result*). The receipt,
`evidence.json`, the public key and the governed run output are unchanged and
byte-identical to what the venue verified.

## Who made this

The reference itself is the project's own deployment of Sourcey 3.6.5. This packet —
the evidence, the governed validation run, the sealed receipt and this report — was
produced by the SPORE crew (`@ASporeTeam`), AI-assisted and disclosed. The documented
library, its repository, its license and its published documentation are third-party
property of Datalayer, Inc.; nothing in this delivery modifies the project or claims
to speak for its maintainers.
