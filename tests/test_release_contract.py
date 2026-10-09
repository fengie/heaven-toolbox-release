import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from verify_release_repo import validate

class LockedReleaseContractTests(unittest.TestCase):
    def test_valid_empty_repo_contract(self):
        x = validate()
        self.assertFalse(x["publication_enabled"])
        self.assertEqual(x["releases"], [])

    def test_wrong_repo_and_source_rejected(self):
        for key, value in [("repository", "fengie/heaven-mod-manager-release"),
                           ("source_repository", "fengie/Heaven-Mod_Manager"),
                           ("publication_enabled", True),
                           ("releases", [{"tag": "updater-main-480"}])]:
            self._expect_bad_index(key, value)

    def _expect_bad_index(self, field, value):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            (p / ".heaven").mkdir()
            (p / ".heaven/update-policy.json").write_bytes(
                (ROOT / ".heaven/update-policy.json").read_bytes())
            obj = json.loads((ROOT / "release-index.json").read_text())
            obj[field] = value
            (p / "release-index.json").write_text(json.dumps(obj))
            with self.assertRaisesRegex(ValueError, "not locked"):
                validate(p)

    def test_policy_paths_and_repo_identity(self):
        p = json.loads((ROOT / ".heaven/update-policy.json").read_text())
        self.assertEqual(p["repository"], "fengie/heaven-toolbox-release")
        self.assertEqual(p["source_update"]["strategy"], "ff-only")
        for item in p["runtime_update"]["evidence_paths"]:
            self.assertTrue((ROOT / item).is_file(), item)

    def test_no_release_publishing_workflow(self):
        w = (ROOT / ".github/workflows/release-repo-policy.yml").read_text()
        self.assertIn("contents: read", w)
        self.assertNotIn("contents: write", w)
        self.assertNotIn("id-token: write", w)
        self.assertIn("--live", w)

    def test_private_source_not_tracked_in_public_channel(self):
        result = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True,
                                text=True, check=True)
        for path in result.stdout.splitlines():
            self.assertFalse(path.startswith(("src/", "plugins/", "apps/")))
            self.assertFalse(path.endswith((".zip", ".exe", ".dll", ".pfx", ".key")))

if __name__ == "__main__":
    unittest.main()
