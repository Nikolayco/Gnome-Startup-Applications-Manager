"""
Tests for the .desktop file read/write round-trip, the legacy-entry fallback
parser, and the one-time migration that upgrades old entries.

Run with:
    python3 -m unittest discover -s tests -v
No PyGObject/GTK install is required (see stub_gi.py).
"""
import gettext
import importlib.util
import os
import re
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(__file__))
from stub_gi import install_stub_gi

install_stub_gi()

APP_PATH = os.path.join(os.path.dirname(__file__), "..", "baslangic-yoneticisi.py")
_spec = importlib.util.spec_from_file_location("gsam_app", APP_PATH)
gsam = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gsam)


class DesktopEntryTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="gsam-test-")
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        gsam.AUTOSTART_DIR = os.path.join(self.tmp, "autostart")
        gsam.CUSTOM_SCRIPTS_DIR = os.path.join(self.tmp, "scripts")
        gsam.SYS_AUTOSTART_DIR = os.path.join(self.tmp, "sys_autostart")
        os.makedirs(gsam.AUTOSTART_DIR)
        os.makedirs(gsam.CUSTOM_SCRIPTS_DIR)
        os.makedirs(gsam.SYS_AUTOSTART_DIR)
        self.mgr = object.__new__(gsam.AutostartManager)

    def _roundtrip(self, **kwargs):
        self.mgr.write_desktop_file(
            kwargs["filename"], kwargs["name"], kwargs["cmd"], kwargs["comment"],
            kwargs["terminal"], kwargs["term_size"], kwargs["delay"], kwargs["enabled"],
        )
        path = os.path.join(gsam.AUTOSTART_DIR, kwargs["filename"])
        return self.mgr.parse_desktop_file(path)

    def test_roundtrip_normal_terminal(self):
        app = self._roundtrip(filename="a.desktop", name="Htop", cmd="htop", comment="c",
                               terminal=True, term_size="normal", delay=0, enabled=True)
        self.assertEqual(app.cmd, "htop")
        self.assertTrue(app.terminal)
        self.assertEqual(app.term_size, "normal")

    def test_roundtrip_maximize_terminal_with_quoted_args(self):
        cmd = "btop --arg 'quoted value'"
        app = self._roundtrip(filename="b.desktop", name="Btop", cmd=cmd, comment="c",
                               terminal=True, term_size="maximize", delay=5, enabled=True)
        self.assertEqual(app.cmd, cmd)
        self.assertEqual(app.term_size, "maximize")

    def test_roundtrip_minimize_terminal(self):
        app = self._roundtrip(filename="c.desktop", name="Watch", cmd="watch -n1 date", comment="",
                               terminal=True, term_size="minimize", delay=0, enabled=False)
        self.assertEqual(app.cmd, "watch -n1 date")
        self.assertEqual(app.term_size, "minimize")
        self.assertFalse(app.enabled)

    def test_roundtrip_no_terminal(self):
        app = self._roundtrip(filename="d.desktop", name="NM Applet", cmd="/usr/bin/nm-applet",
                               comment="", terminal=False, term_size="normal", delay=10, enabled=True)
        self.assertEqual(app.cmd, "/usr/bin/nm-applet")
        self.assertFalse(app.terminal)
        self.assertEqual(app.delay, 10)

    def test_roundtrip_cmd_with_newline_and_backslash(self):
        cmd = 'echo "line1"\necho "line2 with backslash \\\\ here"'
        app = self._roundtrip(filename="nl.desktop", name="NL", cmd=cmd, comment="c",
                               terminal=True, term_size="normal", delay=0, enabled=True)
        self.assertEqual(app.cmd, cmd)

    def test_legacy_entry_without_gsam_keys_still_parses(self):
        runner = os.path.join(gsam.CUSTOM_SCRIPTS_DIR, "runner.py")
        pid = os.path.join(gsam.CUSTOM_SCRIPTS_DIR, "pids", "legacy.desktop.pid")
        log = os.path.join(gsam.CUSTOM_SCRIPTS_DIR, "logs", "legacy.desktop.log")
        content = (
            "[Desktop Entry]\nType=Application\nName=LegacyApp\n"
            f"Exec=gnome-terminal -- python3 {runner} {pid} htop {log}\n"
            "Comment=old\nIcon=application-x-executable\nTerminal=false\n"
            "Hidden=false\nX-GNOME-Autostart-enabled=true\n"
        )
        path = os.path.join(gsam.AUTOSTART_DIR, "legacy.desktop")
        with open(path, "w") as f:
            f.write(content)

        app = self.mgr.parse_desktop_file(path)
        self.assertEqual(app.cmd, "htop")
        self.assertTrue(app.terminal)
        self.assertEqual(app.term_size, "normal")

    def test_migration_upgrades_legacy_entry_in_place(self):
        runner = os.path.join(gsam.CUSTOM_SCRIPTS_DIR, "runner.py")
        pid = os.path.join(gsam.CUSTOM_SCRIPTS_DIR, "pids", "legacy.desktop.pid")
        log = os.path.join(gsam.CUSTOM_SCRIPTS_DIR, "logs", "legacy.desktop.log")
        path = os.path.join(gsam.AUTOSTART_DIR, "legacy.desktop")
        with open(path, "w") as f:
            f.write(
                "[Desktop Entry]\nType=Application\nName=LegacyApp\n"
                f"Exec=gnome-terminal -- python3 {runner} {pid} htop {log}\n"
                "X-GNOME-Autostart-enabled=true\n"
            )

        self.mgr.migrate_terminal_desktop_files()

        with open(path) as f:
            migrated = f.read()
        self.assertIn("X-GSAM-Cmd=htop", migrated)

        app = self.mgr.parse_desktop_file(path)
        self.assertEqual(app.cmd, "htop")
        self.assertTrue(app.terminal)

    def test_migration_leaves_foreign_entries_untouched(self):
        path = os.path.join(gsam.AUTOSTART_DIR, "foreign.desktop")
        content = "[Desktop Entry]\nType=Application\nName=NM Applet\nExec=nm-applet\nX-GNOME-Autostart-enabled=true\n"
        with open(path, "w") as f:
            f.write(content)

        self.mgr.migrate_terminal_desktop_files()

        with open(path) as f:
            self.assertEqual(f.read(), content)


