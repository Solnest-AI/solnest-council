"""install.sh: installs the skill and its 18 members into a (fake) home, writes the launcher,
keeps the user's own files, settings and edited members on a second run, brings an older
copy up to date, never installs a stray .cursor folder or the repo's housekeeping, and
refuses to overwrite a link or a different skill.
Offline: it installs from this copy of the repo, or from a local archive."""
import os
import pathlib
import shutil
import subprocess
import tarfile
import tempfile
import unittest

REPO = pathlib.Path(__file__).resolve().parent.parent
BASH = shutil.which("bash")
SKIP = shutil.ignore_patterns(".git", ".cursor", "__pycache__", ".pytest_cache")
SETTINGS = "configs/auto-route-defaults.yaml"


@unittest.skipUnless(BASH, "needs bash")
class InstallTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = pathlib.Path(self.tmp.name) / "home"
        self.home.mkdir()
        self.dest = self.home / ".claude" / "skills" / "solnest-council"
        self.agents = self.home / ".claude" / "agents"

    def run_install(self, script=None, stdin=None, **extra):
        env = dict(os.environ, HOME=str(self.home), SOLNEST_HOME=str(self.home / ".solnest"))
        env.pop("SOLNEST_COUNCIL_AGENTS_DIR", None)
        env.update(extra)
        args = [BASH, str(script)] if script else [BASH]
        return subprocess.run(args, env=env, capture_output=True, text=True, timeout=300,
                              stdin=stdin or subprocess.DEVNULL, cwd=self.tmp.name)

    def test_installs_and_a_second_run_keeps_what_is_the_users(self):
        r = self.run_install(REPO / "install.sh")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("[ok] updater", r.stdout)
        self.assertIn("[ok] agents    18 of 18", r.stdout)
        for rel in ("SKILL.md", "VERSION", "LICENSE", "SETUP-MODELS.md", "bin/py", "scripts/update.py",
                    "scripts/install_agents.py", "scripts/solnest_autoupdate.py", "scripts/detect-providers.sh",
                    SETTINGS, "agents/council-taleb.md", ".council-agents.json"):
            self.assertTrue((self.dest / rel).is_file(), rel)
        self.assertTrue(os.access(self.dest / "scripts" / "detect-providers.sh", os.X_OK))
        self.assertEqual((self.dest / "VERSION").read_text(), (REPO / "VERSION").read_text())
        for rel in (".cursor", "tests", ".github", ".git", ".gitignore", ".agents-before"):
            self.assertFalse((self.dest / rel).exists(), rel)
        self.assertEqual(len(list(self.agents.glob("council-*.md"))), 18)
        h = subprocess.run([str(self.dest / "bin" / "py"), str(self.dest / "scripts" / "update.py"), "--help"],
                           capture_output=True, text=True, timeout=60)
        self.assertEqual(h.returncode, 0, h.stderr)

        (self.dest / "my-notes.md").write_text("mine\n", encoding="utf-8")
        (self.dest / SETTINGS).write_text("chairman: mine\n", encoding="utf-8")
        (self.dest / "configs" / "provider-model-slots.yaml").write_text("my seats\n", encoding="utf-8")
        (self.agents / "council-taleb.md").write_text("taleb, edited by the user\n", encoding="utf-8")
        (self.agents / "my-own-agent.md").write_text("mine\n", encoding="utf-8")
        r = self.run_install(REPO / "install.sh")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("kept your own " + SETTINGS, r.stdout)
        self.assertIn("Kept your own version of: council-taleb.md", r.stdout)
        self.assertEqual((self.dest / "my-notes.md").read_text(), "mine\n")
        self.assertEqual((self.dest / SETTINGS).read_text(), "chairman: mine\n")
        self.assertEqual((self.dest / "configs" / "provider-model-slots.yaml").read_text(), "my seats\n")
        self.assertEqual((self.agents / "council-taleb.md").read_text(), "taleb, edited by the user\n")
        self.assertEqual((self.agents / "my-own-agent.md").read_text(), "mine\n")

    def test_an_older_copy_is_brought_up_to_date_and_an_edited_member_is_kept(self):
        """A copy installed the old way: the whole folder in skills/, the members in agents/,
        no record of what was installed."""
        (self.dest / "agents").mkdir(parents=True)
        self.agents.mkdir(parents=True)
        (self.dest / "SKILL.md").write_text("---\nname: solnest-council\n---\nold\n", encoding="utf-8")
        (self.dest / "VERSION").write_text("1.1.1\n", encoding="utf-8")
        for p in (REPO / "agents").glob("council-*.md"):
            (self.dest / "agents" / p.name).write_text("old " + p.name + "\n", encoding="utf-8")
            (self.agents / p.name).write_text("old " + p.name + "\n", encoding="utf-8")
        (self.agents / "council-rams.md").write_text("rams, edited by the user\n", encoding="utf-8")
        (self.dest / "START-HERE.md").write_text("# START HERE: Auto-installer (Claude reads this)\n", encoding="utf-8")
        r = self.run_install(REPO / "install.sh")
        self.assertFalse((self.dest / "START-HERE.md").exists())      # the old install guide is taken away
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("[ok] agents    18 of 18", r.stdout)
        self.assertEqual((self.dest / "VERSION").read_text(), (REPO / "VERSION").read_text())
        self.assertEqual((self.agents / "council-taleb.md").read_bytes(), (REPO / "agents" / "council-taleb.md").read_bytes())
        self.assertEqual((self.agents / "council-rams.md").read_text(), "rams, edited by the user\n")
        self.assertFalse((self.dest / ".agents-before").exists())
        self.assertFalse((self.home / ".solnest" / "council" / "agents-saved").exists())

    def test_a_stray_cursor_folder_is_never_installed(self):
        """A sync job can drop private editor rules into any folder: they must not ship."""
        copy = pathlib.Path(self.tmp.name) / "repo"
        shutil.copytree(REPO, copy, ignore=SKIP)
        for where in (copy / ".cursor" / "rules", copy / "agents" / ".cursor" / "rules"):
            where.mkdir(parents=True)
            (where / "private.mdc").write_text("private\n", encoding="utf-8")
        r = self.run_install(copy / "install.sh")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue((self.dest / "SKILL.md").is_file())
        self.assertEqual(list(self.dest.rglob(".cursor")), [])
        self.assertEqual(list(self.dest.rglob("*.mdc")), [])

    def test_piped_install_from_an_archive(self):
        """The `curl ... | bash` path: no local repo, the skill comes from an archive."""
        archive = pathlib.Path(self.tmp.name) / "main.tar.gz"
        with tarfile.open(archive, "w:gz") as tar:
            tar.add(REPO, "solnest-council-main",
                    filter=lambda t: None if any(x in t.name for x in ("__pycache__", ".cursor", "/.git/", ".pytest_cache"))
                    or t.name.endswith("/.git") else t)
        with open(REPO / "install.sh", "rb") as script:
            r = self.run_install(stdin=script, COUNCIL_ARCHIVE_URL=archive.as_uri())
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("downloading the skill", r.stdout)
        self.assertIn("[ok] agents    18 of 18", r.stdout)
        self.assertEqual((self.dest / "VERSION").read_text(), (REPO / "VERSION").read_text())
        self.assertFalse((self.dest / "tests").exists())

    def test_refuses_a_different_skill(self):
        self.dest.mkdir(parents=True)
        (self.dest / "SKILL.md").write_text("---\nname: something-else\n---\n", encoding="utf-8")
        r = self.run_install(REPO / "install.sh")
        self.assertEqual(r.returncode, 3, r.stdout + r.stderr)
        self.assertEqual((self.dest / "SKILL.md").read_text(), "---\nname: something-else\n---\n")
        self.assertFalse((self.dest / "scripts").exists())
        self.assertFalse(self.agents.exists())

    def test_refuses_a_link(self):
        real = self.home / "elsewhere" / "solnest-council"
        real.mkdir(parents=True)
        (real / "SKILL.md").write_text("---\nname: solnest-council\n---\noriginal\n", encoding="utf-8")
        self.dest.parent.mkdir(parents=True)
        self.dest.symlink_to(real)
        r = self.run_install(REPO / "install.sh")
        self.assertEqual(r.returncode, 3, r.stdout + r.stderr)
        self.assertIn("is a link", r.stdout)
        self.assertEqual(sorted(p.name for p in real.iterdir()), ["SKILL.md"])


if __name__ == "__main__":
    unittest.main()
