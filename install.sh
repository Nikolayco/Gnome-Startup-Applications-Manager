#!/usr/bin/env bash

mkdir -p ~/.local/bin ~/.local/share/applications

echo "Kodlar ~/.local/bin klasörüne kopyalanıyor..."
cp baslangic-yoneticisi.py ~/.local/bin/baslangic-yoneticisi
chmod +x ~/.local/bin/baslangic-yoneticisi

echo "Masaüstü kısayolu oluşturuluyor..."
cat << DESKTOP > ~/.local/share/applications/baslangic-yoneticisi.desktop
[Desktop Entry]
Name=Başlangıç Uygulamaları Yöneticisi
Comment=Sistem başlangıcındaki uygulamaları yönetin ve test edin
Exec=$HOME/.local/bin/baslangic-yoneticisi
Icon=preferences-system
Terminal=false
Type=Application
Categories=Settings;System;
DESKTOP

update-desktop-database ~/.local/share/applications 2>/dev/null || true

echo "---------------------------------------------------"
echo "Kurulum başarıyla tamamlandı!"
echo "Uygulama menüsünde 'Başlangıç Uygulamaları Yöneticisi' olarak aratabilirsiniz."
