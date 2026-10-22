# Frantic #33 delivery packet — Sourcey docs for datalayer/jupyter-mcp-server

This repository is the public delivery packet for the Frantic bounty
**"Publish Sourcey docs for a maintained OSS library"** (bounty #33).

| artifact | URL |
|---|---|
| public_url (the published documentation, on the project's own domain) | https://jupyter-mcp-server.datalayer.tech/mcp/ |
| evidence_json | https://asporeteam.github.io/jupyter-mcp-server-packet/evidence.json |
| report | https://asporeteam.github.io/jupyter-mcp-server-packet/report.md |
| sealed runx receipt | https://asporeteam.github.io/jupyter-mcp-server-packet/receipt.json |
| receipt public key (Ed25519; no private seed) | https://asporeteam.github.io/jupyter-mcp-server-packet/receipt-public-key.json |
| step receipt | https://asporeteam.github.io/jupyter-mcp-server-packet/receipt-step.json |
| governed run output | https://asporeteam.github.io/jupyter-mcp-server-packet/verification-output.json |
| verifier | https://asporeteam.github.io/jupyter-mcp-server-packet/verify-jupyter.py |

## Verify the receipt yourself

```sh
curl -sS -O https://asporeteam.github.io/jupyter-mcp-server-packet/receipt.json
runx verify --receipt receipt.json --json
# -> "valid": true, content address + digest + Ed25519 signature all valid
```

`runx verify` needs the issuer's public key in the runx home
(`~/.runx/keys/local-receipt-ed25519.json`); the public key of this receipt is
published as `receipt-public-key.json` so anybody can check the binding:

```sh
python3 - <<'PY'
import base64, hashlib, json
k = json.load(open("receipt-public-key.json"))
r = json.load(open("receipt.json"))
pub = base64.urlsafe_b64decode(k["public_key_base64"] + "=" * (-len(k["public_key_base64"]) % 4))
print("key binding ok:", "sha256:" + hashlib.sha256(pub).hexdigest() == r["issuer"]["public_key_sha256"])
PY
```

## Re-run the governed check against the live site

```sh
npm i -g @runxhq/cli          # runx-cli 0.10.2
runx skill ./SKILL.md default -i base_url=https://jupyter-mcp-server.datalayer.tech
```

The skill re-fetches the published pages, spot-checks the documented MCP surface and
recomputes the digests of the upstream Sourcey config and LICENSE file at the pinned
commit `ef47e8b9c9bfce1a23265831a1ad80f94d58bb85`. It performs no writes and spends
nothing.

## What is being claimed

The documented library, its repository, its license and the published documentation
are third-party property of Datalayer, Inc. The crew did not modify the upstream
project; this packet proves that the published reference is the Sourcey output of the
pinned commit and that the project itself builds, publishes and maintains it on its
own registered domain.
