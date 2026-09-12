#!/usr/bin/env python3
"""Collect unchanged notices from the pinned core and bundled SDL/libretro source."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def render():
    sections = ["NXEngine Retrom browser core\nUpstream: libretro/nxengine-libretro\n"
                "Source baseline: fd1c0686f8b4c0aea9b5addbc077e3ad7da23bb7\n"
                "Game data is supplied separately and is not included in this core.\n"]
    for name in ("nxengine/LICENSE", "retrom/licenses/LGPL-2.1.txt"):
        sections.append(f"\n=== {name} ===\n" + (ROOT / name).read_text())
    notices = {}
    for file in sorted((ROOT / "nxengine").rglob("*")):
        if file.suffix not in {".c", ".cpp", ".h", ".hpp"}:
            continue
        contents = file.read_text(errors="replace")
        for match in re.finditer(r"/\*[\s\S]*?\*/|(?://[^\n]*\n)+", contents):
            text = match.group()
            if re.search(r"copyright|permission is hereby|redistribut|warranty|license", text, re.I):
                notices.setdefault(text, []).append(str(file.relative_to(ROOT)))
    for text, paths in notices.items():
        sections.append("\n=== Source notices: " + ", ".join(paths) + " ===\n" + text)
    return "\n".join(sections)


if __name__ == "__main__":
    Path(sys.argv[1]).write_text(render())
