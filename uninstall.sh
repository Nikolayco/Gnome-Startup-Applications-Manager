#!/bin/bash

echo "Kaldırılıyor / Uninstalling GNOME Startup Applications Manager..."
echo ""

# Uygulama binary
rm -f "$HOME/.local/bin/baslangic-yoneticisi"
echo "✓ Uygulama dosyası kaldırıldı."

# Uygulama verisi (PID, settings, runner.py, logs)
rm -rf "$HOME/.local/share/Gnome-Startup-Applications-Manager/"
echo "✓ Uygulama verileri kaldırıldı."

# .desktop launcher
rm -f "$HOME/.local/share/applications/baslangic-yoneticisi.desktop"
echo "✓ Uygulama başlatıcısı kaldırıldı."

# Zamanlayıcı (systemd user timers/services created by the app)
for f in "$HOME/.config/systemd/user/gsam-"*.timer "$HOME/.config/systemd/user/gsam-"*.service; do
    [ -f "$f" ] && systemctl --user disable --now "$(basename "$f")" 2>/dev/null
    rm -f "$f"
done
systemctl --user daemon-reload 2>/dev/null
echo "✓ Zamanlanmış görevler kaldırıldı."

# Autostart entries created by the app
rm -f "$HOME/.config/autostart/gsam-"*.desktop
echo "✓ Autostart girdileri kaldırıldı."

echo ""
echo "✅ Tamamlandı! / Uninstallation complete!"
echo "   Kendi eklediğiniz başlangıç uygulamaları silinmedi."
echo "   Your own startup entries were NOT removed."
