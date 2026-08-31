# Gnome Startup Applications Manager

A powerful, modern, and minimalist GTK-based manager for GNOME startup applications, built entirely in Python. Now featuring a full-fledged Task Scheduler (Cron alternative) backed by `systemd --user`.

**Supports both English and Turkish natively! (Auto-detects system language)**

![GNOME Startup Applications Manager](screenshot.png) *(Note: Placeholder for screenshot)*

## Features

- **True PID Tracking:** Never accidentally kill the wrong background process. Accurately tracks PIDs.
- **Resource Usage:** Real-time monitoring of CPU (%) and RAM (MB/GB) usage for each startup script/app.
- **Task Scheduler (Cron Alternative):** Schedule tasks to run at Boot, Login, at Specific Intervals (e.g., every 30 mins), or at Specific Dates/Times.
- **Lingering Support:** Scheduled background tasks can run on system boot without requiring you to log in first.
- **Run in Terminal:** Optionally run any startup script or scheduled task inside a visible GNOME Terminal window.
- **Multi-Select:** Start, Stop, or Delete multiple apps at the same time.
- **Keyboard Shortcuts:** Fast management via `Ctrl+N` (New), `Ctrl+E` (Edit), `Ctrl+S` (Start), `Ctrl+K` (Kill), `Delete` (Remove).
- **Persistent Settings:** Remembers your window size and position natively.
- **System Tray (Indicator):** Can run silently in the background and be managed via the System Tray.

## Installation

No complex dependencies! Just clone and run:

```bash
git clone https://github.com/Nikolayco/Gnome-Startup-Applications-Manager.git
cd Gnome-Startup-Applications-Manager
python3 baslangic-yoneticisi.py
```

## Contributing
Pull requests are welcome! I built this tool to solve my own desktop management issues, but I hope it helps the wider Linux community.

---
*Developed by Nikolayco*
