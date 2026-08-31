#!/usr/bin/env python3
import os
import glob
import shlex
import subprocess
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gio, GdkPixbuf, Gdk

_EN_DICT = {
    "-": "-",
    "-- Hızlı Başlat --": "-- Quick Launch --",
    "<b>Başlangıç Uygulamaları Yöneticisi</b>": "<b>Startup Applications Manager</b>",
    "<b>Gelişmiş Arka Plan İzni (Lingering)</b>": "<b>Advanced Background Permission (Lingering)</b>",
    "Aktif": "Enabled",
    "Ayarlar": "Settings",
    "Ayarları düzenle": "Edit settings",
    "Açıklama (İsteğe):": "Description (Optional):",
    "Başlangıç": "Startup",
    "Başlangıç Uygulamaları Yöneticisi": "Startup Applications Manager",
    "Belirli Aralıklarla (Tekrarla)": "Interval (Repeat)",
    "Belirli Gün/Saat (Takvim)": "Specific Day/Time (Calendar)",
    "Bilgisayar açıldığında, siz henüz şifre girip oturum açmasanız bile\nzamanlanmış görevlerin (Sistem Açılışında - Boot) çalışabilmesi için gereklidir.": "Required for scheduled tasks (Boot) to run\nin the background before you even log in.",
    "Bu öğeyi silmek istediğinize emin misiniz?": "Are you sure you want to delete this item?",
    "Dakika": "Minutes",
    "Dosya Seç": "Select File",
    "Durum": "Status",
    "Durum Tarama Sıklığı (Saniye):": "Status Refresh Rate (Seconds):",
    "Düzenle": "Edit",
    "Evet (Max)": "Yes (Max)",
    "Evet (Min)": "Yes (Min)",
    "Evet (Normal)": "Yes (Normal)",
    "Gecikme": "Delay",
    "Gecikme (Sn):": "Delay (Sec):",
    "Gecikme:": "Delay:",
    "Görev": "Task",
    "Görev Adı:": "Task Name:",
    "Görevi Düzenle": "Edit Task",
    "Gün": "Days",
    "Hakkında": "About",
    "Kalıcı olarak sil": "Delete permanently",
    "Kaydet": "Save",
    "Kaynak": "Resources",
    "Komut": "Command",
    "Komut / Dosya:": "Command / File:",
    "Kullanıcı Uygulamaları": "User Applications",
    "Kısaca açıklama yazın...": "Write a short description...",
    "Mevcut Dosya / Komut Seç": "Select Existing File / Command",
    "Mini Editör (Kodu Buraya Yaz)": "Mini Editor (Write Code Here)",
    "Oturum Açılışında (Login)": "At Login (Startup)",
    "Pencere Boyutu ve Pozisyonu:": "Window Size and Position:",
    "Pencere Modu:": "Window Mode:",
    "Saat": "Hours",
    "Saniye": "Seconds",
    "Seç": "Select",
    "Seçili görevleri silmek istiyor musunuz?": "Are you sure you want to delete the selected tasks?",
    "Sil": "Delete",
    "Sistem Açılışında (Boot)": "At System Boot",
    "Sistem Uygulamaları": "System Applications",
    "Sistem Uygulamalarını (Alt Liste) Göster:": "Show System Applications (Sublist):",
    "Sistem açıldıktan kaç saniye sonra çalışsın?": "How many seconds after boot should it run?",
    "Sistem ve Kullanıcı uygulamalarını yönetin": "Manage system and user startup applications",
    "Sistem Çekmecesinde (Tray) Her Zaman Göster:": "Always Show in System Tray:",
    "Sisteminizde systemd bulunamadığı için zamanlayıcı kullanılamıyor.": "Task Scheduler is unavailable because systemd is not found on your system.",
    "Sürüm: 1.1\nGeliştirici: Nikolayco": "Version: 1.1\nDeveloper: Nikolayco",
    "Sıradaki Çalışma": "Next Run",
    "Terminal": "Terminal",
    "Terminalde Çalıştır:": "Run in Terminal:",
    "Terminalde çalıştır": "Run in terminal",
    "Tetikleyici": "Trigger",
    "Tetikleyici:": "Trigger:",
    "Tüm Dosyalar": "All Files",
    "Uygulama Adı": "App Name",
    "Uygulama Adı:": "App Name:",
    "Uygulama Ara...": "Search app...",
    "Uygulama bulunamadı": "No application found",
    "Uygulamayı arka plana (Tray) gizle": "Hide application to Tray",
    "Uygulamayı hemen çalıştırarak test et": "Run application immediately to test",
    "Varsayılan Boyuta Dön": "Restore Default Size",
    "Yeni Başlangıç Öğesi Ekle": "Add New Startup Item",
    "Yeni Görev": "New Task",
    "Yeni uygulama veya script ekle": "Add new app or script",
    "Zamanlayıcı": "Task Scheduler",
    "Çalışacak Dosya/Kod:": "File/Code to Run:",
    "Çalışan uygulamayı durdur (Kapat)": "Stop running application (Kill)",
    "Çalıştırma Hatası!": "Execution Error!",
    "Çalıştırılacak Dosyayı Seçin": "Select File to Run",
    "Örn: Otomatik Yedekleme": "e.g. Auto Backup",
    "Örn: Yedekleme": "e.g. Backup",
    "Öğeyi Düzenle": "Edit Item",
    "İptal": "Cancel",
    "İzin Ver (Lingering'i Aç)": "Enable (Turn on Lingering)",
    "İzin Ver / Kaldır": "Enable / Disable",
    "İzin Verildi (Aktif)": "Enabled (Active)",
    "Şimdi Çalıştır": "Run Now",
    "⚙️ Yöneticiyi Aç": "⚙️ Open Manager",
    "❌ Çıkış Yap": "❌ Quit",
    "Klavye Kısayolları": "Keyboard Shortcuts",
    "Kısayol": "Shortcut",
    "İşlev": "Function",
    "Yeni başlangıç uygulaması ekle": "Add a new startup application",
    "Seçili uygulamayı düzenle": "Edit selected application",
    "Seçili uygulamayı başlat": "Start selected application",
    "Seçili uygulamayı durdur (öldür)": "Stop (kill) selected application",
    "Seçili uygulamayı sil": "Delete selected application",
    "Arama kutusuna odaklan": "Focus the search box",
    "Çalışıyor": "Running",
    "Durdu": "Stopped"
}

_RU_DICT = {
    "-": "-",
    "-- Hızlı Başlat --": "-- Быстрый запуск --",
    "<b>Başlangıç Uygulamaları Yöneticisi</b>": "<b>Менеджер автозапуска</b>",
    "<b>Gelişmiş Arka Plan İzni (Lingering)</b>": "<b>Расширенное фоновое разрешение (Lingering)</b>",
    "Aktif": "Активен",
    "Ayarlar": "Настройки",
    "Ayarları düzenle": "Изменить настройки",
    "Açıklama (İsteğe):": "Описание (необяз.):",
    "Başlangıç": "Автозапуск",
    "Başlangıç Uygulamaları Yöneticisi": "Менеджер автозапуска",
    "Belirli Aralıklarla (Tekrarla)": "С интервалом (повтор)",
    "Belirli Gün/Saat (Takvim)": "По расписанию (календарь)",
    "Bilgisayar açıldığında, siz henüz şifre girip oturum açmasanız bile\nzamanlanmış görevlerin (Sistem Açılışında - Boot) çalışabilmesi için gereklidir.": "Требуется для запуска задач при загрузке системы,\nдаже если вы ещё не вошли в систему.",
    "Bu öğeyi silmek istediğinize emin misiniz?": "Вы уверены, что хотите удалить этот элемент?",
    "Dakika": "Минуты",
    "Dosya Seç": "Выбрать файл",
    "Durum": "Статус",
    "Durum Tarama Sıklığı (Saniye):": "Частота обновления (сек):",
    "Düzenle": "Изменить",
    "Evet (Max)": "Да (Макс)",
    "Evet (Min)": "Да (Мин)",
    "Evet (Normal)": "Да (Норм)",
    "Gecikme": "Задержка",
    "Gecikme (Sn):": "Задержка (сек):",
    "Gecikme:": "Задержка:",
    "Görev": "Задача",
    "Görev Adı:": "Название задачи:",
    "Görevi Düzenle": "Изменить задачу",
    "Gün": "Дни",
    "Hakkında": "О программе",
    "Kalıcı olarak sil": "Удалить навсегда",
    "Kaydet": "Сохранить",
    "Kaynak": "Ресурсы",
    "Komut": "Команда",
    "Komut / Dosya:": "Команда / Файл:",
    "Kullanıcı Uygulamaları": "Приложения пользователя",
    "Kısaca açıklama yazın...": "Краткое описание...",
    "Mevcut Dosya / Komut Seç": "Выбрать файл / команду",
    "Mini Editör (Kodu Buraya Yaz)": "Мини-редактор (вставьте код)",
    "Oturum Açılışında (Login)": "При входе в систему",
    "Pencere Boyutu ve Pozisyonu:": "Размер и положение окна:",
    "Pencere Modu:": "Режим окна:",
    "Saat": "Часы",
    "Saniye": "Секунды",
    "Seç": "Выбрать",
    "Seçili görevleri silmek istiyor musunuz?": "Удалить выбранные задачи?",
    "Sil": "Удалить",
    "Sistem Açılışında (Boot)": "При загрузке системы",
    "Sistem Uygulamaları": "Системные приложения",
    "Sistem Uygulamalarını (Alt Liste) Göster:": "Показывать системные приложения:",
    "Sistem açıldıktan kaç saniye sonra çalışsın?": "Через сколько секунд после загрузки запустить?",
    "Sistem ve Kullanıcı uygulamalarını yönetin": "Управление приложениями автозапуска",
    "Sistem Çekmecesinde (Tray) Her Zaman Göster:": "Всегда показывать в трее:",
    "Sisteminizde systemd bulunamadığı için zamanlayıcı kullanılamıyor.": "Планировщик недоступен: systemd не найден в системе.",
    "Sürüm: 1.1\nGeliştirici: Nikolayco": "Версия: 1.1\nРазработчик: Nikolayco",
    "Sıradaki Çalışma": "Следующий запуск",
    "Terminal": "Терминал",
    "Terminalde Çalıştır:": "Запустить в терминале:",
    "Terminalde çalıştır": "Запустить в терминале",
    "Tetikleyici": "Триггер",
    "Tetikleyici:": "Триггер:",
    "Tüm Dosyalar": "Все файлы",
    "Uygulama Adı": "Имя приложения",
    "Uygulama Adı:": "Имя приложения:",
    "Uygulama Ara...": "Поиск приложения...",
    "Uygulama bulunamadı": "Приложение не найдено",
    "Uygulamayı arka plana (Tray) gizle": "Свернуть в трей",
    "Uygulamayı hemen çalıştırarak test et": "Запустить немедленно для тестирования",
    "Varsayılan Boyuta Dön": "Восстановить размер по умолчанию",
    "Yeni Başlangıç Öğesi Ekle": "Добавить элемент автозапуска",
    "Yeni Görev": "Новая задача",
    "Yeni uygulama veya script ekle": "Добавить приложение или скрипт",
    "Zamanlayıcı": "Планировщик",
    "Çalışacak Dosya/Kod:": "Файл/код для запуска:",
    "Çalışan uygulamayı durdur (Kapat)": "Остановить приложение (завершить)",
    "Çalıştırma Hatası!": "Ошибка запуска!",
    "Çalıştırılacak Dosyayı Seçin": "Выберите файл для запуска",
    "Örn: Otomatik Yedekleme": "Напр: Автоматическое резервное копирование",
    "Örn: Yedekleme": "Напр: Резервная копия",
    "Öğeyi Düzenle": "Изменить элемент",
    "İptal": "Отмена",
    "İzin Ver (Lingering'i Aç)": "Разрешить (включить Lingering)",
    "İzin Ver / Kaldır": "Включить / Отключить",
    "İzin Verildi (Aktif)": "Разрешено (Активно)",
    "Şimdi Çalıştır": "Запустить сейчас",
    "⚙️ Yöneticiyi Aç": "⚙️ Открыть менеджер",
    "❌ Çıkış Yap": "❌ Выйти",
    "Klavye Kısayolları": "Горячие клавиши",
    "Kısayol": "Сочетание",
    "İşlev": "Функция",
    "Yeni başlangıç uygulaması ekle": "Добавить новое приложение автозапуска",
    "Seçili uygulamayı düzenle": "Изменить выбранное приложение",
    "Seçili uygulamayı başlat": "Запустить выбранное приложение",
    "Seçili uygulamayı durdur (öldür)": "Остановить выбранное приложение",
    "Seçili uygulamayı sil": "Удалить выбранное приложение",
    "Arama kutusuna odaklan": "Перейти в поле поиска",
    "Çalışıyor": "Работает",
    "Durdu": "Остановлено"
}

