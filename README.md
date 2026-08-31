# Gnome Startup Applications Manager

<div align="center">
  <h3>
    <a href="#-türkçe">🇹🇷 Türkçe</a> |
    <a href="#-english">🇬🇧 English</a> |
    <a href="#-български">🇧🇬 Български</a> |
    <a href="#-русский">🇷🇺 Русский</a>
  </h3>
</div>

---

## 🇹🇷 Türkçe

**Gnome Başlangıç Uygulamaları Yöneticisi**, GNOME masaüstü ortamında (veya diğer GTK tabanlı ortamlarda) sistem açılışında başlayan uygulama ve scriptleri yönetmek, eklemek, düzenlemek ve anında test etmek için geliştirilmiş modern ve kullanıcı dostu bir araçtır.

### Özellikler
- **Kullanıcı Dostu Arayüz**: Modern GNOME (HeaderBar) tasarım standartlarına uygundur.
- **Kategorize Edilmiş Listeler**: Kullanıcıya özel (User) uygulamalar ile sistem (System) servislerini iki ayrı listede düzenli bir şekilde ayırır.
- **Terminal Modu Desteği**: Eklenen `.sh` veya `.py` scriptlerini otomatik algılar ve arka planda veya ön planda (Terminal penceresinde) çalıştırma seçeneği sunar.
- **Anında Test (Başlat)**: Eklenen bir uygulamanın doğru çalışıp çalışmadığı tek bir tıkla anında test edilebilir.
- **Akıllı İsimlendirme**: Gözat menüsü ile dosya seçildiğinde, uygulamanın ismini dosya adına göre otomatik olarak doldurur.
- **Hızlı Düzenleme**: Listeden herhangi bir uygulamanın üzerine çift tıklayarak ayarları anında değiştirilebilir.

### Kurulum (Install)
Uygulamayı sisteme menü kısayolu ile kalıcı olarak kurmak için terminalden şu komutları çalıştırmanız yeterlidir:
```bash
git clone https://github.com/Nikolayco/Gnome-Startup-Applications-Manager.git
cd Gnome-Startup-Applications-Manager
./install.sh
```
Kurulum tamamlandıktan sonra uygulama menüsünde **Başlangıç Uygulamaları Yöneticisi** olarak aratarak erişebilirsiniz.

### Kaldırma (Uninstall)
Uygulama resmi mağaza paketleri (Apt/Flatpak) yerine harici bir betik olarak kurulduğundan, GNOME uygulama menüsündeki "Kaldır" butonuna basmak işe yaramayacaktır. Sistemden tamamen silmek (kaldırmak) için:
```bash
cd Gnome-Startup-Applications-Manager
./uninstall.sh
```

---

## 🇬🇧 English

**Gnome Startup Applications Manager** is a modern, user-friendly GTK3 tool designed to manage, add, edit, and instantly test autostart applications and scripts in GNOME or other GTK-based desktop environments.

### Features
- **User-Friendly Interface**: Designed following modern GNOME HeaderBar UI guidelines.
- **Categorized Lists**: Visually separates user-specific custom scripts (User Apps) from default background services (System Apps).
- **Foreground/Background Execution**: Automatically detects `.sh` or `.py` files and offers a checkbox to run them visibly in a Terminal window or hidden in the background.
- **Instant Test**: Run the selected application immediately with a single click to verify its functionality.
- **Smart Auto-fill**: Automatically generates application names based on the selected executable file.
- **Double-click Editing**: Quickly edit properties by double-clicking on any row in the lists.

### Installation
To install the application permanently into the system's app menu, run the following commands in the terminal:
```bash
git clone https://github.com/Nikolayco/Gnome-Startup-Applications-Manager.git
cd Gnome-Startup-Applications-Manager
./install.sh
```
Once installed, it can be found in the application launcher.

### Uninstallation
Because this app is installed via a custom script rather than a package manager (Apt/Flatpak), the "Uninstall" button in the GNOME app grid will not work. To completely remove it from the system:
```bash
cd Gnome-Startup-Applications-Manager
./uninstall.sh
```

---

## 🇧🇬 Български

**Мениджър на стартиращи приложения за Gnome** е модерен и удобен GTK3 инструмент за управление, добавяне, редактиране и мигновено тестване на автоматично стартиращи приложения и скриптове в GNOME и други GTK базирани графични среди.

### Характеристики
- **Удобен интерфейс**: Дизайн, следващ съвременните стандарти на GNOME (HeaderBar).
- **Категоризирани списъци**: Визуално разделя потребителските скриптове (Потребителски) от системните услуги (Системни).
- **Изпълнение в терминал**: Автоматично разпознава `.sh` или `.py` файлове и предлага опция за стартирането им във видим терминален прозорец или скрито във фонов режим.
- **Мигновен тест**: Стартирайте избраното приложение веднага с един клик, за да проверите функционалността му.
- **Автоматично попълване**: Генерира имена на приложения въз основа на избрания файл.
- **Бързо редактиране**: Редактирайте свойствата бързо чрез двойно кликване върху който и да е ред.

### Инсталация
За да инсталирате приложението за постоянно в менюто на системата, изпълнете следните команди в терминала:
```bash
git clone https://github.com/Nikolayco/Gnome-Startup-Applications-Manager.git
cd Gnome-Startup-Applications-Manager
./install.sh
```

### Деинсталиране
Тъй като приложението е инсталирано чрез персонализиран скрипт, бутонът "Деинсталиране" (Uninstall) в менюто на GNOME няма да работи. За да го премахнете напълно от системата:
```bash
cd Gnome-Startup-Applications-Manager
./uninstall.sh
```

---

## 🇷🇺 Русский

**Менеджер автозапуска приложений Gnome** — это современный и удобный GTK3 инструмент для управления, добавления, редактирования и мгновенного тестирования автозагружаемых приложений и скриптов в среде GNOME.

### Особенности
- **Удобный интерфейс**: Разработан в соответствии с современными стандартами дизайна GNOME (HeaderBar).
- **Раздельные списки**: Визуально отделяет пользовательские скрипты от системных служб.
- **Запуск в терминале**: Автоматически обнаруживает файлы `.sh` или `.py` и предлагает опцию их запуска в окне терминала или скрыто в фоновом режиме.
- **Мгновенный тест**: Проверка работы выбранного приложения или скрипта одним кликом.
- **Автозаполнение**: Автоматическое создание названий приложений на основе выбранного файла.
- **Быстрое редактирование**: Двойной клик по строке для мгновенного изменения свойств.

### Установка
Для постоянной установки приложения в системное меню выполните следующие команды в терминале:
```bash
git clone https://github.com/Nikolayco/Gnome-Startup-Applications-Manager.git
cd Gnome-Startup-Applications-Manager
./install.sh
```

### Удаление
Поскольку приложение устанавливается с помощью пользовательского скрипта, кнопка «Удалить» (Uninstall) в меню GNOME работать не будет. Чтобы полностью удалить его из системы:
```bash
cd Gnome-Startup-Applications-Manager
./uninstall.sh
```
