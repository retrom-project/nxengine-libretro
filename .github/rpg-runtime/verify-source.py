#!/usr/bin/env python3
"""Verify the fixed NXEngine engine and storage provenance."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
BASELINE = "fd1c0686f8b4c0aea9b5addbc077e3ad7da23bb7"

def main():
    fork = json.loads((ROOT / "retrom-fork.json").read_text())
    assert fork["schemaVersion"] == 1
    assert fork["forkRepository"] == "https://github.com/retrom-project/nxengine-libretro"
    assert fork["defaultBranch"] == "retrom/gfd1c0686f8b4"
    assert fork["upstreamMirrorBranch"] == "master"
    assert fork["adapterAbi"] == "nxengine-host-v1"
    assert fork["upstreams"] == [
        {"role": "engine", "repository": "https://github.com/libretro/nxengine-libretro", "refType": "COMMIT", "ref": BASELINE, "commit": BASELINE},
    ]
    assert fork["releaseAssets"] == ["nxengine-retrom.mjs", "nxengine-retrom.wasm", "LICENSES.txt", "rpg-runtime-release.json"]
    revision = "HEAD^2" if os.environ.get("GITHUB_EVENT_NAME") == "pull_request" else "HEAD"
    subprocess.run(["git", "merge-base", "--is-ancestor", BASELINE, revision], cwd=ROOT, check=True)
    assert not subprocess.check_output(["git", "rev-list", "--min-parents=2", f"{BASELINE}..{revision}"], cwd=ROOT).strip()
    print("NXEngine fork source contract: ok")

if __name__ == "__main__":
    main()