_BG_DICT = {
    "-": "-",
    "-- Hızlı Başlat --": "-- Бърз старт --",
    "<b>Başlangıç Uygulamaları Yöneticisi</b>": "<b>Мениджър за автостартиране</b>",
    "<b>Gelişmiş Arka Plan İzni (Lingering)</b>": "<b>Разширено фоново разрешение (Lingering)</b>",
    "Aktif": "Активен",
    "Ayarlar": "Настройки",
    "Ayarları düzenle": "Редактирай настройките",
    "Açıklama (İsteğe):": "Описание (незадълж.):",
    "Başlangıç": "Автостартиране",
    "Başlangıç Uygulamaları Yöneticisi": "Мениджър за автостартиране",
    "Belirli Aralıklarla (Tekrarla)": "На интервали (повтаряй)",
    "Belirli Gün/Saat (Takvim)": "По разписание (календар)",
    "Bilgisayar açıldığında, siz henüz şifre girip oturum açmasanız bile\nzamanlanmış görevlerin (Sistem Açılışında - Boot) çalışabilmesi için gereklidir.": "Необходимо за изпълнение на задачи при стартиране,\nдори ако все още не сте влезли в системата.",
    "Bu öğeyi silmek istediğinize emin misiniz?": "Сигурни ли сте, че искате да изтриете този елемент?",
    "Dakika": "Минути",
    "Dosya Seç": "Избери файл",
    "Durum": "Статус",
    "Durum Tarama Sıklığı (Saniye):": "Честота на обновяване (сек):",
    "Düzenle": "Редактирай",
    "Evet (Max)": "Да (Макс)",
    "Evet (Min)": "Да (Мин)",
    "Evet (Normal)": "Да (Норм)",
    "Gecikme": "Закъснение",
    "Gecikme (Sn):": "Закъснение (сек):",
    "Gecikme:": "Закъснение:",
    "Görev": "Задача",
    "Görev Adı:": "Име на задачата:",
    "Görevi Düzenle": "Редактирай задачата",
    "Gün": "Дни",
    "Hakkında": "За програмата",
    "Kalıcı olarak sil": "Изтрий завинаги",
    "Kaydet": "Запази",
    "Kaynak": "Ресурси",
    "Komut": "Команда",
    "Komut / Dosya:": "Команда / Файл:",
    "Kullanıcı Uygulamaları": "Потребителски приложения",
    "Kısaca açıklama yazın...": "Кратко описание...",
    "Mevcut Dosya / Komut Seç": "Избери файл / команда",
    "Mini Editör (Kodu Buraya Yaz)": "Мини редактор (вмъкни код)",
    "Oturum Açılışında (Login)": "При вход в системата",
    "Pencere Boyutu ve Pozisyonu:": "Размер и позиция на прозореца:",
    "Pencere Modu:": "Режим на прозореца:",
    "Saat": "Часове",
    "Saniye": "Секунди",
    "Seç": "Избери",
    "Seçili görevleri silmek istiyor musunuz?": "Да изтриете ли избраните задачи?",
    "Sil": "Изтрий",
    "Sistem Açılışında (Boot)": "При стартиране на системата",
    "Sistem Uygulamaları": "Системни приложения",
    "Sistem Uygulamalarını (Alt Liste) Göster:": "Покажи системни приложения:",
    "Sistem açıldıktan kaç saniye sonra çalışsın?": "Колко секунди след стартиране да се изпълни?",
    "Sistem ve Kullanıcı uygulamalarını yönetin": "Управление на приложения за автостартиране",
    "Sistem Çekmecesinde (Tray) Her Zaman Göster:": "Винаги показвай в системния трей:",
    "Sisteminizde systemd bulunamadığı için zamanlayıcı kullanılamıyor.": "Планировщикът е недостъпен: systemd не е намерен в системата.",
    "Sürüm: 1.1\nGeliştirici: Nikolayco": "Версия: 1.1\nРазработчик: Nikolayco",
    "Sıradaki Çalışma": "Следващо изпълнение",
    "Terminal": "Терминал",
    "Terminalde Çalıştır:": "Изпълни в терминал:",
    "Terminalde çalıştır": "Изпълни в терминал",
    "Tetikleyici": "Тригер",
    "Tetikleyici:": "Тригер:",
    "Tüm Dosyalar": "Всички файлове",
    "Uygulama Adı": "Ime на приложението",
    "Uygulama Adı:": "Ime на приложението:",
    "Uygulama Ara...": "Търси приложение...",
    "Uygulama bulunamadı": "Приложението не е намерено",
    "Uygulamayı arka plana (Tray) gizle": "Скрий в системния трей",
    "Uygulamayı hemen çalıştırarak test et": "Стартирай незабавно за тест",
    "Varsayılan Boyuta Dön": "Възстанови размера по подразбиране",
    "Yeni Başlangıç Öğesi Ekle": "Добави елемент за автостартиране",
    "Yeni Görev": "Нова задача",
    "Yeni uygulama veya script ekle": "Добави приложение или скрипт",
    "Zamanlayıcı": "Планировщик",
    "Çalışacak Dosya/Kod:": "Файл/код за изпълнение:",
    "Çalışan uygulamayı durdur (Kapat)": "Спри приложението (прекрати)",
    "Çalıştırma Hatası!": "Грешка при стартиране!",
    "Çalıştırılacak Dosyayı Seçin": "Избери файл за изпълнение",
    "Örn: Otomatik Yedekleme": "Напр: Автоматично архивиране",
    "Örn: Yedekleme": "Напр: Архив",
    "Öğeyi Düzenle": "Редактирай елемента",
    "İptal": "Отказ",
    "İzin Ver (Lingering'i Aç)": "Разреши (включи Lingering)",
    "İzin Ver / Kaldır": "Включи / Изключи",
    "İzin Verildi (Aktif)": "Разрешено (Активно)",
    "Şimdi Çalıştır": "Изпълни сега",
    "⚙️ Yöneticiyi Aç": "⚙️ Отвори мениджъра",
    "❌ Çıkış Yap": "❌ Изход",
    "Klavye Kısayolları": "Клавишни комбинации",
    "Kısayol": "Комбинация",
    "İşlev": "Функция",
    "Yeni başlangıç uygulaması ekle": "Добави ново приложение за автостартиране",
    "Seçili uygulamayı düzenle": "Редактирай избраното приложение",
    "Seçili uygulamayı başlat": "Стартирай избраното приложение",
    "Seçili uygulamayı durdur (öldür)": "Спри избраното приложение",
    "Seçili uygulamayı sil": "Изтрий избраното приложение",
    "Arama kutusuna odaklan": "Фокусирай полето за търсене",
    "Çalışıyor": "Работи",
    "Durdu": "Спряно"
}

_LANG = os.environ.get("LANG", "en").split("_")[0]

def _(text):
    if _LANG == "tr": return text
    if _LANG == "ru": return _RU_DICT.get(text, _EN_DICT.get(text, text))
    if _LANG == "bg": return _BG_DICT.get(text, _EN_DICT.get(text, text))
    return _EN_DICT.get(text, text)



try:
    gi.require_version('AyatanaAppIndicator3', '0.1')
    from gi.repository import AyatanaAppIndicator3 as AppIndicator3
except ValueError:
    try:
        gi.require_version('AppIndicator3', '0.1')
        from gi.repository import AppIndicator3
    except ValueError:
        AppIndicator3 = None

AUTOSTART_DIR = os.path.expanduser("~/.config/autostart")
SYS_AUTOSTART_DIR = "/etc/xdg/autostart"
CUSTOM_SCRIPTS_DIR = os.path.expanduser("~/.local/share/Gnome-Startup-Applications-Manager/scripts")
APP_ICON = "system-run"
SYSTEMD_USER_DIR = os.path.expanduser("~/.config/systemd/user")

class AutostartApp:
    def __init__(self, filename, name, cmd, comment, hidden, is_sys, path, icon, terminal, delay, term_size="normal"):
        self.filename = filename
        self.name = name
        self.cmd = cmd
        self.comment = comment
        self.hidden = hidden
        self.is_sys = is_sys
        self.path = path
        self.icon = icon
        self.terminal = terminal
        self.delay = delay
        self.enabled = not hidden
        self.term_size = term_size

class CmdTextView(Gtk.ScrolledWindow):
    def __init__(self):
        super().__init__()
        self.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.set_size_request(-1, 70)
        self.tv = Gtk.TextView()
        self.tv.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.tv.set_monospace(True)
        self.tv.set_hexpand(True)
        self.add(self.tv)
        self.show_all()
        
    def get_text(self):
        buf = self.tv.get_buffer()
        return buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True).strip()
        
    def set_text(self, text):
        self.tv.get_buffer().set_text(text)

