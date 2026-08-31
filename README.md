# GNOME Startup Applications Manager

🌍 **[Türkçe](README.tr.md) | English | [Русский](README.ru.md) | [Български](README.bg.md)**

---

> I was looking for a single application that could both manage GNOME startup applications **and** work as a proper task scheduler — running scripts at specific intervals, on boot, or at a set time. I couldn’t find anything that did both well, so I built it myself.

---

A powerful, modern GTK-based manager for GNOME startup applications with a full-fledged **Task Scheduler** backed by `systemd --user`. Built entirely in Python — zero extra dependencies.

The application **automatically detects your system language** and displays in Turkish, English, Russian, or Bulgarian.

---

## ✨ Features

### Startup Manager
- **Real Application Icons** — shows `.desktop` icons instead of generic ones
- **Live Status & Resource Usage** — real-time CPU (%) and RAM (MB/GB) per app with PID tracking
- **Multi-Select** — start, stop, or delete multiple apps simultaneously
- **Safe Process Stopping** — uses PID files; never kills the wrong process
- **Terminal Mode** — optionally open scripts in a visible GNOME Terminal window
- **Startup Delay** — configure per-app delay in seconds

### Task Scheduler (Cron Alternative)
- **Interval** — run every N minutes / hours / days
- **Calendar** — run on specific days and times (e.g. every Monday at 09:00)
- **Boot** — run at system startup (background, no login required with Lingering)
- **Login** — run when you open a session
- **Manual Trigger** — “Run Now” button to test a task immediately
- **Lingering Support** — one-click `loginctl enable-linger` from Settings

### General
- **System Tray** — runs silently in background with tray icon
- **Persistent Window State** — remembers size and position
- **Multi-language** — Turkish 🇹🇷, English 🇬🇧, Russian 🇷🇺, Bulgarian 🇧🇬

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Function |
|----------|----------|
| `Ctrl + N` | Add a new startup application |
| `Ctrl + E` | Edit selected application |
| `Ctrl + S` | Start selected application |
| `Ctrl + K` | Stop (kill) selected application |
| `Delete` | Delete selected application |
| `Ctrl + F` | Focus the search box |

---

## 🚀 Installation

```bash
git clone https://github.com/Nikolayco/Gnome-Startup-Applications-Manager.git
cd Gnome-Startup-Applications-Manager
python3 baslangic-yoneticisi.py
```

**Requirements:** Python 3.8+, GTK 3, systemd

---

## 🗑️ Uninstallation

```bash
rm -f ~/.local/bin/baslangic-yoneticisi
rm -rf ~/.local/share/Gnome-Startup-Applications-Manager/

for f in ~/.config/systemd/user/gsam-*.timer ~/.config/systemd/user/gsam-*.service; do
    [ -f "$f" ] && systemctl --user disable --now "$(basename $f)" 2>/dev/null
    rm -f "$f"
done
systemctl --user daemon-reload

rm -f ~/.config/autostart/gsam-*.desktop
```

> **Note:** Your own `.desktop` autostart entries will NOT be deleted — only files created by this application are removed.

---

*Developed by Nikolayco — Version 1.1*
