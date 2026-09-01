#!/bin/bash

BIN_DIR="$HOME/.local/bin"
APPS_DIR="$HOME/.local/share/applications"

echo "Kuruluyor / Installing GNOME Startup Applications Manager..."
echo ""

# Get true version
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    TS=$(git log -1 --format=%ct -- baslangic-yoneticisi.py)
    VER=$(date -d @"$TS" +v%y%m%d.%H%M%S)
else
    VER=$(date -r baslangic-yoneticisi.py +v%y%m%d.%H%M%S)
fi

# Binary
mkdir -p "$BIN_DIR"
cp baslangic-yoneticisi.py "$BIN_DIR/baslangic-yoneticisi"
chmod +x "$BIN_DIR/baslangic-yoneticisi"

# Inject version
sed -i "s/VERSION = \"AUTO_VERSION\"/VERSION = \"$VER\"/g" "$BIN_DIR/baslangic-yoneticisi"

echo "✓ Uygulama yüklendi (Sürüm: $VER)."

# .desktop (uygulama ızgarasında/app grid'de görünmesi için)
mkdir -p "$APPS_DIR"
cp baslangic-yoneticisi.desktop "$APPS_DIR/baslangic-yoneticisi.desktop"
update-desktop-database "$APPS_DIR" 2>/dev/null || true
echo "✓ Uygulama kısayolu oluşturuldu (App Grid)."

echo ""
echo "✅ Tamamlandı! / Installation complete!"
echo "   Uygulamayı başlatmak için: baslangic-yoneticisi"
echo "   Or launch from your Applications grid."