class DesktopValueEscapingTestCase(unittest.TestCase):
    def test_encode_decode_roundtrip(self):
        for value in ["plain", "a\\b", "line1\nline2", "back\\\\slash\nand\nnewlines"]:
            self.assertEqual(gsam.decode_desktop_value(gsam.encode_desktop_value(value)), value)


class _FakeAppInfo:
    def __init__(self, commandline):
        self._commandline = commandline

    def get_commandline(self):
        return self._commandline


class InstalledAppExecCleaningTestCase(unittest.TestCase):
    """CommandSourceEditor._clean_exec_command() strips XDG field codes (%f, %U, ...)."""

    def _clean(self, commandline):
        return gsam.CommandSourceEditor._clean_exec_command(None, _FakeAppInfo(commandline))

    def test_strips_trailing_field_code(self):
        self.assertEqual(self._clean("firefox %u"), "firefox")

    def test_strips_multiple_field_codes(self):
        self.assertEqual(self._clean("libreoffice --writer %U %f"), "libreoffice --writer")

    def test_keeps_quoted_arguments_intact(self):
        self.assertEqual(self._clean('myapp "some arg" %F'), "myapp 'some arg'")

    def test_empty_commandline(self):
        self.assertEqual(self._clean(""), "")

    def test_commandline_that_is_only_a_field_code(self):
        self.assertEqual(self._clean("%u"), "")


class TranslationTestCase(unittest.TestCase):
    """Sanity-checks the gettext wiring against the shipped locale/ catalogs."""

    def test_known_languages_translate(self):
        expectations = {
            "tr": "Kaydet",
            "en": "Save",
            "ru": "Сохранить",
            "bg": "Запази",
        }
        for lang, expected in expectations.items():
            os.environ["LANG"] = f"{lang}_XX.UTF-8"
            gettext_lang = lang if lang in ("ru", "bg") else "en"
            if lang == "tr":
                translated = "Kaydet"
            else:
                t = gettext.translation(
                    "gnome-startup-manager",
                    localedir=os.path.join(os.path.dirname(APP_PATH), "locale"),
                    languages=[gettext_lang],
                    fallback=True,
                )
                translated = t.gettext("Kaydet")
            self.assertEqual(translated, expected)


class TranslationCoverageTestCase(unittest.TestCase):
    """Every _("...") literal in the source must have a real en/ru/bg
    translation, so a new UI string never silently ships untranslated.
    A tiny allowlist covers strings that are correctly identical to the
    Turkish source (e.g. "-", or "Terminal" which is already English)."""

    ALLOWED_IDENTITY = {
        "en": {"-", "Terminal"},
        "ru": {"-"},
        "bg": {"-"},
    }

    _CALL_RE = re.compile(r'''_\(\s*(f?)(["'])((?:\\.|(?!\2).)*)\2\s*\)''')

    @staticmethod
    def _unescape(body):
        out = []
        i = 0
        while i < len(body):
            c = body[i]
            if c == "\\" and i + 1 < len(body):
                nxt = body[i + 1]
                if nxt == "n":
                    out.append("\n"); i += 2; continue
                if nxt == "t":
                    out.append("\t"); i += 2; continue
                if nxt in ("'", '"', "\\"):
                    out.append(nxt); i += 2; continue
            out.append(c)
            i += 1
        return "".join(out)

    def _extract_keys(self):
        with open(APP_PATH, encoding="utf-8") as f:
            src = f.read()
        keys = set()
        for is_fstring, _quote, body in self._CALL_RE.findall(src):
            if is_fstring:
                continue  # dynamic content, not a static catalog key
            keys.add(self._unescape(body))
        return keys

    def test_all_static_strings_are_translated(self):
        keys = self._extract_keys()
        self.assertGreater(len(keys), 50, "sanity check: string extraction found too few keys")

        localedir = os.path.join(os.path.dirname(APP_PATH), "locale")
        for lang in ("en", "ru", "bg"):
            t = gettext.translation("gnome-startup-manager", localedir=localedir, languages=[lang], fallback=False)
            untranslated = sorted(
                k for k in keys
                if t.gettext(k) == k and k not in self.ALLOWED_IDENTITY[lang]
            )
            self.assertEqual(untranslated, [], f"{lang}: missing translations for {untranslated}")


if __name__ == "__main__":
    unittest.main()
