"""
Minimal stand-in for PyGObject's `gi` module.

The app under test is a single GTK script; importing it normally requires a
working PyGObject/GTK install. The parsing/formatting logic exercised by
these tests never touches real widgets, so we install fake `gi`/`gi.repository`
modules that hand back a harmless dummy class for any attribute access
(Gtk.Window, Gtk.ResponseType.CANCEL, etc.). This lets the test suite import
and exercise the app's logic on any machine, GTK or not.
"""
import sys
import types


def _make_dummy_class(name):
    def _init(self, *a, **k):
        pass

    return type(name, (object,), {"__init__": _init})


class _AutoModule(types.ModuleType):
    """Returns a fresh dummy class/object for any attribute access."""

    def __getattr__(self, name):
        val = _make_dummy_class(name)
        setattr(self, name, val)
        return val


def install_stub_gi():
    gi = types.ModuleType("gi")
    gi.require_version = lambda *a, **k: None
    repo_pkg = types.ModuleType("gi.repository")

    for modname in ["Gtk", "GLib", "Gio", "GdkPixbuf", "Gdk", "AyatanaAppIndicator3", "AppIndicator3"]:
        mod = _AutoModule(f"gi.repository.{modname}")
        setattr(repo_pkg, modname, mod)
        sys.modules[f"gi.repository.{modname}"] = mod

    gi.repository = repo_pkg
    sys.modules["gi"] = gi
    sys.modules["gi.repository"] = repo_pkg
