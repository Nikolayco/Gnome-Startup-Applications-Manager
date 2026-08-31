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

        # Terminal and Size Box
        lbl_term = Gtk.Label(label=_("Pencere Modu:"), xalign=0)
        lbl_term.get_style_context().add_class("dim-label")
        grid.attach(lbl_term, 0, 3, 1, 1)

        term_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        self.check_terminal = Gtk.CheckButton(label=_("Terminalde çalıştır"))
        term_box.pack_start(self.check_terminal, False, False, 0)
        
        self.combo_term_size = Gtk.ComboBoxText()
        self.combo_term_size.append("normal", _("Normal"))
        self.combo_term_size.append("maximize", _("Maximize (Tam Ekran)"))
        self.combo_term_size.append("minimize", _("Minimize (Küçültülmüş)"))
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
        self.set_default_size(900, 650)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_icon_name(APP_ICON)
        self.current_selection = None
        
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
            btn_tray = Gtk.Button()
            btn_tray.add(Gtk.Image.new_from_icon_name("go-down-symbolic", Gtk.IconSize.BUTTON))
            btn_tray.set_tooltip_text(_("Arka planda (Tray) çalışmaya devam et"))
            btn_tray.connect("clicked", lambda w: self.hide())
            hb.pack_end(btn_tray)

        self.btn_remove = Gtk.Button()
        self.btn_remove.add(Gtk.Image.new_from_icon_name("user-trash-symbolic", Gtk.IconSize.BUTTON))
        self.btn_remove.set_tooltip_text(_("Kalıcı olarak sil"))
        self.btn_remove.connect("clicked", self.on_remove_clicked)
        self.btn_remove.get_style_context().add_class("destructive-action")
        self.btn_remove.set_sensitive(False)
        hb.pack_end(self.btn_remove)

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

        btn_add = Gtk.Button()
        btn_add.add(Gtk.Image.new_from_icon_name("list-add-symbolic", Gtk.IconSize.BUTTON))
        btn_add.set_tooltip_text(_("Yeni uygulama veya script ekle"))
        btn_add.connect("clicked", self.on_add_clicked)
        btn_add.get_style_context().add_class("suggested-action")
        hb.pack_end(btn_add)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(vbox)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        box_lists = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        box_lists.set_margin_start(10)
        box_lists.set_margin_end(10)
        box_lists.set_margin_top(15)
        box_lists.set_margin_bottom(15)
        
        # Data Model: 0:Icon, 1:Enabled, 2:Name, 3:Cmd, 4:Comment, 5:IsSys, 6:Path, 7:Filename, 8:Terminal, 9:Delay, 10:TermSize, 11:IsRunning
        self.store_user = Gtk.ListStore(str, bool, str, str, str, bool, str, str, bool, int, str, bool)
        self.filter_user = self.store_user.filter_new()
        self.filter_user.set_visible_func(self.filter_func)
        
        lbl_user = Gtk.Label(xalign=0)
        lbl_user.set_markup(_("<span size='large' weight='bold' color='#2A7BDE'>Kullanıcı Uygulamaları</span>"))
        box_lists.pack_start(lbl_user, False, False, 0)
        
        self.tree_user = self.create_treeview(self.filter_user)
        box_lists.pack_start(self.tree_user, False, False, 0)
        
        box_lists.pack_start(Gtk.Separator(), False, False, 10)
        
        self.store_sys = Gtk.ListStore(str, bool, str, str, str, bool, str, str, bool, int, str, bool)
        self.filter_sys = self.store_sys.filter_new()
        self.filter_sys.set_visible_func(self.filter_func)
        
        lbl_sys = Gtk.Label(xalign=0)
        lbl_sys.set_markup(_("<span size='large' weight='bold' color='#E35D5D'>Sistem Uygulamaları</span>"))
        box_lists.pack_start(lbl_sys, False, False, 0)
        
        self.tree_sys = self.create_treeview(self.filter_sys)
        box_lists.pack_start(self.tree_sys, False, False, 0)
        
        scroll.add(box_lists)
        vbox.pack_start(scroll, True, True, 0)

        os.makedirs(AUTOSTART_DIR, exist_ok=True)
        os.makedirs(CUSTOM_SCRIPTS_DIR, exist_ok=True)
        
        self.load_apps()
        self.setup_tray()
        self.connect("delete-event", self.on_delete_event)
        self.refresh_status()
        GLib.timeout_add_seconds(3, self.refresh_status)

    def refresh_status(self):
        try:
            import subprocess
            res = subprocess.run(["ps", "-eo", "args"], stdout=subprocess.PIPE, text=True)
            all_procs = res.stdout
        except:
            all_procs = ""

        def is_running(cmd):
            import shlex, os
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
                base = os.path.basename(target)
                search_term = target if "/" in target else base
                if search_term in ["bash", "sh", "env"]: return False
                return search_term in all_procs
            except:
                return False

        for row in self.store_user:
            row[11] = is_running(row[3])
        for row in self.store_sys:
            row[11] = is_running(row[3])
            
        return True

    def on_delete_event(self, widget, event):
        Gtk.main_quit()
        return False

    def setup_tray(self):
        self.indicator = None
        if AppIndicator3:
            self.indicator = AppIndicator3.Indicator.new(
                "gnome-startup-manager-indicator",
                APP_ICON,
                AppIndicator3.IndicatorCategory.APPLICATION_STATUS
            )
            self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
            self.indicator.set_title(_("Başlangıç Uygulamaları Yöneticisi"))
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
            app_name = row[2]
            app_cmd = row[3]
            item = Gtk.MenuItem(label=app_name)
            item.connect("activate", self.on_tray_execute, app_cmd)
            menu.append(item)
            
        if count == 0:
            empty = Gtk.MenuItem(label=_("Uygulama bulunamadı"))
            empty.set_sensitive(False)
            menu.append(empty)
            
        menu.append(Gtk.SeparatorMenuItem())
        
        item_show = Gtk.MenuItem(label=_("⚙️ Yöneticiyi Aç"))
        item_show.connect("activate", lambda w: self.present())
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
            if not m[i][8]:
                cell.set_property("text", _("-"))
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
        is_enabled = not filter_model[treeiter][1]
        
        filename = filter_model[treeiter][7]
        name = filter_model[treeiter][2]
        cmd = filter_model[treeiter][3]
        comment = filter_model[treeiter][4]
        terminal = filter_model[treeiter][8]
        delay = filter_model[treeiter][9]
        term_size = filter_model[treeiter][10]
        
        self.write_desktop_file(filename, name, cmd, comment, terminal, term_size, delay, is_enabled)
        self.load_apps()

    def parse_desktop_file(self, path):
        name = os.path.basename(path).replace(".desktop", "")
        cmd, comment, hidden, icon, terminal, delay = "", "", False, "application-x-executable", False, 0
        term_size = "normal"
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
        if "/" in icon: icon = "application-x-executable"
        
        # Check if it was wrapped by our maximize logic
        if cmd.startswith("gnome-terminal --maximize -- "):
            cmd = cmd.replace("gnome-terminal --maximize -- ", "")
            term_size = "maximize"
            terminal = True
        prefix_min = 'gnome-terminal -- bash -c "xdotool getactivewindow windowminimize; '
        if cmd.startswith(prefix_min) and cmd.endswith('"'):
            cmd = cmd[len(prefix_min):-1]
            term_size = "minimize"
            terminal = True
            
        return AutostartApp(os.path.basename(path), name, cmd, comment, hidden, path.startswith("/etc"), path, icon, terminal, delay, term_size)

    def load_apps(self):
        self.store_user.clear()
        self.store_sys.clear()
        
        paths = []
        if os.path.exists(AUTOSTART_DIR):
            paths.extend(glob.glob(os.path.join(AUTOSTART_DIR, "*.desktop")))
        if os.path.exists(SYS_AUTOSTART_DIR):
            paths.extend(glob.glob(os.path.join(SYS_AUTOSTART_DIR, "*.desktop")))
            
        seen = {}
        for p in paths:
            fname = os.path.basename(p)
            if fname not in seen:
                user_path = os.path.join(AUTOSTART_DIR, fname)
                seen[fname] = user_path if os.path.exists(user_path) else p
                    
        all_apps = []
        for fname, path in seen.items():
            app = self.parse_desktop_file(path)
            if app.cmd:
                all_apps.append(app)
                
        all_apps.sort(key=lambda x: x.name.lower())
                
        for app in all_apps:
            row = [app.icon, app.enabled, app.name, app.cmd, app.comment, app.is_sys, app.path, app.filename, app.terminal, app.delay, app.term_size, False]
            if app.is_sys:
                self.store_sys.append(row)
            else:
                self.store_user.append(row)
                
        if hasattr(self, 'indicator'):
            self.update_tray_menu()

    def on_selection_changed(self, selection, treeview):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            other_tree = self.tree_sys if treeview == self.tree_user else self.tree_user
            other_tree.get_selection().unselect_all()
            
            self.current_selection = (model, treeiter)
            self.btn_start.set_sensitive(True)
            self.btn_remove.set_sensitive(True)
            self.btn_edit.set_sensitive(True)
        else:
            if not self.tree_user.get_selection().get_selected()[1] and \
               not self.tree_sys.get_selection().get_selected()[1]:
                self.current_selection = None
                self.btn_start.set_sensitive(False)
                self.btn_remove.set_sensitive(False)
                self.btn_edit.set_sensitive(False)

    def on_row_activated(self, treeview, path, column):
        self.on_edit_clicked(None)

    def write_desktop_file(self, filename, name, cmd, comment, terminal, term_size, delay, enabled):
        path = os.path.join(AUTOSTART_DIR, filename)
        
        final_cmd = cmd
        term_str = "false"
        
        if terminal:
            if term_size == "maximize":
                final_cmd = f"gnome-terminal --maximize -- {cmd}"
            elif term_size == "minimize":
                final_cmd = f'gnome-terminal -- bash -c "xdotool getactivewindow windowminimize; {cmd}"'
            else:
                term_str = "true"
                
        en_str = "true" if enabled else "false"
        hidden_str = "false" if enabled else "true"
        
        content = f"[Desktop Entry]\nType=Application\nName={name}\nExec={final_cmd}\nComment={comment}\nIcon=application-x-executable\nTerminal={term_str}\nHidden={hidden_str}\nX-GNOME-Autostart-enabled={en_str}\n"
        if delay > 0:
            content += f"X-GNOME-Autostart-Delay={delay}\n"
            
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    def save_custom_script(self, filename, code):
        script_path = os.path.join(CUSTOM_SCRIPTS_DIR, filename.replace('.desktop', '.sh'))
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write("#!/usr/bin/env bash\n" + code + "\n")
        os.chmod(script_path, 0o755)
        return script_path

    def on_add_clicked(self, widget):
        dialog = AppDialog(self, _("Yeni Başlangıç Öğesi Ekle"))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            name = dialog.entry_name.get_text()
            comment = dialog.entry_comment.get_text()
            terminal = dialog.check_terminal.get_active()
            term_size = dialog.combo_term_size.get_active_id()
            delay = int(dialog.spin_delay.get_value())
            
            visible_tab = dialog.stack.get_visible_child_name()
            if visible_tab == "file":
                cmd = dialog.entry_cmd.get_text()
            else:
                buf = dialog.text_buffer
                code = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True).strip()
                if code:
                    filename = name.lower().replace(" ", "-").replace("/", "") + ".desktop"
                    cmd = self.save_custom_script(filename, code)
                else:
                    cmd = ""

            if name and cmd:
                filename = name.lower().replace(" ", "-").replace("/", "") + ".desktop"
                self.write_desktop_file(filename, name, cmd, comment, terminal, term_size, delay, True)
                self.load_apps()
        dialog.destroy()

    def on_edit_clicked(self, widget):
        if not self.current_selection: return
        model, treeiter = self.current_selection
        path = model[treeiter][6]
        app = self.parse_desktop_file(path)
        
        dialog = AppDialog(self, _("Öğeyi Düzenle"), app)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            name = dialog.entry_name.get_text()
            comment = dialog.entry_comment.get_text()
            terminal = dialog.check_terminal.get_active()
            term_size = dialog.combo_term_size.get_active_id()
            delay = int(dialog.spin_delay.get_value())
            
            visible_tab = dialog.stack.get_visible_child_name()
            if visible_tab == "file":
                cmd = dialog.entry_cmd.get_text()
            else:
                buf = dialog.text_buffer
                code = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True).strip()
                if code:
                    cmd = self.save_custom_script(app.filename, code)
                else:
                    cmd = app.cmd
                    
            if name and cmd:
                self.write_desktop_file(app.filename, name, cmd, comment, terminal, term_size, delay, app.enabled)
                self.load_apps()
        dialog.destroy()

    def on_remove_clicked(self, widget):
        if not self.current_selection: return
        model, treeiter = self.current_selection
        filename = model[treeiter][7]
        is_sys = model[treeiter][5]
        user_path = os.path.join(AUTOSTART_DIR, filename)
        
        dialog = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.WARNING,
                                   buttons=Gtk.ButtonsType.YES_NO, text=_("Bu öğeyi KALICI OLARAK silmek istiyor musunuz?\\nGeçici olarak durdurmak için listeden 'Aktif' tikini kaldırabilirsiniz."))
        response = dialog.run()
        dialog.destroy()
        
        if response == Gtk.ResponseType.YES:
            if is_sys:
                with open(user_path, 'w', encoding='utf-8') as f:
                    f.write(f"[Desktop Entry]\nHidden=true\nX-GNOME-Autostart-enabled=false\n")
            else:
                if os.path.exists(user_path):
                    os.remove(user_path)
            self.load_apps()

    def on_start_clicked(self, widget):
        if not self.current_selection: return
        model, treeiter = self.current_selection
        path = model[treeiter][6]
        
        try:
            app_info = Gio.DesktopAppInfo.new_from_filename(path)
            if app_info:
                context = Gdk.Display.get_default().get_app_launch_context()
                app_info.launch([], context)
            else:
                cmd = model[treeiter][3]
                cmd_clean = cmd.replace("%f", "").replace("%u", "").replace("%F", "").replace("%U", "")
                subprocess.Popen(shlex.split(cmd_clean), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
            d = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK, text=_("Uygulama/Script Başlatıldı!"))
            d.run()
            d.destroy()
        except Exception as e:
            d = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK, text=_("Çalıştırma Hatası!"))
            d.format_secondary_text(str(e))
            d.run()
            d.destroy()

if __name__ == "__main__":
    app = AutostartManager()
    import sys
    if "--tray" in sys.argv:
        if app.indicator:
            pass
        else:
            app.show_all()
    else:
        app.show_all()
        
    Gtk.main()
