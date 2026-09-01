#!/bin/bash

BIN_DIR="$HOME/.local/bin"
APPS_DIR="$HOME/.local/share/applications"

echo "Kuruluyor / Installing GNOME Startup Applications Manager..."
echo ""

# Binary
mkdir -p "$BIN_DIR"
cp baslangic-yoneticisi.py "$BIN_DIR/baslangic-yoneticisi"
chmod +x "$BIN_DIR/baslangic-yoneticisi"
echo "✓ Uygulama yüklendi."

# .desktop (uygulama ızgarasında/app grid'de görünmesi için)
mkdir -p "$APPS_DIR"
cp baslangic-yoneticisi.desktop "$APPS_DIR/baslangic-yoneticisi.desktop"
update-desktop-database "$APPS_DIR" 2>/dev/null || true
echo "✓ Uygulama kısayolu oluşturuldu (App Grid)."

echo ""
echo "✅ Tamamlandı! / Installation complete!"
echo "   Uygulamayı başlatmak için: baslangic-yoneticisi"
echo "   Or launch from your Applications grid."
