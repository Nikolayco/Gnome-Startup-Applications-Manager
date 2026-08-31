# Gnome Startup Applications Manager

GNOME masaüstü ortamında (veya diğer GTK tabanlı ortamlarda) başlangıçta çalışan uygulama ve scriptlerinizi yönetmek, eklemek, düzenlemek ve **anında başlatarak test etmek** için geliştirilmiş özel bir yöneticidir.

## Özellikler
- **Kullanıcı Dostu Arayüz (HeaderBar)**: Modern GNOME standartlarına uygun tasarım.
- **Ekleme & Düzenleme**: Sistem veya kişisel scriptlerinizi başlangıca ekleyin. "Gözat" (Klasör) butonu ile bilgisayarınızdan dosyaları kolayca seçin.
- **Çift Tıklama**: Listedeki uygulamalara çift tıklayarak hızlıca düzenleyebilirsiniz.
- **Anında Başlatma (Test)**: Cinnamon'daki gibi, eklediğiniz uygulamayı tek tıklamayla anında çalıştırabilirsiniz.
- **Güvenli Silme**: Sistem (root) dosyalarına dokunmadan, kullanıcı seviyesinde dosyaları devre dışı bırakır.
- **İkon Desteği**: Uygulamaların sistem ikonları listede şık bir biçimde gösterilir.

## Gereksinimler
- Python 3
- GTK 3 (python3-gi)

## Kurulum (Install)
Uygulamayı sisteminize menü kısayolu ile kalıcı olarak kurmak için terminalden kurulum scriptini çalıştırmanız yeterlidir:
```bash
git clone https://github.com/Nikolayco/Gnome-Startup-Applications-Manager.git
cd Gnome-Startup-Applications-Manager
./install.sh
```
Bu adımdan sonra menüde **Başlangıç Uygulamaları Yöneticisi** olarak aratarak uygulamaya erişebilirsiniz.

## Kaldırma (Uninstall)
Uygulama harici bir script olarak kurulduğundan, GNOME uygulama menüsündeki "Kaldır" butonuna basmak işe yaramayacaktır. Sistemden tamamen silmek için projenin bulunduğu klasörde kaldırma scriptini çalıştırmanız yeterlidir:
```bash
cd Gnome-Startup-Applications-Manager
./uninstall.sh
```
