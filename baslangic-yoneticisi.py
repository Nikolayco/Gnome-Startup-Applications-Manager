#!/usr/bin/env python3
import os
import glob
import shlex
import subprocess
import gettext
import locale
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib, Gdk
GLib.set_prgname('baslangic-yoneticisi')

APP_NAME = "gnome-startup-manager"
LOCALE_DIR = os.path.expanduser("~/.local/share/locale")

try:
    locale.setlocale(locale.LC_ALL, '')
except locale.Error:
    pass

try:
    gettext.bindtextdomain(APP_NAME, LOCALE_DIR)
    gettext.textdomain(APP_NAME)
    _ = gettext.gettext
except Exception:
    _ = lambda s: s

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
        self.entry_cmd = Gtk.Entry(placeholder_text=_("Dosya yolu veya komut..."))
        self.entry_cmd.set_hexpand(True)
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
        
        self.store_user = Gtk.ListStore(str, bool, str, str, str, bool, str, str, bool, int, str, bool)
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
        
        self.store_sys = Gtk.ListStore(str, bool, str, str, str, bool, str, str, bool, int, str, bool)
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

        self.stack.add_titled(page_settings, "page_settings", _("Ayarlar"))
        
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
        
        lbl_desc = Gtk.Label(label=_("Sürüm: 1.0\nGeliştirici: Nikolayco"))
        lbl_desc.set_justify(Gtk.Justification.CENTER)
        page_about.pack_start(lbl_desc, False, False, 0)
        
        # Kayitlar (Logs) Sayfasi
        self.page_logs = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.page_logs.set_margin_top(15)
        self.page_logs.set_margin_start(15)
        self.page_logs.set_margin_end(15)
        self.page_logs.set_margin_bottom(15)
        
        box_log_top = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        lbl_log = Gtk.Label(label=_("<b>Uygulama Çıktıları (Canlı Log)</b>"), use_markup=True, xalign=0)
        box_log_top.pack_start(lbl_log, True, True, 0)
        
        self.combo_logs = Gtk.ComboBoxText()
        self.combo_logs.connect("changed", self.on_log_selection_changed)
        box_log_top.pack_start(self.combo_logs, False, False, 0)
        
        btn_refresh_log = Gtk.Button(label=_("Yenile"))
        btn_refresh_log.connect("clicked", self.on_log_selection_changed)
        box_log_top.pack_start(btn_refresh_log, False, False, 0)
        
        self.page_logs.pack_start(box_log_top, False, False, 0)
        
        scroll_logs = Gtk.ScrolledWindow()
        scroll_logs.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.textview_logs = Gtk.TextView()
        self.textview_logs.set_editable(False)
        self.textview_logs.set_wrap_mode(Gtk.WrapMode.WORD)
        self.textview_logs.get_style_context().add_class("terminal-font")
        scroll_logs.add(self.textview_logs)
        self.page_logs.pack_start(scroll_logs, True, True, 0)
        
        self.stack.add_titled(self.page_logs, "page_logs", _("Kayıtlar (Log)"))

        self.stack.add_titled(page_about, "page_about", _("Hakkında"))


        os.makedirs(AUTOSTART_DIR, exist_ok=True)
        os.makedirs(CUSTOM_SCRIPTS_DIR, exist_ok=True)
        
        wrapper_path = os.path.join(CUSTOM_SCRIPTS_DIR, "minimize_wrapper.sh")
        if not os.path.exists(wrapper_path):
            with open(wrapper_path, "w") as f:
                f.write("#!/bin/bash\nTITLE=$1\nshift\nfor i in {1..30}; do\n    WID=$(xdotool search --name \"$TITLE\" | head -1)\n    if [ -n \"$WID\" ]; then\n        xdotool windowminimize $WID\n        if xprop -id $WID | grep -q _NET_WM_STATE_HIDDEN; then\n            break\n        fi\n    fi\n    sleep 0.1\ndone\neval \"$@\"\n")
            os.chmod(wrapper_path, 0o755)

        runner_path = os.path.join(CUSTOM_SCRIPTS_DIR, "runner.py")
        if not os.path.exists(runner_path):
            with open(runner_path, "w") as f:
                f.write("""#!/usr/bin/env python3\nimport sys, os, subprocess, signal\npid_file = sys.argv[1]\ncmd = sys.argv[2]\nwith open(pid_file, 'w') as f:\n    f.write(str(os.getpid()))\nproc = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)\ndef handler(signum, frame):\n    os.killpg(proc.pid, signal.SIGTERM)\n    sys.exit(0)\nsignal.signal(signal.SIGTERM, handler)\nproc.wait()\n""")
            os.chmod(runner_path, 0o755)
            
        self.load_apps()
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
            
        if stack.get_visible_child_name() == "page_logs":
            self.populate_log_combo()

    def populate_log_combo(self):
        self.combo_logs.remove_all()
        log_dir = os.path.join(CUSTOM_SCRIPTS_DIR, "logs")
        if os.path.exists(log_dir):
            import glob
            logs = glob.glob(os.path.join(log_dir, "*.log"))
            for log in sorted(logs):
                basename = os.path.basename(log)
                self.combo_logs.append(log, basename.replace(".log", ""))
        self.combo_logs.set_active(0)

    def on_log_selection_changed(self, widget):
        log_file = self.combo_logs.get_active_id()
        buffer = self.textview_logs.get_buffer()
        if not log_file or not os.path.exists(log_file):
            buffer.set_text(_("Gösterilecek log dosyası bulunamadı."))
            return
        try:
            with open(log_file, "r") as f:
                log_content = f.read()
            if not log_content.strip():
                log_content = _("(Dosya boş, henüz çıktı üretilmemiş)")
            buffer.set_text(log_content)
        except Exception as e:
            buffer.set_text(f"Hata: {str(e)}")

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
            res = subprocess.run(["ps", "-eo", "args"], stdout=subprocess.PIPE, text=True)
            all_procs = res.stdout
        except:
            all_procs = ""
            
        def is_running(row):
            filename = row[7]
            cmd = row[3]
            
            pid_file = os.path.join(CUSTOM_SCRIPTS_DIR, "pids", f"{filename}.pid")
            if os.path.exists(pid_file):
                try:
                    with open(pid_file, "r") as f:
                        pid = f.read().strip()
                    if pid.isdigit():
                        res = subprocess.run(["ps", "-p", pid, "-o", "args="], stdout=subprocess.PIPE, text=True)
                        out = res.stdout.strip()
                        if "runner.py" in out and filename in out:
                            return True
                        elif out:
                            return False
                except: pass
                
            try:
                clean_cmd = cmd.replace("%f", "").replace("%F", "").replace("%u", "").replace("%U", "")
                parts = shlex.split(clean_cmd)
                if not parts: return False
                if parts[0] == "gnome-terminal" and "--" in parts:
                    idx = parts.index("--")
                    target = parts[idx+1] if len(parts) > idx+1 else parts[0]
                else:
                    target = parts[0]
                if target in ["bash", "sh", "python3", "python"] and len(parts) >= 2:
                    target = parts[-1] 
                
                if "runner.py" in target: return False
                    
                base = os.path.basename(target)
                search_term = target if "/" in target else base
                if search_term in ["bash", "sh", "env"]: return False
                return search_term in all_procs
            except: 
                return False
                
        for row in self.store_user: 
            new_val = is_running(row)
            if row[11] != new_val: row[11] = new_val
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

        col_status = Gtk.TreeViewColumn(_("Durum"))
        render_status = Gtk.CellRendererText()
        col_status.pack_start(render_status, False)
        def format_status(c, cell, m, i, d):
            if m[i][11]:
                cell.set_property("markup", "<span foreground='#2ca02c'>🟢 Çalışıyor</span>")
            else:
                cell.set_property("markup", "<span foreground='#7f7f7f'>⚪ Durdu</span>")
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
            row = [app.icon, app.enabled, app.name, app.cmd, app.comment, app.is_sys, app.path, app.filename, app.terminal, app.delay, app.term_size, False]
            if app.is_sys: self.store_sys.append(row)
            else: self.store_user.append(row)
        if hasattr(self, 'indicator'): self.update_tray_menu()

    def on_selection_changed(self, selection, treeview):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            other = self.tree_sys if treeview == self.tree_user else self.tree_user
            other.get_selection().unselect_all()
            self.current_selection = (model, treeiter)
            self.btn_start.set_sensitive(True)
            self.btn_stop.set_sensitive(model[treeiter][11])
            self.btn_remove.set_sensitive(True)
            self.btn_edit.set_sensitive(True)
        else:
            if not self.tree_user.get_selection().get_selected()[1] and not self.tree_sys.get_selection().get_selected()[1]:
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
        runner_exec = f'python3 "{runner_path}" "{pid_file}" "{base_cmd}" "{log_file}"'
        
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
        if not self.current_selection: return
        model, treeiter = self.current_selection
        dialog = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.WARNING, buttons=Gtk.ButtonsType.YES_NO, text=_("Bu öğeyi KALICI OLARAK silmek istiyor musunuz?\\nGeçici olarak durdurmak için listeden 'Aktif' tikini kaldırabilirsiniz."))
        if dialog.run() == Gtk.ResponseType.YES:
            if model[treeiter][5]:
                with open(os.path.join(AUTOSTART_DIR, model[treeiter][7]), 'w', encoding='utf-8') as f: f.write("[Desktop Entry]\nHidden=true\nX-GNOME-Autostart-enabled=false\n")
            else:
                if os.path.exists(os.path.join(AUTOSTART_DIR, model[treeiter][7])): os.remove(os.path.join(AUTOSTART_DIR, model[treeiter][7]))
            self.load_apps()
        dialog.destroy()

    def on_stop_clicked(self, widget):
        if not self.current_selection: return
        model, treeiter = self.current_selection
        cmd = model[treeiter][3]
        import shlex, os, subprocess
        try:
            clean_cmd = cmd.replace("%f", "").replace("%F", "").replace("%u", "").replace("%U", "")
            parts = shlex.split(clean_cmd)
            if not parts: return
            if parts[0] == "gnome-terminal" and "--" in parts:
                idx = parts.index("--")
                target = parts[idx+1] if len(parts) > idx+1 else parts[0]
            else:
                target = parts[0]
            if target in ["bash", "sh", "python3", "python"] and len(parts) >= 2:
                target = parts[-1] 
                
            if "minimize_wrapper.sh" in target:
                try:
                    w_parts = shlex.split(target)
                    if len(w_parts) >= 3:
                        target = w_parts[2]
                except: pass
                
            base = os.path.basename(target)
            search_term = target if "/" in target else base
            if search_term in ["bash", "sh", "env"]: return
            subprocess.run(["pkill", "-f", search_term])
            # Hizli tepki icin arayuzu aninda guncelle
            model[treeiter][11] = False
            self.btn_stop.set_sensitive(False)
        except Exception as e:
            pass

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

if __name__ == "__main__":
    app = AutostartManager()
    import sys
    if "--tray" in sys.argv:
        if not app.indicator: app.show_all()
    else: app.show_all()
    Gtk.main()
