#!/bin/bash

APP_NAME="baslangic-yoneticisi"
BIN_DIR="$HOME/.local/bin"
APP_DIR="$HOME/.local/share/applications"
LOCALE_DIR="$HOME/.local/share/locale"

mkdir -p "$BIN_DIR"
mkdir -p "$APP_DIR"
mkdir -p "$LOCALE_DIR"

# Copy python script
cp "${APP_NAME}.py" "$BIN_DIR/${APP_NAME}"
chmod +x "$BIN_DIR/${APP_NAME}"

# Copy translations
if [ -d "locale" ]; then
    cp -r locale/* "$LOCALE_DIR/"
fi

# Create desktop shortcut
cat << DESKTOP > "$APP_DIR/${APP_NAME}.desktop"
[Desktop Entry]
Name=Başlangıç Uygulamaları Yöneticisi
Name[en]=Startup Applications Manager
Name[bg]=Мениджър на стартиращи приложения
Name[ru]=Менеджер автозапуска приложений
Comment=Sistem ve Kullanıcı uygulamalarını yönetin
Comment[en]=Manage system and user applications
Exec=$BIN_DIR/${APP_NAME}
Icon=system-run
Terminal=false
Type=Application
Categories=Settings;System;Utility;
Keywords=startup;autostart;manager;
StartupWMClass=baslangic-yoneticisi
DESKTOP

chmod +x "$APP_DIR/${APP_NAME}.desktop"
update-desktop-database "$APP_DIR" 2>/dev/null || true

echo "Kurulum tamamlandi! (Installation complete!)"
echo "Uygulama menusunde 'Baslangic Uygulamalari Yoneticisi' olarak bulabilirsiniz."
