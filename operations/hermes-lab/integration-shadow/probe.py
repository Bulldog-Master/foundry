#!/usr/bin/env python3
"""Read-only Hermes and Ollama as-built probe for the contained Standalone lab."""
import argparse
import http.client
import json
import os
import pathlib
import shutil
import urllib.error
import urllib.request

OLLAMA = "http://127.0.0.1:11434/api/tags"
ALLOWED_ROOT = pathlib.Path("/srv/hermes-lab/foundry-agent")

class RejectRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def open_loopback(url, timeout):
    client = urllib.request.build_opener(
        urllib.request.ProxyHandler({}), RejectRedirects())
    return client.open(url, timeout=timeout)


def probe(opener=open_loopback, which=shutil.which):
    # Always avoid subprocess shells, environment dumps, credentials and model prompts.
    info = {"mode": "SHADOW_READ_ONLY", "execution_enabled": False,
            "authority": "NONE", "hermes": {}, "ollama": {}}
    for name in ("hermes", "hermes-agent"):
        location = which(name)
        if location:
            info["hermes"]["binary_found"] = True
            info["hermes"]["command_name"] = name
            break
    else:
        info["hermes"]["binary_found"] = False
    try:
        with opener(OLLAMA, timeout=5) as response:
            document = json.load(response)
        if not isinstance(document, dict):
            raise ValueError("invalid Ollama response")
        models = document.get("models")
        if not isinstance(models, list):
            raise ValueError("invalid Ollama response")
        info["ollama"] = {
            "reachable": True,
            "model_count": len(models),
            "models": sorted(str(x.get("name", "")) for x in models if isinstance(x, dict))[:25],
        }
    except (ValueError, OSError, http.client.HTTPException) as error:
        if isinstance(error, urllib.error.HTTPError):
            error.close()
        info["ollama"] = {"reachable": False, "model_count": None, "models": []}
    return info

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=pathlib.Path)
    args = parser.parse_args()
    if os.geteuid() == 0:
        parser.error("root execution prohibited")
    state = probe()
    data = json.dumps(state, sort_keys=True, indent=2) + "\n"
    if args.output:
        target = args.output
        # No uncontrolled destinations or overwriting existing evidence.
        if (not target.is_absolute() or ".." in target.parts or target.is_symlink()
                or target.exists() or target.parent != ALLOWED_ROOT):
            parser.error("unsafe output destination")
        fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, "w") as handle:
            handle.write(data)
    else:
        print(data, end="")
if __name__ == "__main__":
    main()
