"""scripts/install_agents.py: copies the shipped members into the live agents folder, never
touches an agent that is not ours, keeps a member the user changed, saves a differing file
when there is no record to go by, and exits non-zero when the panel is not whole."""
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = pathlib.Path(__file__).resolve().parent.parent


class InstallAgentsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        base = pathlib.Path(self.tmp.name)
        self.skill = base / "skill"
        (self.skill / "scripts").mkdir(parents=True)
        (self.skill / "agents").mkdir()
        shutil.copy(REPO / "scripts" / "install_agents.py", self.skill / "scripts")
        for name in ("council-taleb.md", "council-rams.md"):
            (self.skill / "agents" / name).write_text(f"{name} v1\n", encoding="utf-8")
        self.live = base / "live-agents"
        self.solnest = base / ".solnest"
        self.record = self.skill / ".council-agents.json"

    def run_it(self, *args):
        env = dict(os.environ, SOLNEST_COUNCIL_AGENTS_DIR=str(self.live), SOLNEST_HOME=str(self.solnest))
        return subprocess.run([sys.executable, str(self.skill / "scripts" / "install_agents.py"), *args],
                              env=env, capture_output=True, text=True, timeout=60)

    def ship(self, name, text):
        (self.skill / "agents" / name).write_text(text, encoding="utf-8")

    def test_installs_all_and_leaves_other_agents_alone(self):
        self.live.mkdir()
        (self.live / "my-own-agent.md").write_text("mine\n", encoding="utf-8")
        (self.live / "council-extra-i-wrote.md").write_text("mine too\n", encoding="utf-8")
        r = self.run_it()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("[ok] agents    2 of 2", r.stdout)
        self.assertEqual((self.live / "council-taleb.md").read_text(), "council-taleb.md v1\n")
        self.assertEqual((self.live / "my-own-agent.md").read_text(), "mine\n")
        self.assertEqual((self.live / "council-extra-i-wrote.md").read_text(), "mine too\n")
        self.assertEqual(sorted(json.loads(self.record.read_text())), ["council-rams.md", "council-taleb.md"])

    def test_a_new_release_replaces_untouched_members_and_keeps_an_edited_one(self):
        self.run_it()
        (self.live / "council-rams.md").write_text("rams, edited by the user\n", encoding="utf-8")
        self.ship("council-taleb.md", "taleb v2\n")
        self.ship("council-rams.md", "rams v2\n")
        r = self.run_it()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("Kept your own version of: council-rams.md", r.stdout)
        self.assertEqual((self.live / "council-taleb.md").read_text(), "taleb v2\n")
        self.assertEqual((self.live / "council-rams.md").read_text(), "rams, edited by the user\n")
        self.ship("council-rams.md", "rams v3\n")                 # and at the release after that
        self.run_it()
        self.assertEqual((self.live / "council-rams.md").read_text(), "rams, edited by the user\n")
        (self.live / "council-rams.md").unlink()                  # delete it to get the standard one back
        self.run_it()
        self.assertEqual((self.live / "council-rams.md").read_text(), "rams v3\n")

    def test_going_back_a_version_puts_the_old_members_back(self):
        self.run_it()
        self.ship("council-taleb.md", "taleb v2\n")
        self.run_it()
        self.ship("council-taleb.md", "council-taleb.md v1\n")    # what --undo does to the skill folder
        self.run_it()
        self.assertEqual((self.live / "council-taleb.md").read_text(), "council-taleb.md v1\n")

    def test_no_record_and_no_baseline_saves_the_differing_file_first(self):
        self.live.mkdir()
        (self.live / "council-taleb.md").write_text("an older or edited copy\n", encoding="utf-8")
        r = self.run_it()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual((self.live / "council-taleb.md").read_text(), "council-taleb.md v1\n")
        saved = list((self.solnest / "council" / "agents-saved").glob("council-taleb.md.*"))
        self.assertEqual(len(saved), 1)
        self.assertEqual(saved[0].read_text(), "an older or edited copy\n")

    def test_baseline_tells_an_old_copy_from_an_edited_one(self):
        """An install from before the record existed: the old skill folder's copies are the baseline."""
        base = pathlib.Path(self.tmp.name) / "before"
        base.mkdir()
        (base / "council-taleb.md").write_text("taleb v0\n", encoding="utf-8")
        (base / "council-rams.md").write_text("rams v0\n", encoding="utf-8")
        self.live.mkdir()
        (self.live / "council-taleb.md").write_text("taleb v0\n", encoding="utf-8")          # just older
        (self.live / "council-rams.md").write_text("rams v0, edited\n", encoding="utf-8")    # the user's
        r = self.run_it("--baseline", str(base))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual((self.live / "council-taleb.md").read_text(), "council-taleb.md v1\n")
        self.assertEqual((self.live / "council-rams.md").read_text(), "rams v0, edited\n")
        self.assertFalse((self.solnest / "council" / "agents-saved").exists())

    def test_a_member_dropped_by_a_release_is_removed_unless_edited(self):
        self.ship("council-gone.md", "gone v1\n")
        self.ship("council-gone-edited.md", "gone-edited v1\n")
        self.run_it()
        (self.live / "council-gone-edited.md").write_text("user version\n", encoding="utf-8")
        (self.skill / "agents" / "council-gone.md").unlink()
        (self.skill / "agents" / "council-gone-edited.md").unlink()
        r = self.run_it()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertFalse((self.live / "council-gone.md").exists())
        self.assertEqual((self.live / "council-gone-edited.md").read_text(), "user version\n")

    def test_check_changes_nothing_and_fails_on_a_short_panel(self):
        r = self.run_it("--check")
        self.assertEqual(r.returncode, 1)
        self.assertIn("[!!] agents    0 of 2", r.stdout)
        self.assertFalse(self.live.exists())
        self.assertFalse(self.record.exists())

    def test_no_shipped_members_is_a_failure(self):
        shutil.rmtree(self.skill / "agents")
        r = self.run_it()
        self.assertEqual(r.returncode, 1)

    def test_the_repo_ships_18_members(self):
        self.assertEqual(len(list((REPO / "agents").glob("council-*.md"))), 18)


if __name__ == "__main__":
    unittest.main()
