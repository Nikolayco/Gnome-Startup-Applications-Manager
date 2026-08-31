#!/bin/bash

APP_NAME="baslangic-yoneticisi"
BIN_DIR="$HOME/.local/bin"
APP_DIR="$HOME/.local/share/applications"
LOCALE_DIR="$HOME/.local/share/locale"

echo "Kaldırma işlemi başlatılıyor... (Uninstalling...)"

rm -f "$BIN_DIR/${APP_NAME}"
rm -f "$APP_DIR/${APP_NAME}.desktop"

# Sadece bu uygulamaya ait mo dosyalarını bulup sil
find "$LOCALE_DIR" -type f -name "gnome-startup-manager.mo" -delete 2>/dev/null || true

update-desktop-database "$APP_DIR" 2>/dev/null || true

echo "Kaldırma tamamlandı! (Uninstallation complete!)"
