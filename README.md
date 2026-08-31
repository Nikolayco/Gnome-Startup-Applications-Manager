# GNOME Startup Applications Manager

🌍 **[Türkçe](README.tr.md) | English | [Русский](README.ru.md) | [Български](README.bg.md)**

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
- **Manual Trigger** — "Run Now" button to test a task immediately
- **Lingering Support** — one-click `loginctl enable-linger` from Settings

### General
- **Keyboard Shortcuts** — `Ctrl+N` (New), `Ctrl+E` (Edit), `Ctrl+S` (Start), `Ctrl+K` (Kill), `Delete` (Remove)
- **System Tray** — runs silently in background with tray icon
- **Persistent Window State** — remembers size and position
- **Multi-language** — Turkish 🇹🇷, English 🇬🇧, Russian 🇷🇺, Bulgarian 🇧🇬

---

## 🚀 Installation

```bash
git clone https://github.com/Nikolayco/Gnome-Startup-Applications-Manager.git
cd Gnome-Startup-Applications-Manager
python3 baslangic-yoneticisi.py
```

**Requirements:** Python 3.8+, GTK 3, systemd

---

*Developed by Nikolayco — Version 1.1*

---

## 🗑️ Uninstallation

To completely remove the application and all its data:

```bash
# Remove the application binary
rm -f ~/.local/bin/baslangic-yoneticisi

# Remove all app data (PID files, settings, runner script)
rm -rf ~/.local/share/Gnome-Startup-Applications-Manager/

# Remove all scheduled tasks (systemd timers created by the app)
for f in ~/.config/systemd/user/gsam-*.timer ~/.config/systemd/user/gsam-*.service; do
    [ -f "$f" ] && systemctl --user disable --now "$(basename $f)" 2>/dev/null
    rm -f "$f"
done
systemctl --user daemon-reload

# Remove autostart entries created by the app
rm -f ~/.config/autostart/gsam-*.desktop
```

> **Note:** Your own `.desktop` autostart entries (apps you added manually) will NOT be deleted by this process. Only files created by this application are removed.
