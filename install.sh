#!/bin/bash

BIN_DIR="$HOME/.local/bin"
APPS_DIR="$HOME/.local/share/applications"

echo "Kuruluyor / Installing GNOME Startup Applications Manager..."
echo ""

# Sürümü belirle
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    # Git reposu içindeyse dosyanın commit saatini veya mtime'ı al
    if [ -n "$(git status --porcelain -- baslangic-yoneticisi.py)" ]; then
        VER=$(date -r baslangic-yoneticisi.py +v%y%m%d.%H%M%S)
    else
        TS=$(git log -1 --format=%ct -- baslangic-yoneticisi.py)
        if [ -n "$TS" ]; then
            VER=$(date -d @"$TS" +v%y%m%d.%H%M%S)
        else
            VER=$(date -r baslangic-yoneticisi.py +v%y%m%d.%H%M%S)
        fi
    fi
else
    VER=$(date -r baslangic-yoneticisi.py +v%y%m%d.%H%M%S)
fi

# Binary
mkdir -p "$BIN_DIR"
cp baslangic-yoneticisi.py "$BIN_DIR/baslangic-yoneticisi"
chmod +x "$BIN_DIR/baslangic-yoneticisi"

# Versiyonu yerel dosyaya GÖM!
sed -i "s/VERSION = \"AUTO_VERSION\"/VERSION = \"$VER\"/g" "$BIN_DIR/baslangic-yoneticisi"

echo "✓ Uygulama yüklendi (Sürüm: $VER)."

# .desktop
mkdir -p "$APPS_DIR"
cp baslangic-yoneticisi.desktop "$APPS_DIR/baslangic-yoneticisi.desktop"
update-desktop-database "$APPS_DIR" 2>/dev/null || true
echo "✓ Uygulama kısayolu oluşturuldu (App Grid)."

echo ""
echo "✅ Tamamlandı! / Installation complete!"
