import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
def module(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result

class BuildContractTests(unittest.TestCase):
    def test_release_rejects_wrong_identity_and_dirty_tree(self):
        release = module("release", ".github/rpg-runtime/build-release.py")
        fork = json.loads((ROOT / "retrom-fork.json").read_text())
        commit = "a" * 40
        with patch.object(release, "git", side_effect=[commit, " M retrom/bridge.c"]):
            with self.assertRaisesRegex(ValueError, "RELEASE_SOURCE_DIRTY"):
                release.validate_identity(fork["forkRepository"], "retrom-core-gfd1c0686f8b4-r1", commit, fork)
        with self.assertRaisesRegex(ValueError, "RELEASE_TAG_INVALID"):
            release.validate_identity(fork["forkRepository"], "latest", commit, fork)

    def test_notices_include_engine_sdl_and_libretro_authors(self):
        notices = module("notices", "retrom/licenses.py").render()
        self.assertIn("GNU GENERAL PUBLIC LICENSE", notices)
        self.assertIn("GNU LESSER GENERAL PUBLIC LICENSE", notices)
        self.assertIn("Sam Lantinga", notices)
        self.assertIn("The RetroArch team", notices)
        self.assertIn("Permission is hereby granted", notices)
        self.assertLess(len(notices.encode()), 1024 * 1024)