class AppDialog(Gtk.Dialog):
    def __init__(self, parent, title, app=None):
        super().__init__(title=title, transient_for=parent, flags=Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT)
        self.set_default_size(580, 420)
        self.original_icon = app.icon if app else "application-x-executable"

        
        self.add_buttons(_("İptal"), Gtk.ResponseType.CANCEL, _("Kaydet"), Gtk.ResponseType.OK)
        save_btn = self.get_widget_for_response(Gtk.ResponseType.OK)
        save_btn.get_style_context().add_class("suggested-action")
        
        box = self.get_content_area()
        box.set_spacing(15)
        box.set_margin_top(20)
        box.set_margin_bottom(20)
        box.set_margin_start(20)
        box.set_margin_end(20)
        
        grid = Gtk.Grid()
        grid.set_row_spacing(15)
        grid.set_column_spacing(15)
        box.pack_start(grid, True, True, 0)
        
        lbl_name = Gtk.Label(label=_("Uygulama Adı:"), xalign=0)
        lbl_name.get_style_context().add_class("dim-label")
        grid.attach(lbl_name, 0, 0, 1, 1)
        self.entry_name = Gtk.Entry(placeholder_text=_("Örn: Yedekleme"))
        self.entry_name.set_hexpand(True)
        grid.attach(self.entry_name, 1, 0, 1, 1)
        
        lbl_comment = Gtk.Label(label=_("Açıklama (İsteğe):"), xalign=0)
        lbl_comment.get_style_context().add_class("dim-label")
        grid.attach(lbl_comment, 0, 1, 1, 1)
        self.entry_comment = Gtk.Entry(placeholder_text=_("Kısaca açıklama yazın..."))
        grid.attach(self.entry_comment, 1, 1, 1, 1)

        lbl_delay = Gtk.Label(label=_("Gecikme (Sn):"), xalign=0)
        lbl_delay.get_style_context().add_class("dim-label")
        grid.attach(lbl_delay, 0, 2, 1, 1)
        
        self.spin_delay = Gtk.SpinButton.new_with_range(0, 300, 1)
        self.spin_delay.set_tooltip_text(_("Sistem açıldıktan kaç saniye sonra çalışsın?"))
        grid.attach(self.spin_delay, 1, 2, 1, 1)

        lbl_term = Gtk.Label(label=_("Pencere Modu:"), xalign=0)
        lbl_term.get_style_context().add_class("dim-label")
        grid.attach(lbl_term, 0, 3, 1, 1)

        term_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        self.check_terminal = Gtk.CheckButton(label=_("Terminalde çalıştır"))
        term_box.pack_start(self.check_terminal, False, False, 0)
        
        self.combo_term_size = Gtk.ComboBoxText()
        self.combo_term_size.append("maximize", "Maximize")
        self.combo_term_size.append("normal", "Normal")
        self.combo_term_size.append("minimize", "Minimize")
        self.combo_term_size.set_active_id("normal")
        self.combo_term_size.set_sensitive(False)
        self.check_terminal.connect("toggled", lambda w: self.combo_term_size.set_sensitive(w.get_active()))
        
        term_box.pack_start(self.combo_term_size, False, False, 0)
        grid.attach(term_box, 1, 3, 1, 1)

        lbl_source = Gtk.Label(label=_("Çalışacak Dosya/Kod:"), xalign=0)
        lbl_source.get_style_context().add_class("dim-label")
        grid.attach(lbl_source, 0, 4, 1, 1)
        
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        
        file_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.entry_cmd = CmdTextView()
        file_box.pack_start(self.entry_cmd, True, True, 0)
        btn_browse = Gtk.Button()
        btn_browse.add(Gtk.Image.new_from_icon_name("folder-open-symbolic", Gtk.IconSize.BUTTON))
        btn_browse.connect("clicked", self.on_browse_clicked)
        file_box.pack_start(btn_browse, False, False, 0)
        
        self.text_buffer = Gtk.TextBuffer()
        self.text_view = Gtk.TextView(buffer=self.text_buffer)
        self.text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self.text_view.set_monospace(True)
        scroll_tv = Gtk.ScrolledWindow()
        scroll_tv.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll_tv.set_size_request(-1, 100)
        scroll_tv.add(self.text_view)
        
        self.stack.add_titled(file_box, "file", _("Mevcut Dosya / Komut Seç"))
        self.stack.add_titled(scroll_tv, "code", _("Mini Editör (Kodu Buraya Yaz)"))
        
        switcher = Gtk.StackSwitcher()
        switcher.set_stack(self.stack)
        switcher.set_halign(Gtk.Align.START)
        
        vbox_source = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        vbox_source.pack_start(switcher, False, False, 0)
        vbox_source.pack_start(self.stack, True, True, 0)
        
        grid.attach(vbox_source, 1, 4, 1, 1)

        if app:
            self.entry_name.set_text(app.name)
            self.entry_cmd.set_text(app.cmd)
            self.entry_comment.set_text(app.comment)
            self.check_terminal.set_active(app.terminal)
            self.combo_term_size.set_active_id(app.term_size)
            self.combo_term_size.set_sensitive(app.terminal)
            self.spin_delay.set_value(app.delay)
            
            if app.cmd.startswith(CUSTOM_SCRIPTS_DIR):
                self.stack.set_visible_child_name("code")
                try:
                    with open(app.cmd, 'r') as f:
                        lines = f.readlines()
                        if lines and lines[0].startswith("#!"):
                            content = "".join(lines[1:])
                        else:
                            content = "".join(lines)
                        self.text_buffer.set_text(content.strip())
                except: pass
            
        self.show_all()

    def on_browse_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(title=_("Çalıştırılacak Dosyayı Seçin"), parent=self, action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons(_("İptal"), Gtk.ResponseType.CANCEL, _("Seç"), Gtk.ResponseType.OK)
        filter_all = Gtk.FileFilter()
        filter_all.set_name(_("Tüm Dosyalar"))
        filter_all.add_pattern("*")
        dialog.add_filter(filter_all)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filepath = dialog.get_filename()
            self.entry_cmd.set_text(f'"{filepath}"' if " " in filepath else filepath)
            if not self.entry_name.get_text().strip():
                name_no_ext = os.path.splitext(os.path.basename(filepath))[0]
                self.entry_name.set_text(name_no_ext.replace("-", " ").replace("_", " ").title())
            if filepath.endswith(".sh") or filepath.endswith(".py"):
                self.check_terminal.set_active(True)
        dialog.destroy()

class ScheduleDialog(Gtk.Dialog):
    def __init__(self, parent, title, task=None):
        super().__init__(title=title, transient_for=parent, flags=Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT)
        self.set_default_size(600, 500)
        self.add_buttons(_("İptal"), Gtk.ResponseType.CANCEL, _("Kaydet"), Gtk.ResponseType.OK)
        self.get_widget_for_response(Gtk.ResponseType.OK).get_style_context().add_class("suggested-action")
        
        box = self.get_content_area()
        box.set_spacing(15)
        box.set_margin_top(20)
        box.set_margin_bottom(20)
        box.set_margin_start(20)
        box.set_margin_end(20)
        
        grid = Gtk.Grid()
        grid.set_row_spacing(15)
        grid.set_column_spacing(15)
        box.pack_start(grid, True, True, 0)
        
        # Name
        lbl_name = Gtk.Label(label=_("Görev Adı:"), xalign=0)
        grid.attach(lbl_name, 0, 0, 1, 1)
        self.entry_name = Gtk.Entry(placeholder_text=_("Örn: Otomatik Yedekleme"))
        self.entry_name.set_hexpand(True)
        grid.attach(self.entry_name, 1, 0, 1, 1)
        
        # Command
        lbl_cmd = Gtk.Label(label=_("Komut / Dosya:"), xalign=0)
        grid.attach(lbl_cmd, 0, 1, 1, 1)
        cmd_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.entry_cmd = CmdTextView()
        cmd_box.pack_start(self.entry_cmd, True, True, 0)
        btn_browse = Gtk.Button()
        btn_browse.add(Gtk.Image.new_from_icon_name("folder-open-symbolic", Gtk.IconSize.BUTTON))
        btn_browse.connect("clicked", self.on_browse)
        cmd_box.pack_start(btn_browse, False, False, 0)
        grid.attach(cmd_box, 1, 1, 1, 1)
        
        # Terminal Switch
        lbl_term = Gtk.Label(label=_("Terminalde Çalıştır:"), xalign=0)
        grid.attach(lbl_term, 0, 2, 1, 1)
        self.switch_term = Gtk.Switch()
        self.switch_term.set_halign(Gtk.Align.START)
        self.switch_term.set_valign(Gtk.Align.CENTER)
        grid.attach(self.switch_term, 1, 2, 1, 1)
        
        # Trigger Type
        lbl_type = Gtk.Label(label=_("Tetikleyici:"), xalign=0)
        grid.attach(lbl_type, 0, 3, 1, 1)
        self.combo_type = Gtk.ComboBoxText()
        self.combo_type.append("interval", _("Belirli Aralıklarla (Tekrarla)"))
        self.combo_type.append("calendar", _("Belirli Gün/Saat (Takvim)"))
        self.combo_type.append("boot", _("Sistem Açılışında (Boot)"))
        self.combo_type.append("login", _("Oturum Açılışında (Login)"))
        self.combo_type.set_active_id("interval")
        grid.attach(self.combo_type, 1, 3, 1, 1)
        
        # Trigger Settings Stack
        self.stack = Gtk.Stack()
        
        # Interval Box
        box_int = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.spin_int = Gtk.SpinButton.new_with_range(1, 1000, 1)
        self.combo_int_unit = Gtk.ComboBoxText()
        self.combo_int_unit.append("min", _("Dakika"))
        self.combo_int_unit.append("h", _("Saat"))
        self.combo_int_unit.append("d", _("Gün"))
        self.combo_int_unit.set_active_id("min")
        box_int.pack_start(self.spin_int, False, False, 0)
        box_int.pack_start(self.combo_int_unit, False, False, 0)
        self.stack.add_named(box_int, "interval")
        
        # Calendar Box
        box_cal = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.entry_cal = Gtk.Entry(placeholder_text="Örn: Mon,Wed *-*-* 09:00:00")
        box_cal.pack_start(self.entry_cal, True, True, 0)
        self.stack.add_named(box_cal, "calendar")
        
        # Boot Box
        box_boot = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        box_boot.pack_start(Gtk.Label(label=_("Gecikme:")), False, False, 0)
        self.spin_boot = Gtk.SpinButton.new_with_range(0, 3600, 1)
        box_boot.pack_start(self.spin_boot, False, False, 0)
        box_boot.pack_start(Gtk.Label(label=_("Saniye")), False, False, 0)
        self.stack.add_named(box_boot, "boot")
        
        # Login Box
        box_login = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        box_login.pack_start(Gtk.Label(label=_("Gecikme:")), False, False, 0)
        self.spin_login = Gtk.SpinButton.new_with_range(0, 3600, 1)
        box_login.pack_start(self.spin_login, False, False, 0)
        box_login.pack_start(Gtk.Label(label=_("Saniye")), False, False, 0)
        self.stack.add_named(box_login, "login")
        
        grid.attach(self.stack, 1, 4, 1, 1)
        
        self.combo_type.connect("changed", lambda c: self.stack.set_visible_child_name(c.get_active_id()))
        
        if task:
            self.entry_name.set_text(task['name'])
            cmd_text = task['cmd']
            if cmd_text.startswith("gnome-terminal -- "):
                cmd_text = cmd_text.replace("gnome-terminal -- ", "", 1)
                self.switch_term.set_active(True)
            self.entry_cmd.set_text(cmd_text)
            self.combo_type.set_active_id(task['type'])
            if task['type'] == 'interval':
                self.spin_int.set_value(task['val_int'])
                self.combo_int_unit.set_active_id(task['val_unit'])
            elif task['type'] == 'calendar':
                self.entry_cal.set_text(task['val_cal'])
            elif task['type'] == 'boot':
                self.spin_boot.set_value(task['val_delay'])
            elif task['type'] == 'login':
                self.spin_login.set_value(task['val_delay'])
                
        self.show_all()

    def on_browse(self, widget):
        dialog = Gtk.FileChooserDialog(title=_("Dosya Seç"), parent=self, action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        if dialog.run() == Gtk.ResponseType.OK:
            filepath = dialog.get_filename()
            self.entry_cmd.set_text(f'"{filepath}"' if " " in filepath else filepath)
            if not self.entry_name.get_text().strip():
                self.entry_name.set_text(os.path.splitext(os.path.basename(filepath))[0].title())
        dialog.destroy()

class AutostartManager(Gtk.Window):
    def __init__(self):
        super().__init__(title=_("Başlangıç Uygulamaları Yöneticisi"))
        self.set_default_size(800, 600)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_icon_name(APP_ICON)
        self.set_wmclass('baslangic-yoneticisi', 'baslangic-yoneticisi')
        self.current_selection = None
        self.load_settings()
        self.set_default_size(self.config.get("window_width", 800), self.config.get("window_height", 600))
        if self.config.get("window_maximized", False):
            self.maximize()
            
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.set_title(self.get_title())
        hb.set_subtitle(_("Sistem ve Kullanıcı uygulamalarını yönetin"))
        self.set_titlebar(hb)

        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_placeholder_text(_("Uygulama Ara..."))
        self.search_entry.connect("search-changed", self.on_search_changed)
        hb.pack_start(self.search_entry)

        if AppIndicator3:
            self.btn_tray = Gtk.Button()
            self.btn_tray.add(Gtk.Image.new_from_icon_name("go-down-symbolic", Gtk.IconSize.BUTTON))
            self.btn_tray.set_tooltip_text(_("Uygulamayı arka plana (Tray) gizle"))
            self.btn_tray.connect("clicked", self.on_tray_clicked)
            hb.pack_end(self.btn_tray)

        self.btn_remove = Gtk.Button()
        self.btn_remove.add(Gtk.Image.new_from_icon_name("user-trash-symbolic", Gtk.IconSize.BUTTON))
        self.btn_remove.set_tooltip_text(_("Kalıcı olarak sil"))
        self.btn_remove.connect("clicked", self.on_remove_clicked)
        self.btn_remove.get_style_context().add_class("destructive-action")
        self.btn_remove.set_sensitive(False)
        hb.pack_end(self.btn_remove)

        self.btn_stop = Gtk.Button()
        self.btn_stop.add(Gtk.Image.new_from_icon_name("media-playback-stop-symbolic", Gtk.IconSize.BUTTON))
        self.btn_stop.set_tooltip_text(_("Çalışan uygulamayı durdur (Kapat)"))
        self.btn_stop.connect("clicked", self.on_stop_clicked)
        self.btn_stop.set_sensitive(False)
        hb.pack_end(self.btn_stop)

        self.btn_start = Gtk.Button()
        self.btn_start.add(Gtk.Image.new_from_icon_name("media-playback-start-symbolic", Gtk.IconSize.BUTTON))
        self.btn_start.set_tooltip_text(_("Uygulamayı hemen çalıştırarak test et"))
        self.btn_start.connect("clicked", self.on_start_clicked)
        self.btn_start.set_sensitive(False)
        hb.pack_end(self.btn_start)

        self.btn_edit = Gtk.Button()
        self.btn_edit.add(Gtk.Image.new_from_icon_name("document-edit-symbolic", Gtk.IconSize.BUTTON))
        self.btn_edit.set_tooltip_text(_("Ayarları düzenle"))
        self.btn_edit.connect("clicked", self.on_edit_clicked)
        self.btn_edit.set_sensitive(False)
        hb.pack_end(self.btn_edit)

        self.btn_add = Gtk.Button()
        self.btn_add.add(Gtk.Image.new_from_icon_name("list-add-symbolic", Gtk.IconSize.BUTTON))
        self.btn_add.set_tooltip_text(_("Yeni uygulama veya script ekle"))
        self.btn_add.connect("clicked", self.on_add_clicked)
        self.btn_add.get_style_context().add_class("suggested-action")
        hb.pack_end(self.btn_add)

        hbox_main = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.add(hbox_main)
        
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_UP_DOWN)
        self.stack.connect("notify::visible-child-name", self.on_stack_page_changed)
        
        sidebar = Gtk.StackSidebar()
        sidebar.set_stack(self.stack)
        sidebar.set_size_request(160, -1)
        
        hbox_main.pack_start(sidebar, False, False, 0)
        hbox_main.pack_start(Gtk.Separator(orientation=Gtk.Orientation.VERTICAL), False, False, 0)
        hbox_main.pack_start(self.stack, True, True, 0)

        paned = Gtk.Paned(orientation=Gtk.Orientation.VERTICAL)
        paned.set_position(300)
        
        # Kullanici listesi alani
        box_user = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        box_user.set_margin_start(10)
        box_user.set_margin_end(10)
        box_user.set_margin_top(15)
        
        self.store_user = Gtk.ListStore(str, bool, str, str, str, bool, str, str, bool, int, str, bool, str)
        self.filter_user = self.store_user.filter_new()
        self.filter_user.set_visible_func(self.filter_func)
        
        lbl_user = Gtk.Label(xalign=0)
        lbl_user.set_markup(f"<span size='large' weight='bold' color='#2A7BDE'>{_('Kullanıcı Uygulamaları')}</span>")
        box_user.pack_start(lbl_user, False, False, 0)
        
        scroll_user = Gtk.ScrolledWindow()
        scroll_user.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.tree_user = self.create_treeview(self.filter_user)
        scroll_user.add(self.tree_user)
        box_user.pack_start(scroll_user, True, True, 0)
        
        # Sistem listesi alani
        self.box_sys = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.box_sys.set_margin_start(10)
        self.box_sys.set_margin_end(10)
        self.box_sys.set_margin_top(15)
        
        self.store_sys = Gtk.ListStore(str, bool, str, str, str, bool, str, str, bool, int, str, bool, str)
        self.filter_sys = self.store_sys.filter_new()
        self.filter_sys.set_visible_func(self.filter_func)
        
        lbl_sys = Gtk.Label(xalign=0)
        lbl_sys.set_markup(f"<span size='large' weight='bold' color='#E03C31'>{_('Sistem Uygulamaları')}</span>")
        self.box_sys.pack_start(lbl_sys, False, False, 0)
        
        scroll_sys = Gtk.ScrolledWindow()
        scroll_sys.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.tree_sys = self.create_treeview(self.filter_sys)
        scroll_sys.add(self.tree_sys)
        self.box_sys.pack_start(scroll_sys, True, True, 0)
        
        paned.pack1(box_user, True, False)
        paned.pack2(self.box_sys, True, False)
        self.box_sys.set_visible(self.config.get('show_sys_apps', True))
        
        page_apps = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        page_apps.pack_start(paned, True, True, 0)
        self.stack.add_titled(page_apps, "page_apps", _("Başlangıç"))
        
        # Ayarlar Sayfasi
        page_settings = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        page_settings.set_margin_top(30)
        page_settings.set_margin_start(30)
        page_settings.set_margin_end(30)
        
        
        # Ayar 1: Yenileme Suresi
        box_interval = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        lbl_interval = Gtk.Label(label=_("Durum Tarama Sıklığı (Saniye):"), xalign=0)
        box_interval.pack_start(lbl_interval, True, True, 0)
        
        adj_interval = Gtk.Adjustment(value=self.config["refresh_interval"], lower=1, upper=30, step_increment=1)
        spin_interval = Gtk.SpinButton(adjustment=adj_interval, numeric=True)
        spin_interval.connect("value-changed", self.on_interval_changed)
        box_interval.pack_start(spin_interval, False, False, 0)
        
        page_settings.pack_start(box_interval, False, False, 0)
        
        # Ayar 2: Sabit Tray
        box_tray = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        lbl_tray = Gtk.Label(label=_("Sistem Çekmecesinde (Tray) Her Zaman Göster:"), xalign=0)
        box_tray.pack_start(lbl_tray, True, True, 0)
        
        sw_tray = Gtk.Switch()
        sw_tray.set_active(self.config["tray_always_visible"])
        sw_tray.connect("notify::active", self.on_tray_switch_changed)
        box_tray.pack_start(sw_tray, False, False, 0)
        
        page_settings.pack_start(box_tray, False, False, 0)
        
        # Ayar 3: Sistem Uygulamalarini Goster
        box_show_sys = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        lbl_show_sys = Gtk.Label(label=_("Sistem Uygulamalarını (Alt Liste) Göster:"), xalign=0)
        box_show_sys.pack_start(lbl_show_sys, True, True, 0)
        
        sw_show_sys = Gtk.Switch()
        sw_show_sys.set_active(self.config.get("show_sys_apps", True))
        sw_show_sys.connect("notify::active", self.on_show_sys_changed)
        box_show_sys.pack_start(sw_show_sys, False, False, 0)
        
        page_settings.pack_start(box_show_sys, False, False, 0)
        
        # Ayar 4: Pencere Boyutu
        box_reset = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        lbl_reset = Gtk.Label(label=_("Pencere Boyutu ve Pozisyonu:"), xalign=0)
        box_reset.pack_start(lbl_reset, True, True, 0)
        
        btn_reset = Gtk.Button(label=_("Varsayılan Boyuta Dön"))
        btn_reset.connect("clicked", self.on_reset_size_clicked)
        box_reset.pack_start(btn_reset, False, False, 0)
        
        page_settings.pack_start(box_reset, False, False, 0)
        
        # Linger ayari
        import shutil
        if shutil.which("loginctl"):
            page_settings.pack_start(Gtk.Separator(), False, False, 10)
            box_linger = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            lbl_linger_title = Gtk.Label(label=_("<b>Gelişmiş Arka Plan İzni (Lingering)</b>"), use_markup=True, xalign=0)
            lbl_linger_desc = Gtk.Label(label=_("Bilgisayar açıldığında, siz henüz şifre girip oturum açmasanız bile\nzamanlanmış görevlerin (Sistem Açılışında - Boot) çalışabilmesi için gereklidir."), xalign=0)
            lbl_linger_desc.get_style_context().add_class("dim-label")
            box_linger.pack_start(lbl_linger_title, False, False, 0)
            box_linger.pack_start(lbl_linger_desc, False, False, 0)
            
            box_linger_btn = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            self.btn_linger = Gtk.ToggleButton(label=_("İzin Ver / Kaldır"))
            self.btn_linger.connect("toggled", self.on_linger_toggled)
            box_linger_btn.pack_start(self.btn_linger, False, False, 0)
            box_linger.pack_start(box_linger_btn, False, False, 5)
            
            page_settings.pack_start(box_linger, False, False, 0)
            self.check_linger_status()

        
        # Hakkinda Sayfasi
        page_about = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        page_about.set_margin_top(40)
        
        try:
            img = Gtk.Image.new_from_icon_name(APP_ICON, Gtk.IconSize.DIALOG)
            img.set_pixel_size(128)
            page_about.pack_start(img, False, False, 0)
        except: pass
        
        lbl_title = Gtk.Label(label=_("<b>Başlangıç Uygulamaları Yöneticisi</b>"), use_markup=True)
        page_about.pack_start(lbl_title, False, False, 0)
        
        lbl_desc = Gtk.Label(label=_("Sürüm: 1.1\nGeliştirici: Nikolayco"))
        lbl_desc.set_justify(Gtk.Justification.CENTER)
        page_about.pack_start(lbl_desc, False, False, 0)
        
        # Kayitlar (Logs) Sayfasi


        # SCHEDULER PAGE
        self.page_sched = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        import shutil
        if shutil.which("systemctl"):
            sched_toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
            self.btn_sched_add = Gtk.Button(label=_("Yeni Görev"))
            self.btn_sched_add.connect("clicked", self.on_sched_add)
            sched_toolbar.pack_start(self.btn_sched_add, False, False, 0)
            
            self.btn_sched_run = Gtk.Button(label=_("Şimdi Çalıştır"))
            self.btn_sched_run.set_sensitive(False)
            self.btn_sched_run.connect("clicked", self.on_sched_run)
            sched_toolbar.pack_start(self.btn_sched_run, False, False, 0)
            
            self.btn_sched_edit = Gtk.Button(label=_("Düzenle"))
            self.btn_sched_edit.set_sensitive(False)
            self.btn_sched_edit.connect("clicked", self.on_sched_edit)
            sched_toolbar.pack_start(self.btn_sched_edit, False, False, 0)
            
            self.btn_sched_rem = Gtk.Button(label=_("Sil"))
            self.btn_sched_rem.set_sensitive(False)
            self.btn_sched_rem.connect("clicked", self.on_sched_rem)
            sched_toolbar.pack_start(self.btn_sched_rem, False, False, 0)
            
            self.page_sched.pack_start(sched_toolbar, False, False, 0)
            
            # id, enabled, name, trigger_desc, next_run, cmd, type, val1, val2
            self.store_sched = Gtk.ListStore(str, bool, str, str, str, str, str, str, str)
            self.tree_sched = Gtk.TreeView(model=self.store_sched)
            
            render_toggle_sched = Gtk.CellRendererToggle()
            render_toggle_sched.connect("toggled", self.on_sched_toggled)
            col_t = Gtk.TreeViewColumn(_("Aktif"), render_toggle_sched, active=1)
            self.tree_sched.append_column(col_t)
            self.tree_sched.append_column(Gtk.TreeViewColumn(_("Görev"), Gtk.CellRendererText(), text=2))
            self.tree_sched.append_column(Gtk.TreeViewColumn(_("Tetikleyici"), Gtk.CellRendererText(), text=3))
            self.tree_sched.append_column(Gtk.TreeViewColumn(_("Sıradaki Çalışma"), Gtk.CellRendererText(), text=4))
            
            scroll_sched = Gtk.ScrolledWindow()
            scroll_sched.add(self.tree_sched)
            self.page_sched.pack_start(scroll_sched, True, True, 0)
            
            sel_sched = self.tree_sched.get_selection()
            sel_sched.set_mode(Gtk.SelectionMode.MULTIPLE)
            sel_sched.connect("changed", self.on_sched_selection_changed)
            
        else:
            lbl_nosys = Gtk.Label(label=_("Sisteminizde systemd bulunamadığı için zamanlayıcı kullanılamıyor."))
            self.page_sched.pack_start(lbl_nosys, True, True, 0)
            
        self.stack.add_titled(self.page_sched, "page_sched", _("Zamanlayıcı"))
        self.stack.add_titled(page_settings, "page_settings", _("Ayarlar"))

        # KISAYOLLAR SAYFASI
        page_shortcuts = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        page_shortcuts.set_margin_top(20)
        page_shortcuts.set_margin_start(20)
        page_shortcuts.set_margin_end(20)
        page_shortcuts.set_margin_bottom(20)

        lbl_sc_title = Gtk.Label(label=_("<b>Klavye Kısayolları</b>"), use_markup=True, xalign=0)
        lbl_sc_title.set_margin_bottom(15)
        page_shortcuts.pack_start(lbl_sc_title, False, False, 0)

        shortcuts_list = [
            ("Ctrl + N", _("Yeni başlangıç uygulaması ekle")),
            ("Ctrl + E", _("Seçili uygulamayı düzenle")),
            ("Ctrl + S", _("Seçili uygulamayı başlat")),
            ("Ctrl + K", _("Seçili uygulamayı durdur (öldür)")),
            ("Delete",   _("Seçili uygulamayı sil")),
            ("Ctrl + F", _("Arama kutusuna odaklan")),
        ]

        sc_store = Gtk.ListStore(str, str)
        for key, desc in shortcuts_list:
            sc_store.append([key, desc])

        sc_tree = Gtk.TreeView(model=sc_store)
        sc_tree.set_headers_visible(True)
        sc_tree.set_rules_hint(True)

        col_key = Gtk.TreeViewColumn(_("Kısayol"), Gtk.CellRendererText(), text=0)
        col_key.set_min_width(160)
        r_func = Gtk.CellRendererText()
        col_func = Gtk.TreeViewColumn(_("İşlev"), r_func, text=1)
        col_func.set_expand(True)
        sc_tree.append_column(col_key)
        sc_tree.append_column(col_func)

        sc_tree.set_can_focus(False)
        sc_tree.get_selection().set_mode(Gtk.SelectionMode.NONE)

        sc_scroll = Gtk.ScrolledWindow()
        sc_scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        sc_scroll.add(sc_tree)
        page_shortcuts.pack_start(sc_scroll, True, True, 0)

        self.stack.add_titled(page_shortcuts, "page_shortcuts", _("Klavye Kısayolları"))

        self.stack.add_titled(page_about, "page_about", _("Hakkında"))


        os.makedirs(AUTOSTART_DIR, exist_ok=True)
        os.makedirs(CUSTOM_SCRIPTS_DIR, exist_ok=True)
        
        wrapper_path = os.path.join(CUSTOM_SCRIPTS_DIR, "minimize_wrapper.sh")
        if not os.path.exists(wrapper_path):
            with open(wrapper_path, "w") as f:
                f.write("#!/bin/bash\nTITLE=$1\nshift\nfor i in {1..30}; do\n    WID=$(xdotool search --name \"$TITLE\" | head -1)\n    if [ -n \"$WID\" ]; then\n        xdotool windowminimize $WID\n        if xprop -id $WID | grep -q _NET_WM_STATE_HIDDEN; then\n            break\n        fi\n    fi\n    sleep 0.1\ndone\neval \"$@\"\n")
            os.chmod(wrapper_path, 0o755)

        runner_path = os.path.join(CUSTOM_SCRIPTS_DIR, "runner.py")
        with open(runner_path, "w") as f:
            f.write("""#!/usr/bin/env python3\nimport sys, os, subprocess, signal\npid_file = sys.argv[1]\ncmd = sys.argv[2]\nlog_file = sys.argv[3]\nwith open(pid_file, 'w') as f:\n    f.write(str(os.getpid()))\nwith open(log_file, 'w') as lf:\n    proc = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid, stdout=lf, stderr=subprocess.STDOUT)\n    def handler(signum, frame):\n        os.killpg(proc.pid, signal.SIGTERM)\n        sys.exit(0)\n    signal.signal(signal.SIGTERM, handler)\n    proc.wait()\n""")
        os.chmod(runner_path, 0o755)
            
        self.load_apps()
        self.load_sched_tasks()
        self.setup_tray()
        self.connect("delete-event", self.on_delete_event)
        self.connect("key-press-event", self.on_key_press)
        self.refresh_status()
        self.timer_id = GLib.timeout_add_seconds(self.config["refresh_interval"], self.refresh_status)

    def on_stack_page_changed(self, stack, param):
        is_main = (stack.get_visible_child_name() == "page_apps")
        self.search_entry.set_visible(is_main)
        self.btn_add.set_visible(is_main)
        self.btn_edit.set_visible(is_main)
        self.btn_start.set_visible(is_main)
        self.btn_stop.set_visible(is_main)
        self.btn_remove.set_visible(is_main)
        if hasattr(self, 'btn_tray'):
            self.btn_tray.set_visible(is_main)

    def load_settings(self):
        import json
        self.settings_file = os.path.join(CUSTOM_SCRIPTS_DIR, "settings.json")
        self.config = {"refresh_interval": 3, "tray_always_visible": False, "show_sys_apps": True, "window_width": 800, "window_height": 600, "window_maximized": False}
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r") as f:
                    self.config.update(json.load(f))
            except: pass

    def save_settings(self):
        import json
        try:
            with open(self.settings_file, "w") as f:
                json.dump(self.config, f)
        except: pass

    def on_interval_changed(self, spin):
        self.config["refresh_interval"] = int(spin.get_value())
        self.save_settings()
        if hasattr(self, 'timer_id') and self.timer_id:
            GLib.source_remove(self.timer_id)
        self.timer_id = GLib.timeout_add_seconds(self.config["refresh_interval"], self.refresh_status)

    def on_show_sys_changed(self, switch, gparam):
        self.config["show_sys_apps"] = switch.get_active()
        self.save_settings()
        if hasattr(self, 'box_sys'):
            self.box_sys.set_visible(self.config["show_sys_apps"])

    def on_tray_switch_changed(self, switch, gparam):
        self.config["tray_always_visible"] = switch.get_active()
        self.save_settings()
        if self.indicator:
            self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE if self.config["tray_always_visible"] else AppIndicator3.IndicatorStatus.PASSIVE)

    def refresh_status(self):
        try:
            import subprocess, os, shlex
            res = subprocess.run(["ps", "-eo", "pid,ppid,%cpu,rss,args="], stdout=subprocess.PIPE, text=True)
            lines = res.stdout.strip().split("\n")
        except:
            lines = []
            
        procs_by_pid = {}
        children_by_ppid = {}
        for line in lines:
            parts = line.strip().split(maxsplit=4)
            if len(parts) >= 5:
                pid, ppid, cpu, rss, args = parts[0], parts[1], 0.0, 0.0, parts[4]
                try: cpu = float(parts[2])
                except: pass
                try: rss = float(parts[3])
                except: pass
                procs_by_pid[pid] = {'cpu': cpu, 'rss': rss, 'args': args}
                children_by_ppid.setdefault(ppid, []).append(pid)

        def get_usage(pid_str):
            t_cpu = procs_by_pid.get(pid_str, {}).get('cpu', 0.0)
            t_mem_kb = procs_by_pid.get(pid_str, {}).get('rss', 0.0)
            
            # Add direct children usage (runner spawns the actual command)
            for child_pid in children_by_ppid.get(pid_str, []):
                t_cpu += procs_by_pid.get(child_pid, {}).get('cpu', 0.0)
                t_mem_kb += procs_by_pid.get(child_pid, {}).get('rss', 0.0)

            if t_cpu > 0 or t_mem_kb > 0:
                mb = t_mem_kb / 1024.0
                if mb > 1024: return f"[{pid_str}] {mb/1024.0:.1f}GB | %{t_cpu:.1f}"
                return f"[{pid_str}] {mb:.0f}MB | %{t_cpu:.1f}"
            return f"[{pid_str}]"

        def is_running(row):
            filename = row[7]
            cmd = row[3]
            
            pid_file = os.path.join(CUSTOM_SCRIPTS_DIR, "pids", f"{filename}.pid")
            if os.path.exists(pid_file):
                try:
                    with open(pid_file, "r") as f:
                        pid = f.read().strip()
                    if pid in procs_by_pid:
                        args = procs_by_pid[pid]['args']
                        if "runner.py" in args and filename in args:
                            return True, get_usage(pid)
                        elif args:
                            return False, ""
                except: pass
                
            try:
                clean_cmd = cmd.replace("%f", "").replace("%F", "").replace("%u", "").replace("%U", "")
                parts = shlex.split(clean_cmd)
                if not parts: return False, ""
                if parts[0] == "gnome-terminal" and "--" in parts:
                    idx = parts.index("--")
                    target = parts[idx+1] if len(parts) > idx+1 else parts[0]
                else:
                    target = parts[0]
                if target in ["bash", "sh", "python3", "python"] and len(parts) >= 2:
                    target = parts[-1] 
                
                if "runner.py" in target: return False, ""
                    
                base = os.path.basename(target)
                search_term = target if "/" in target else base
                if search_term in ["bash", "sh", "env"]: return False, ""
                
                for pid, info in procs_by_pid.items():
                    if search_term in info['args']:
                        return True, get_usage(pid)
                return False, ""
            except: 
                return False, ""

        for row in self.store_user: 
            is_run, usage = is_running(row)
            if row[11] != is_run: row[11] = is_run
            if row[12] != usage: row[12] = usage
        for row in self.store_sys: 
            is_run, usage = is_running(row)
            if row[11] != is_run: row[11] = is_run
            if row[12] != usage: row[12] = usage
        for row in self.store_sys: 
            new_val = is_running(row)
            if row[11] != new_val: row[11] = new_val
        
        if self.current_selection:
            model, treeiter = self.current_selection
            try:
                self.btn_stop.set_sensitive(model[treeiter][11])
            except: pass
            
        return True

    def on_tray_clicked(self, widget):
        if self.indicator:
            self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.hide()
        
    def restore_from_tray(self):
        if self.indicator:
            self.indicator.set_status(AppIndicator3.IndicatorStatus.PASSIVE)
        self.present()

    def on_reset_size_clicked(self, widget):
        self.unmaximize()
        self.resize(800, 600)
        self.config["window_width"] = 800
        self.config["window_height"] = 600
        self.config["window_maximized"] = False
        self.save_settings()

    def on_key_press(self, widget, event):
        if self.stack.get_visible_child_name() != "page_apps": return False
        keyname = Gdk.keyval_name(event.keyval)
        ctrl = event.state & Gdk.ModifierType.CONTROL_MASK
        
        if ctrl:
            if keyname == "n" or keyname == "N":
                self.on_add_clicked(None)
                return True
            elif keyname == "e" or keyname == "E":
                if self.current_selection: self.on_edit_clicked(None)
                return True
            elif keyname == "s" or keyname == "S":
                if self.current_selection: self.on_start_clicked(None)
                return True
            elif keyname == "k" or keyname == "K":
                if self.current_selection: self.on_stop_clicked(None)
                return True
        else:
            if keyname == "Delete":
                if self.current_selection: self.on_remove_clicked(None)
                return True
        return False

    def on_delete_event(self, widget, event):
        try:
            is_max = self.get_window().get_state() & Gdk.WindowState.MAXIMIZED
            self.config["window_maximized"] = bool(is_max)
            if not is_max:
                w, h = self.get_size()
                self.config["window_width"] = w
                self.config["window_height"] = h
            self.save_settings()
        except: pass
        Gtk.main_quit()
        return False

    def setup_tray(self):
        self.indicator = None
        if AppIndicator3:
            self.indicator = AppIndicator3.Indicator.new("gnome-startup-manager-indicator", APP_ICON, AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
            if self.config["tray_always_visible"]:
                self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
            else:
                self.indicator.set_status(AppIndicator3.IndicatorStatus.PASSIVE)
            self.update_tray_menu()

    def update_tray_menu(self):
        if not self.indicator: return
        menu = Gtk.Menu()
        item_title = Gtk.MenuItem(label=_("-- Hızlı Başlat --"))
        item_title.set_sensitive(False)
        menu.append(item_title)
        count = 0
        for row in self.store_user:
            count += 1
            item = Gtk.MenuItem(label=row[2])
            item.connect("activate", self.on_tray_execute, row[3])
            menu.append(item)
        if count == 0:
            empty = Gtk.MenuItem(label=_("Uygulama bulunamadı"))
            empty.set_sensitive(False)
            menu.append(empty)
        menu.append(Gtk.SeparatorMenuItem())
        item_show = Gtk.MenuItem(label=_("⚙️ Yöneticiyi Aç"))
        item_show.connect("activate", lambda w: self.restore_from_tray())
        menu.append(item_show)
        item_quit = Gtk.MenuItem(label=_("❌ Çıkış Yap"))
        item_quit.connect("activate", Gtk.main_quit)
        menu.append(item_quit)
        menu.show_all()
        self.indicator.set_menu(menu)

    def on_tray_execute(self, widget, cmd):
        try:
            cmd_clean = cmd.replace("%f", "").replace("%u", "").replace("%F", "").replace("%U", "")
            subprocess.Popen(shlex.split(cmd_clean), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except: pass

    def on_search_changed(self, widget):
        self.filter_user.refilter()
        self.filter_sys.refilter()

    def filter_func(self, model, iter, data):
        query = self.search_entry.get_text().lower()
        if not query: return True
        return query in model[iter][2].lower()

    def create_treeview(self, model):
        tree = Gtk.TreeView(model=model)
        tree.set_rules_hint(True)
        tree.connect("row-activated", self.on_row_activated)
        selection = tree.get_selection()
        selection.set_mode(Gtk.SelectionMode.MULTIPLE)
        selection.connect("changed", self.on_selection_changed, tree)
        
        render_toggle = Gtk.CellRendererToggle()
        render_toggle.connect("toggled", self.on_app_toggled, model)
        col_toggle = Gtk.TreeViewColumn(_("Aktif"), render_toggle, active=1)
        tree.append_column(col_toggle)

        col_name = Gtk.TreeViewColumn(_("Uygulama Adı"))
        col_name.set_resizable(True)
        col_name.set_expand(True)
        render_icon = Gtk.CellRendererPixbuf()
        render_icon.set_property("stock-size", Gtk.IconSize.DND)
        col_name.pack_start(render_icon, False)
        col_name.add_attribute(render_icon, "icon-name", 0)
        render_name = Gtk.CellRendererText()
        render_name.set_property("weight", 600)
        col_name.pack_start(render_name, True)
        col_name.add_attribute(render_name, "text", 2)
        tree.append_column(col_name)

        render_usage = Gtk.CellRendererText()
        render_usage.set_property("foreground", "#888888")
        col_usage = Gtk.TreeViewColumn(_("Kaynak"), render_usage, text=12)
        tree.append_column(col_usage)

        col_status = Gtk.TreeViewColumn(_("Durum"))
        render_status = Gtk.CellRendererText()
        col_status.pack_start(render_status, False)
        def format_status(c, cell, m, i, d):
            if m[i][11]:
                t = _("Çalışıyor")
                cell.set_property("markup", f"<span foreground='#2ca02c'>🟢 {t}</span>")
            else:
                t = _("Durdu")
                cell.set_property("markup", f"<span foreground='#7f7f7f'>⚪ {t}</span>")
        col_status.set_cell_data_func(render_status, format_status)
        tree.append_column(col_status)

        col_cmd = Gtk.TreeViewColumn(_("Komut"))
        col_cmd.set_resizable(True)
        col_cmd.set_expand(True)
        render_cmd = Gtk.CellRendererText()
        render_cmd.set_property("ellipsize", 3)
        render_cmd.set_property("foreground", "gray")
        col_cmd.pack_start(render_cmd, True)
        col_cmd.add_attribute(render_cmd, "text", 3)
        tree.append_column(col_cmd)
        
        col_term = Gtk.TreeViewColumn(_("Terminal"))
        render_term = Gtk.CellRendererText()
        col_term.pack_start(render_term, False)
        def format_term(c, cell, m, i, d):
            if not m[i][8]: cell.set_property("text", _("-"))
            else:
                s = m[i][10]
                if s == "maximize": cell.set_property("text", _("Evet (Max)"))
                elif s == "minimize": cell.set_property("text", _("Evet (Min)"))
                else: cell.set_property("text", _("Evet (Normal)"))
        col_term.set_cell_data_func(render_term, format_term)
        tree.append_column(col_term)

        col_delay = Gtk.TreeViewColumn(_("Gecikme"))
        render_delay = Gtk.CellRendererText()
        col_delay.pack_start(render_delay, False)
        col_delay.set_cell_data_func(render_delay, lambda c, cell, m, i, d: cell.set_property("text", f"{m[i][9]} sn" if m[i][9]>0 else _("-")))
        tree.append_column(col_delay)
        
        return tree

    def on_app_toggled(self, widget, path, filter_model):
        treeiter = filter_model.get_iter(path)
        self.write_desktop_file(filter_model[treeiter][7], filter_model[treeiter][2], filter_model[treeiter][3], filter_model[treeiter][4], filter_model[treeiter][8], filter_model[treeiter][10], filter_model[treeiter][9], not filter_model[treeiter][1])
        self.load_apps()

    def parse_desktop_file(self, path):
        name = os.path.basename(path).replace(".desktop", "")
        cmd, comment, hidden, icon, terminal, delay, term_size = "", "", False, "application-x-executable", False, 0, "normal"
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("Name="): name = line.split("=", 1)[1]
                    elif line.startswith("Exec="): cmd = line.split("=", 1)[1]
                    elif line.startswith("Comment="): comment = line.split("=", 1)[1]
                    elif line.startswith("Icon="): icon = line.split("=", 1)[1]
                    elif line.startswith("X-GNOME-Autostart-Delay="): 
                        try: delay = int(line.split("=", 1)[1])
                        except: pass
                    elif line.lower().startswith("terminal=true"): terminal = True
                    elif line.startswith("Hidden=true") or line.startswith("X-GNOME-Autostart-enabled=false"):
                        hidden = True
        except: pass
        if "/" in icon or "." in icon: icon = "application-x-executable"
        
        # Clean up runner wrapper from cmd
        import shlex
        if "runner.py" in cmd:
            try:
                parts = shlex.split(cmd)
                if "runner.py" in parts[1] or "runner.py" in parts[3] or "runner.py" in parts[-4]:
                    # Find runner.py index
                    idx = -1
                    for i, p in enumerate(parts):
                        if "runner.py" in p:
                            idx = i
                            break
                    if idx != -1 and len(parts) > idx + 2:
                        base_cmd = parts[idx+2]
                        if "minimize_wrapper.sh" in base_cmd:
                            m_parts = shlex.split(base_cmd)
                            if len(m_parts) >= 3:
                                cmd = " ".join(m_parts[2:])
                            else:
                                cmd = base_cmd
                        else:
                            cmd = base_cmd
            except: pass

        # keep original icon
        
        safe_name = "".join([c for c in name if c.isalnum()])
        wrapper_path = os.path.join(CUSTOM_SCRIPTS_DIR, "minimize_wrapper.sh")
        
        # New robust logic
        prefix1 = f'gnome-terminal --title="MINIMIZE_{safe_name}" -- bash -c "{wrapper_path} \'{safe_name}\' '
        prefix2 = f'gnome-terminal --title="MINIMIZE_{safe_name}" -- bash -c "{wrapper_path} \'MINIMIZE_{safe_name}\' '
        # Old legacy fallbacks
        prefix3 = f'gnome-terminal --title="MINIMIZE_{safe_name}" -- bash -c "xdotool search --sync --name \\\'MINIMIZE_{safe_name}\\\' windowminimize; '
        prefix4 = 'gnome-terminal -- bash -c "sleep 0.4 && xdotool getactivewindow windowminimize; '
        prefix5 = 'gnome-terminal -- bash -c "xdotool getactivewindow windowminimize; '

        if cmd.startswith("gnome-terminal --maximize -- "):
            cmd = cmd.replace("gnome-terminal --maximize -- ", "")
            term_size = "maximize"
            terminal = True
        elif cmd.startswith(prefix1) and cmd.endswith('"'):
            cmd = cmd[len(prefix1):-1]
            term_size = "minimize"
            terminal = True
        elif cmd.startswith(prefix2) and cmd.endswith('"'):
            cmd = cmd[len(prefix2):-1]
            term_size = "minimize"
            terminal = True
        elif cmd.startswith(prefix3) and cmd.endswith('"'):
            cmd = cmd[len(prefix3):-1]
            term_size = "minimize"
            terminal = True
        elif cmd.startswith(prefix4) and cmd.endswith('"'):
            cmd = cmd[len(prefix4):-1]
            term_size = "minimize"
            terminal = True
        elif cmd.startswith(prefix5) and cmd.endswith('"'):
            cmd = cmd[len(prefix5):-1]
            term_size = "minimize"
            terminal = True
            
        is_sys_actual = os.path.exists(os.path.join(SYS_AUTOSTART_DIR, os.path.basename(path)))
        return AutostartApp(os.path.basename(path), name, cmd, comment, hidden, is_sys_actual, path, icon, terminal, delay, term_size)

    def load_apps(self):
        self.store_user.clear()
        self.store_sys.clear()
        paths = []
        if os.path.exists(AUTOSTART_DIR): paths.extend(glob.glob(os.path.join(AUTOSTART_DIR, "*.desktop")))
        if os.path.exists(SYS_AUTOSTART_DIR): paths.extend(glob.glob(os.path.join(SYS_AUTOSTART_DIR, "*.desktop")))
        seen = {}
        for p in paths:
            fname = os.path.basename(p)
            if fname not in seen: seen[fname] = os.path.join(AUTOSTART_DIR, fname) if os.path.exists(os.path.join(AUTOSTART_DIR, fname)) else p
        all_apps = []
        for fname, path in seen.items():
            app = self.parse_desktop_file(path)
            if app.cmd: all_apps.append(app)
        all_apps.sort(key=lambda x: x.name.lower())
        for app in all_apps:
            row = [app.icon, app.enabled, app.name, app.cmd, app.comment, app.is_sys, app.path, app.filename, app.terminal, app.delay, app.term_size, False, ""]
            if app.is_sys: self.store_sys.append(row)
            else: self.store_user.append(row)
        if hasattr(self, 'indicator'): self.update_tray_menu()

    def on_selection_changed(self, selection, treeview):
        model, paths = selection.get_selected_rows()
        if paths:
            other = self.tree_sys if treeview == self.tree_user else self.tree_user
            other.get_selection().unselect_all()
            self.current_selection_paths = paths
            self.current_model = model
            self.current_selection = (model, model.get_iter(paths[0]))
            self.btn_start.set_sensitive(True)
            self.btn_stop.set_sensitive(any(model[model.get_iter(p)][11] for p in paths))
            self.btn_remove.set_sensitive(True)
            self.btn_edit.set_sensitive(len(paths) == 1)
        else:
            if not self.tree_user.get_selection().get_selected_rows()[1] and not self.tree_sys.get_selection().get_selected_rows()[1]:
                self.current_selection_paths = []
                self.current_model = None
                self.current_selection = None
                self.btn_start.set_sensitive(False)
                self.btn_stop.set_sensitive(False)
                self.btn_remove.set_sensitive(False)
                self.btn_edit.set_sensitive(False)

    def on_row_activated(self, treeview, path, column):
        self.on_edit_clicked(None)

    def write_desktop_file(self, filename, name, cmd, comment, terminal, term_size, delay, enabled, icon="application-x-executable"):
        path = os.path.join(AUTOSTART_DIR, filename)
        
        pid_dir = os.path.join(CUSTOM_SCRIPTS_DIR, "pids")
        os.makedirs(pid_dir, exist_ok=True)
        pid_file = os.path.join(pid_dir, f"{filename}.pid")
        runner_path = os.path.join(CUSTOM_SCRIPTS_DIR, "runner.py")
        
        safe_name = "".join([c for c in name if c.isalnum()])
        
        if terminal and term_size == "minimize":
            wrapper_path = os.path.join(CUSTOM_SCRIPTS_DIR, "minimize_wrapper.sh")
            base_cmd = f"{wrapper_path} 'MINIMIZE_{safe_name}' {cmd}"
        else:
            base_cmd = cmd
            
        log_dir = os.path.join(CUSTOM_SCRIPTS_DIR, "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"{filename}.log")
        import shlex
        runner_exec = f'python3 {shlex.quote(runner_path)} {shlex.quote(pid_file)} {shlex.quote(base_cmd)} {shlex.quote(log_file)}'
        
        if terminal:
            if term_size == "maximize":
                final_cmd = f"gnome-terminal --maximize -- {runner_exec}"
            elif term_size == "minimize":
                final_cmd = f'gnome-terminal --title="MINIMIZE_{safe_name}" -- {runner_exec}'
            else:
                final_cmd = f"gnome-terminal -- {runner_exec}"
        else:
            final_cmd = runner_exec
                
        en_str = "true" if enabled else "false"
        hidden_str = "false" if enabled else "true"
        content = f"[Desktop Entry]\nType=Application\nName={name}\nExec={final_cmd}\nComment={comment}\nIcon={icon}\nTerminal=false\nHidden={hidden_str}\nX-GNOME-Autostart-enabled={en_str}\n"
        if delay > 0: content += f"X-GNOME-Autostart-Delay={delay}\n"
        with open(path, 'w', encoding='utf-8') as f: f.write(content)

    def save_custom_script(self, filename, code):
        script_path = os.path.join(CUSTOM_SCRIPTS_DIR, filename.replace('.desktop', '.sh'))
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write("#!/usr/bin/env bash\n" + code + "\n")
        os.chmod(script_path, 0o755)
        return script_path

    def on_add_clicked(self, widget):
        dialog = AppDialog(self, _("Yeni Başlangıç Öğesi Ekle"))
        if dialog.run() == Gtk.ResponseType.OK:
            name, comment, terminal, term_size, delay, icon = dialog.entry_name.get_text(), dialog.entry_comment.get_text(), dialog.check_terminal.get_active(), dialog.combo_term_size.get_active_id(), int(dialog.spin_delay.get_value()), dialog.original_icon
            if dialog.stack.get_visible_child_name() == "file": cmd = dialog.entry_cmd.get_text()
            else:
                buf = dialog.text_buffer
                code = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True).strip()
                cmd = self.save_custom_script(name.lower().replace(" ", "-").replace("/", "") + ".desktop", code) if code else ""
            if name and cmd:
                self.write_desktop_file(name.lower().replace(" ", "-").replace("/", "") + ".desktop", name, cmd, comment, terminal, term_size, delay, True)
                self.load_apps()
        dialog.destroy()

    def on_edit_clicked(self, widget):
        if not self.current_selection: return
        model, treeiter = self.current_selection
        app = self.parse_desktop_file(model[treeiter][6])
        dialog = AppDialog(self, _("Öğeyi Düzenle"), app)
        if dialog.run() == Gtk.ResponseType.OK:
            name, comment, terminal, term_size, delay, icon = dialog.entry_name.get_text(), dialog.entry_comment.get_text(), dialog.check_terminal.get_active(), dialog.combo_term_size.get_active_id(), int(dialog.spin_delay.get_value()), dialog.original_icon
            if dialog.stack.get_visible_child_name() == "file": cmd = dialog.entry_cmd.get_text()
            else:
                buf = dialog.text_buffer
                code = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True).strip()
                cmd = self.save_custom_script(app.filename, code) if code else app.cmd
            if name and cmd:
                self.write_desktop_file(app.filename, name, cmd, comment, terminal, term_size, delay, app.enabled)
                self.load_apps()
        dialog.destroy()

    def on_remove_clicked(self, widget):
        if not getattr(self, 'current_selection_paths', []): return
        model = self.current_model
        count = len(self.current_selection_paths)
        msg = _("Bu öğeyi silmek istediğinize emin misiniz?") if count == 1 else _(f"Seçili {count} öğeyi silmek istediğinize emin misiniz?")
        dialog = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.QUESTION,
                                   buttons=Gtk.ButtonsType.YES_NO, text=msg)
        if dialog.run() == Gtk.ResponseType.YES:
            paths = [Gtk.TreePath(p) for p in self.current_selection_paths]
            paths.sort(reverse=True)
            for path in paths:
                treeiter = model.get_iter(path)
                filename = model[treeiter][7]
                filepath = os.path.join(AUTOSTART_DIR, filename)
                if os.path.exists(filepath): os.remove(filepath)
            self.load_apps()
        dialog.destroy()

    def on_stop_clicked(self, widget):
        if not getattr(self, 'current_selection_paths', []): return
        model = self.current_model
        for path in self.current_selection_paths:
            treeiter = model.get_iter(path)
            filename = model[treeiter][7]
            cmd = model[treeiter][3]
            
            import os, subprocess, shlex
            pid_file = os.path.join(CUSTOM_SCRIPTS_DIR, "pids", f"{filename}.pid")
            killed = False
            if os.path.exists(pid_file):
                try:
                    with open(pid_file, "r") as f:
                        pid = f.read().strip()
                    if pid.isdigit():
                        subprocess.run(["kill", "-TERM", pid])
                        killed = True
                except: pass
                
            if not killed:
                try:
                    clean_cmd = cmd.replace("%f", "").replace("%u", "").replace("%F", "").replace("%U", "")
                    parts = shlex.split(clean_cmd)
                    if not parts: continue
                    if parts[0] == "gnome-terminal" and "--" in parts:
                        idx = parts.index("--")
                        target = parts[idx+1] if len(parts) > idx+1 else parts[0]
                    else:
                        target = parts[0]
                    if target in ["bash", "sh", "python3", "python"] and len(parts) >= 2:
                        target = parts[-1] 
                    base = os.path.basename(target)
                    search_term = target if "/" in target else base
                    if search_term in ["bash", "sh", "env"]: continue
                    subprocess.run(["pkill", "-f", search_term])
                except: pass
        self.refresh_status()

    def on_start_clicked(self, widget):
        if not self.current_selection: return
        model, treeiter = self.current_selection
        try:
            app_info = Gio.DesktopAppInfo.new_from_filename(model[treeiter][6])
            if app_info: app_info.launch([], Gdk.Display.get_default().get_app_launch_context())
            else: subprocess.Popen(shlex.split(model[treeiter][3].replace("%f", "").replace("%u", "").replace("%F", "").replace("%U", "")), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            d = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK, text=_("Çalıştırma Hatası!"))
            d.format_secondary_text(str(e))
            d.run()
            d.destroy()


    def check_linger_status(self):
        if not hasattr(self, 'btn_linger'): return
        import subprocess, os
        # Loginctl show-user $USER --property=Linger
        res = subprocess.run(["loginctl", "show-user", os.getenv("USER"), "--property=Linger"], stdout=subprocess.PIPE, text=True)
        is_linger = "Linger=yes" in res.stdout
        
        self.btn_linger.handler_block_by_func(self.on_linger_toggled)
        self.btn_linger.set_active(is_linger)
        self.btn_linger.set_label(_("İzin Verildi (Aktif)") if is_linger else _("İzin Ver (Lingering'i Aç)"))
        self.btn_linger.handler_unblock_by_func(self.on_linger_toggled)

    def on_linger_toggled(self, widget):
        import subprocess, os
        enable = widget.get_active()
        cmd = "enable-linger" if enable else "disable-linger"
        subprocess.run(["loginctl", cmd, os.getenv("USER")])
        self.check_linger_status()

    def on_sched_toggled(self, widget, path):
        treeiter = self.store_sched.get_iter(path)
        current_state = self.store_sched[treeiter][1]
        t_id = self.store_sched[treeiter][0]
        new_state = not current_state
        self.store_sched[treeiter][1] = new_state
        
        import subprocess
        cmd = "enable" if new_state else "disable"
        subprocess.run(["systemctl", "--user", cmd, "--now", f"{t_id}.timer"])
        subprocess.run(["systemctl", "--user", "daemon-reload"])

    def on_sched_selection_changed(self, selection):
        model, paths = selection.get_selected_rows()
        self.current_sched_paths = paths
        self.btn_sched_run.set_sensitive(len(paths) > 0)
        self.btn_sched_edit.set_sensitive(len(paths) == 1)
        self.btn_sched_rem.set_sensitive(len(paths) > 0)

    def on_sched_run(self, widget):
        if not getattr(self, 'current_sched_paths', []): return
        import subprocess
        for path in self.current_sched_paths:
            treeiter = self.store_sched.get_iter(path)
            t_id = self.store_sched[treeiter][0]
            # Servisi manuel tetikle
            subprocess.Popen(["systemctl", "--user", "start", f"{t_id}.service"])

    def on_sched_add(self, widget):
        dialog = ScheduleDialog(self, _("Yeni Görev"))
        if dialog.run() == Gtk.ResponseType.OK:
            self._save_dialog_to_sched(dialog)
        dialog.destroy()

    def on_sched_edit(self, widget):
        if not getattr(self, 'current_sched_paths', []): return
        path = self.current_sched_paths[0]
        treeiter = self.store_sched.get_iter(path)
        task = {
            'id': self.store_sched[treeiter][0],
            'name': self.store_sched[treeiter][2],
            'cmd': self.store_sched[treeiter][5],
            'type': self.store_sched[treeiter][6],
            'val_int': int(self.store_sched[treeiter][7]) if self.store_sched[treeiter][6] == 'interval' else 1,
            'val_unit': self.store_sched[treeiter][8] if self.store_sched[treeiter][6] == 'interval' else 'min',
            'val_cal': self.store_sched[treeiter][7] if self.store_sched[treeiter][6] == 'calendar' else '',
            'val_delay': int(self.store_sched[treeiter][7]) if self.store_sched[treeiter][6] in ['boot', 'login'] else 0
        }
        dialog = ScheduleDialog(self, _("Görevi Düzenle"), task)
        if dialog.run() == Gtk.ResponseType.OK:
            self._save_dialog_to_sched(dialog, task_id=task['id'])
        dialog.destroy()

    def _save_dialog_to_sched(self, dialog, task_id=None):
        name = dialog.entry_name.get_text().strip()
        cmd = dialog.entry_cmd.get_text().strip()
        if not name or not cmd: return
        
        if dialog.switch_term.get_active() and not cmd.startswith("gnome-terminal"):
            cmd = f"gnome-terminal -- {cmd}" 
        
        t_type = dialog.combo_type.get_active_id()
        if not task_id:
            import uuid
            task_id = "gsam-" + str(uuid.uuid4())[:8]
            
        v1, v2 = "", ""
        if t_type == 'interval':
            v1 = str(int(dialog.spin_int.get_value()))
            v2 = dialog.combo_int_unit.get_active_id()
            t_desc = f"Her {v1} {dialog.combo_int_unit.get_active_text()}"
        elif t_type == 'calendar':
            v1 = dialog.entry_cal.get_text().strip()
            t_desc = f"Takvim: {v1}"
        elif t_type == 'boot':
            v1 = str(int(dialog.spin_boot.get_value()))
            t_desc = f"Sistem açılışında ({v1}s)"
        elif t_type == 'login':
            v1 = str(int(dialog.spin_login.get_value()))
            t_desc = f"Oturum açıldığında ({v1}s)"
            
        self._write_systemd_files(task_id, name, cmd, t_type, v1, v2)
        import subprocess
        subprocess.run(["systemctl", "--user", "daemon-reload"])
        subprocess.run(["systemctl", "--user", "enable", "--now", f"{task_id}.timer"])
        self.load_sched_tasks()

    def _write_systemd_files(self, task_id, name, cmd, t_type, v1, v2):
        import shlex, os
        runner_path = os.path.join(CUSTOM_SCRIPTS_DIR, "runner.py")
        pid_file = os.path.join(CUSTOM_SCRIPTS_DIR, "pids", f"{task_id}.pid")
        log_file = os.path.join(CUSTOM_SCRIPTS_DIR, "logs", f"{task_id}.log")
        exec_start = f'python3 {shlex.quote(runner_path)} {shlex.quote(pid_file)} {shlex.quote(cmd)} {shlex.quote(log_file)}'
        
        srv = f"""[Unit]
Description=GSAM Görev: {name}

[Service]
Type=oneshot
ExecStart={exec_start}
"""
        with open(os.path.join(SYSTEMD_USER_DIR, f"{task_id}.service"), "w") as f: f.write(srv)
        
        tmr = f"""[Unit]
Description=Timer: {name}

[Timer]
Persistent=true
"""
        if t_type == 'interval': tmr += f"OnUnitActiveSec={v1}{v2}\n"
        elif t_type == 'calendar': tmr += f"OnCalendar={v1}\n"
        elif t_type == 'boot': tmr += f"OnBootSec={v1}s\n"
        elif t_type == 'login': tmr += f"OnStartupSec={v1}s\n"
        tmr += "[Install]\nWantedBy=timers.target\n"
        
        with open(os.path.join(SYSTEMD_USER_DIR, f"{task_id}.timer"), "w") as f: f.write(tmr)

    def on_sched_rem(self, widget):
        if not getattr(self, 'current_sched_paths', []): return
        dialog = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.QUESTION, buttons=Gtk.ButtonsType.YES_NO, text=_("Seçili görevleri silmek istiyor musunuz?"))
        if dialog.run() == Gtk.ResponseType.YES:
            import subprocess, os
            for path in self.current_sched_paths:
                treeiter = self.store_sched.get_iter(path)
                t_id = self.store_sched[treeiter][0]
                subprocess.run(["systemctl", "--user", "disable", "--now", f"{t_id}.timer"])
                sf = os.path.join(SYSTEMD_USER_DIR, f"{t_id}.service")
                tf = os.path.join(SYSTEMD_USER_DIR, f"{t_id}.timer")
                if os.path.exists(sf): os.remove(sf)
                if os.path.exists(tf): os.remove(tf)
            subprocess.run(["systemctl", "--user", "daemon-reload"])
            self.load_sched_tasks()
        dialog.destroy()

    def load_sched_tasks(self):
        if not hasattr(self, 'store_sched'): return
        self.store_sched.clear()
        import os
        if not os.path.exists(SYSTEMD_USER_DIR): return
        
        import subprocess, configparser
        res = subprocess.run(["systemctl", "--user", "is-enabled", "*"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Parse timers
        import glob
        for tf in glob.glob(os.path.join(SYSTEMD_USER_DIR, "gsam-*.timer")):
            t_id = os.path.basename(tf).replace(".timer", "")
            sf = os.path.join(SYSTEMD_USER_DIR, f"{t_id}.service")
            if not os.path.exists(sf): continue
            
            c = configparser.ConfigParser(strict=False)
            try: c.read(tf)
            except: pass
            
            s = configparser.ConfigParser(strict=False)
            try: s.read(sf)
            except: pass
            
            name = s.get("Unit", "Description", fallback=t_id).replace("GSAM Görev: ", "")
            enabled = (subprocess.run(["systemctl", "--user", "is-active", f"{t_id}.timer"], stdout=subprocess.PIPE).returncode == 0)
            
            cmd = ""
            with open(sf, "r") as s_file:
                for line in s_file:
                    if line.startswith("ExecStart="):
                        cmd_full = line.split("=", 1)[1].strip()
                        import shlex
                        parts = shlex.split(cmd_full)
                        if len(parts) >= 4:
                            cmd = parts[3]
            
            t_type, v1, v2, t_desc = "", "", "", "Bilinmiyor"
            if c.has_option("Timer", "OnUnitActiveSec"):
                t_type = "interval"
                v = c.get("Timer", "OnUnitActiveSec")
                v1, v2 = "".join(filter(str.isdigit, v)), "".join(filter(str.isalpha, v))
                t_desc = f"Her {v1} {v2}"
            elif c.has_option("Timer", "OnCalendar"):
                t_type = "calendar"
                v1 = c.get("Timer", "OnCalendar")
                t_desc = f"Takvim: {v1}"
            elif c.has_option("Timer", "OnBootSec"):
                t_type = "boot"
                v1 = c.get("Timer", "OnBootSec").replace("s", "")
                t_desc = f"Boot ({v1}s)"
            elif c.has_option("Timer", "OnStartupSec"):
                t_type = "login"
                v1 = c.get("Timer", "OnStartupSec").replace("s", "")
                t_desc = f"Login ({v1}s)"
                
            next_run = "-"
            timer_res = subprocess.run(["systemctl", "--user", "list-timers", "--all", f"{t_id}.timer"], stdout=subprocess.PIPE, text=True)
            for line in timer_res.stdout.split("\n"):
                if f"{t_id}.timer" in line:
                    parts = line.split(f"{t_id}.timer")
                    left_part = parts[0].strip()
                    if left_part.startswith("-"): next_run = "-"
                    else: 
                        import shlex
                        time_parts = shlex.split(left_part)
                        if len(time_parts) >= 3:
                            next_run = " ".join(time_parts[:3])
                    break
            
            self.store_sched.append([t_id, enabled, name, t_desc, next_run, cmd, t_type, v1, v2])

if __name__ == "__main__":

    app = AutostartManager()
    import sys
    if "--tray" in sys.argv:
        if not app.indicator: app.show_all()
    else: app.show_all()
    Gtk.main()
