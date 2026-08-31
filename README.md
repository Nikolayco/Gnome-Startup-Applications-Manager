<p align="center">
  <img src="https://raw.githubusercontent.com/Nikolayco/Gnome-Startup-Applications-Manager/main/icon.png" width="128" alt="Gnome Startup Applications Manager">
</p>
<h1 align="center">Gnome Startup Applications Manager</h1>

## 🇹🇷 Türkçe

**Gnome Başlangıç Uygulamaları Yöneticisi**, GNOME ve GTK tabanlı masaüstü ortamlarında başlangıç uygulamalarını ve scriptlerini yönetmek, eklemek, düzenlemek, anında test etmek ve canlı olarak takip etmek için geliştirilmiş modern bir GTK3 aracıdır.

### Özellikler
- **Canlı Durum Takibi**: Uygulamaların arka planda çalışıp çalışmadığını (🟢 Çalışıyor / ⚪ Durdu) saniyesi saniyesine canlı olarak gösterir.
- **Başlat ve Durdur Butonları**: Herhangi bir uygulamayı arayüzden çıkmadan anında başlatabilir (Test edebilir) veya çalışan bir uygulamayı doğrudan durdurabilirsiniz.
- **Akıllı Tray (Sistem Çekmecesi)**: İsterseniz uygulamayı tamamen gizleyip sağ alttaki sistem çekmecesine gönderebilir ve oradan uygulamalarınıza "Hızlı Başlat" menüsüyle anında erişebilirsiniz.
- **Kategorize Edilmiş ve Bölünmüş Listeler**: Kullanıcı (User) ve Sistem (System) uygulamalarını birbirinden ayırır. Birbirinden bağımsız kaydırılabilir listeler sayesinde ekran boyutunuz ne olursa olsun rahatça kullanılır.
- **Terminal Modu ve Kusursuz Küçültme (Minimize)**: Scriptlerinizi (.sh veya .py) terminalde çalıştırabilir, isterseniz başlar başlamaz tamamen simge durumuna küçültebilirsiniz (Minimize).
- **Çoklu Dil Desteği (i18n)**: Sistem dilinize göre otomatik olarak Türkçe, İngilizce, Rusça veya Bulgarca dillerine adapte olur.

### Kurulum (Install)
Uygulamayı sisteme menü kısayolu ile kalıcı olarak kurmak için terminalden şu komutları çalıştırmanız yeterlidir:
```bash
git clone https://github.com/Nikolayco/Gnome-Startup-Applications-Manager.git
cd Gnome-Startup-Applications-Manager
./install.sh
```

### Kaldırma (Uninstall)
Sistemden tamamen silmek (kaldırmak) için:
```bash
cd ~/Belgeler/GitHub/Gnome-Startup-Applications-Manager
./uninstall.sh
```

---

## 🇬🇧 English

**Gnome Startup Applications Manager** is a modern, user-friendly GTK3 tool designed to manage, add, edit, test, and live-track autostart applications and scripts in GNOME or other GTK-based desktop environments.

### Features
- **Live Status Tracking**: Instantly tracks and displays whether your applications are currently running in the background (🟢 Running / ⚪ Stopped).
- **Start and Stop Buttons**: Test any application instantly, or kill a running application directly from the manager.
- **Smart System Tray (Quick Launcher)**: Minimize the manager directly to the system tray and use the right-click menu as a "Quick Launcher" for your scripts.
- **Categorized & Paned Lists**: Visually separates User Apps from System Apps with independently scrollable, adjustable panes.
- **Terminal Mode & Perfect Minimize**: Run scripts (.sh / .py) in the background, foreground, or launch them in a perfectly minimized terminal window.
- **Multi-Language Support (i18n)**: Automatically adapts to English, Turkish, Russian, and Bulgarian based on your system language.

### Installation
```bash
git clone https://github.com/Nikolayco/Gnome-Startup-Applications-Manager.git
cd Gnome-Startup-Applications-Manager
./install.sh
```

### Uninstallation
```bash
cd ~/Belgeler/GitHub/Gnome-Startup-Applications-Manager
./uninstall.sh
```

---

## 🇧🇬 Български

**Мениджър на стартиращи приложения за Gnome** е модерен и удобен GTK3 инструмент за управление, добавяне, редактиране, тестване и проследяване на състоянието на автоматично стартиращи приложения и скриптове в GNOME.

### Характеристики
- **Проследяване на състоянието на живо**: Незабавно проследява и показва дали приложенията ви работят във фонов режим (🟢 Работи / ⚪ Спряно).
- **Бутони за стартиране и спиране**: Тествайте всяко приложение незабавно или спрете работещо приложение директно от мениджъра.
- **Умна системна лента (Tray)**: Минимизирайте мениджъра в системната лента и използвайте менюто като "Бързо стартиране" за вашите скриптове.
- **Категоризирани и разделени списъци**: Разделя потребителските и системните приложения с независимо превъртащи се панели.
- **Терминален режим и минимизиране**: Изпълнявайте скриптове в терминален прозорец или автоматично ги минимизирайте.
- **Многоезична поддръжка**: Автоматично се адаптира към български, английски, руски и турски език.

### Инсталация
```bash
git clone https://github.com/Nikolayco/Gnome-Startup-Applications-Manager.git
cd Gnome-Startup-Applications-Manager
./install.sh
```

### Деинсталиране
```bash
cd ~/Belgeler/GitHub/Gnome-Startup-Applications-Manager
./uninstall.sh
```

---

## 🇷🇺 Русский

**Менеджер автозапуска приложений Gnome** — это современный GTK3 инструмент для управления, редактирования, мгновенного тестирования и отслеживания статуса автозагружаемых приложений и скриптов в GNOME.

### Особенности
- **Отслеживание статуса в реальном времени**: Показывает, работает ли приложение в данный момент (🟢 Работает / ⚪ Остановлено).
- **Кнопки запуска и остановки**: Запускайте приложения для тестирования или останавливайте зависшие процессы прямо из интерфейса.
- **Умный системный трей (Tray)**: Сверните приложение в трей и используйте меню как инструмент быстрого запуска скриптов.
- **Раздельные списки (Paned)**: Независимая прокрутка для пользовательских и системных приложений.
- **Режим терминала и автоматическое сворачивание**: Запускайте скрипты в окне терминала с возможностью автоматического сворачивания при старте.
- **Многоязычная поддержка**: Поддержка русского, английского, болгарского и турецкого языков.

### Установка
```bash
git clone https://github.com/Nikolayco/Gnome-Startup-Applications-Manager.git
cd Gnome-Startup-Applications-Manager
./install.sh
```

### Удаление
```bash
cd ~/Belgeler/GitHub/Gnome-Startup-Applications-Manager
./uninstall.sh
```
