#!/usr/bin/env python3
"""Governed validation run for the published Sourcey documentation site of
datalayer/jupyter-mcp-server (Frantic bounty #33).

Fetches the published site over plain HTTPS (the project's own registered
domain), checks that every page a reviewer would open answers 200, spot-checks
the documented MCP surface against the rendered pages, recomputes the digest of
the upstream Sourcey config AT THE PINNED COMMIT, and records the pinned commit
identity.  Prints one JSON object on stdout.  No writes, no spending.
"""
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64) spore-agent3-jupyter-verify/1.0"

PINNED_COMMIT = "ef47e8b9c9bfce1a23265831a1ad80f94d58bb85"
REPO = "datalayer/jupyter-mcp-server"
RAW_CONFIG = ("https://raw.githubusercontent.com/%s/%s/docs/sourcey/sourcey.config.ts"
              % (REPO, PINNED_COMMIT))
RAW_LICENSE = ("https://raw.githubusercontent.com/%s/%s/LICENSE" % (REPO, PINNED_COMMIT))

PAGES = [
    "/mcp/",
    "/mcp/configuration/",
    "/mcp/reference/",
    "/mcp/prompts/jupyter-cite/",
    "/mcp/tools/connect-to-jupyter/",
    "/mcp/tools/list-files/",
    "/mcp/tools/list-kernels/",
    "/mcp/tools/use-notebook/",
    "/mcp/tools/list-notebooks/",
    "/mcp/tools/read-notebook/",
    "/mcp/tools/restart-notebook/",
    "/mcp/tools/unuse-notebook/",
    "/mcp/tools/insert-cell/",
    "/mcp/tools/overwrite-cell-source/",
    "/mcp/tools/edit-cell-source/",
    "/mcp/tools/execute-cell/",
    "/mcp/tools/insert-execute-code-cell/",
    "/mcp/tools/read-cell/",
    "/mcp/tools/delete-cell/",
    "/mcp/tools/clear-cell-output/",
    "/mcp/tools/move-cell/",
    "/mcp/tools/execute-code/",
    "/mcp/tools/launch-sandbox/",
    "/mcp/tools/list-sandboxes/",
    "/mcp/tools/use-sandbox/",
    "/mcp/tools/terminate-sandbox/",
    "/mcp/llms.txt",
]

SPOT_CHECKS = [
    ("/mcp/", "Jupyter MCP Server", "the landing page names the documented project"),
    ("/mcp/", "sourcey", "the landing page carries the Sourcey generator markers"),
    ("/mcp/", "datalayer/jupyter-mcp-server", "the landing page links the source repository"),
    ("/mcp/configuration/", "JupyterMCPConfig", "the configuration page documents the config model"),
    ("/mcp/tools/use-notebook/", "use_notebook", "the use_notebook tool page documents the tool"),
    ("/mcp/tools/connect-to-jupyter/", "connect_to_jupyter",
     "the connect_to_jupyter tool page documents the tool"),
    ("/mcp/tools/launch-sandbox/", "launch_sandbox", "the launch_sandbox tool page documents the tool"),
    ("/mcp/prompts/jupyter-cite/", "jupyter_cite", "the prompt page documents the jupyter_cite prompt"),
    ("/mcp/llms.txt", "22 tools and 1 prompt", "llms.txt states the documented MCP surface"),
]


def fetch(url, timeout=45):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
    except Exception as exc:  # noqa: BLE001 - a transport error is a fact
        return 0, ("error: %s" % exc).encode()


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def main():
    base = os.environ.get("RUNX_INPUT_BASE_URL") or "https://jupyter-mcp-server.datalayer.tech"
    base = base.rstrip("/")

    page_results = []
    for p in PAGES:
        status, body = fetch(base + p)
        page_results.append({"path": p, "status": status, "bytes": len(body)})

    checks = []
    for path, needle, why in SPOT_CHECKS:
        status, body = fetch(base + path)
        try:
            text = body.decode("utf-8", "replace")
        except Exception:  # noqa: BLE001
            text = str(body)
        checks.append({"path": path, "needle": needle, "why": why,
                       "http_status": status, "found": needle in text})

    artifacts = {}
    status, body = fetch(RAW_CONFIG)
    if status == 200:
        artifacts["docs/sourcey/sourcey.config.ts @ " + PINNED_COMMIT] = {
            "url": RAW_CONFIG, "sha256": sha256_bytes(body), "bytes": len(body)}
    status, body = fetch(RAW_LICENSE)
    if status == 200:
        artifacts["LICENSE @ " + PINNED_COMMIT] = {
            "url": RAW_LICENSE, "sha256": sha256_bytes(body), "bytes": len(body)}
    status, body = fetch(base + "/mcp/llms.txt")
    if status == 200:
        artifacts["published llms.txt"] = {
            "url": base + "/mcp/llms.txt", "sha256": sha256_bytes(body), "bytes": len(body)}

    tools = 0
    prompts = 0
    status, body = fetch(base + "/mcp/llms.txt")
    if status == 200:
        text = body.decode("utf-8", "replace")
        tools = text.count("](/mcp/tools/")
        prompts = text.count("](/mcp/prompts/")

    result = {
        "base_url": base,
        "target_repo": "https://github.com/" + REPO,
        "pinned_commit": PINNED_COMMIT,
        "pages_checked": len(page_results),
        "pages_ok": sum(1 for p in page_results if p["status"] == 200),
        "page_results": page_results,
        "spot_checks_total": len(checks),
        "spot_checks_passed": sum(1 for c in checks if c["found"] and c["http_status"] == 200),
        "spot_checks": checks,
        "documented_tools": tools,
        "documented_prompts": prompts,
        "artifacts": artifacts,
        "verdict": "PASS" if (all(p["status"] == 200 for p in page_results)
                               and all(c["found"] for c in checks)) else "FAIL",
    }
    print(json.dumps({"message": json.dumps(result, sort_keys=True)}))
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
