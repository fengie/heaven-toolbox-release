#!/usr/bin/env python3
"""Fail-closed validation for an EMPTY, not-yet-authorized public Toolbox release."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
REPO = "fengie/heaven-toolbox-release"
SOURCE = "fengie/heaven-toolbox"
BINARY = re.compile(r"\.(?:exe|dll|zip|msi|nupkg|pfx|p12|pem|key)$", re.I)

def validate(root: Path = ROOT) -> dict:
    d = json.loads((root / "release-index.json").read_text(encoding="utf-8"))
    expected = {"schema": "heaven-toolbox/releases/v1", "repository": REPO,
                "source_repository": SOURCE, "publication_enabled": False, "releases": []}
    if d != expected:
        raise ValueError("Toolbox channel not locked to an empty index")
    p = json.loads((root / ".heaven/update-policy.json").read_text(encoding="utf-8"))
    if p.get("repository") != REPO or p.get("kind") != "release-channel":
        raise ValueError("Incorrect canonical release repository identity")
    if p.get("branch") != "main" or p.get("source_update", {}).get("strategy") != "ff-only":
        raise ValueError("Unsupported source update policy")
    if p.get("runtime_update", {}).get("mode") != "release-channel":
        raise ValueError("Incorrect runtime release channel mode")
    if os.environ.get("GITHUB_REPOSITORY", REPO) != REPO:
        raise ValueError("GitHub repository mismatch")
    result = subprocess.run(["git", "-C", str(root), "ls-files", "-z"],
                            capture_output=True, check=True)
    paths = [name.decode("utf-8") for name in result.stdout.split(b"\0") if name]
    if not paths:
        raise ValueError("No tracked source tree")
    for path in paths:
        if BINARY.search(path) or path.startswith(("plugins/", "src/", "apps/")):
            raise ValueError("Public release Git tree contains forbidden source/binary: " + path)
    return d

def remote_empty() -> None:
    url = "https://api.github.com/repos/fengie/heaven-toolbox-release/releases?per_page=100"
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "heaven-toolbox-release-policy"}
    if os.environ.get("GH_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GH_TOKEN"]
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response:
        releases = json.load(response)
    if not isinstance(releases, list) or releases:
        raise ValueError("Publication lock violated: nonempty public GitHub Releases")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true")
    args = parser.parse_args()
    validate()
    if args.live:
        remote_empty()
    print("TOOLBOX_RELEASE_CHANNEL_LOCK_OK")

if __name__ == "__main__":
    main()
