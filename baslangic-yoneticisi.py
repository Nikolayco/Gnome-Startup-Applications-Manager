#!/usr/bin/env python3
import os
import glob
import shlex
import subprocess
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib, Gdk

AUTOSTART_DIR = os.path.expanduser("~/.config/autostart")
SYS_AUTOSTART_DIR = "/etc/xdg/autostart"

class AutostartApp:
    def __init__(self, filename, name, cmd, comment, hidden, is_sys, path, icon, terminal):
        self.filename = filename
        self.name = name
        self.cmd = cmd
        self.comment = comment
        self.hidden = hidden
        self.is_sys = is_sys
        self.path = path
        self.icon = icon
        self.terminal = terminal

class AppDialog(Gtk.Dialog):
    def __init__(self, parent, title, app=None):
        super().__init__(title=title, transient_for=parent, flags=Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT)
        self.set_default_size(500, 250)
        
        self.add_buttons("İptal", Gtk.ResponseType.CANCEL, "Kaydet", Gtk.ResponseType.OK)
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
        
        lbl_name = Gtk.Label(label="Uygulama Adı:", xalign=0)
        lbl_name.get_style_context().add_class("dim-label")
        grid.attach(lbl_name, 0, 0, 1, 1)
        self.entry_name = Gtk.Entry(placeholder_text="Örn: Yedekleme Scripti")
        self.entry_name.set_hexpand(True)
        grid.attach(self.entry_name, 1, 0, 1, 1)
        
        lbl_cmd = Gtk.Label(label="Çalıştırılacak Dosya:", xalign=0)
        lbl_cmd.get_style_context().add_class("dim-label")
        grid.attach(lbl_cmd, 0, 1, 1, 1)
        
        cmd_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.entry_cmd = Gtk.Entry(placeholder_text="Komut veya dosya yolu...")
        self.entry_cmd.set_hexpand(True)
        cmd_box.pack_start(self.entry_cmd, True, True, 0)
        
        btn_browse = Gtk.Button()
        btn_browse.add(Gtk.Image.new_from_icon_name("folder-open-symbolic", Gtk.IconSize.BUTTON))
        btn_browse.set_tooltip_text("Bilgisayardan dosya/script seç")
        btn_browse.connect("clicked", self.on_browse_clicked)
        cmd_box.pack_start(btn_browse, False, False, 0)
        grid.attach(cmd_box, 1, 1, 1, 1)
        
        lbl_comment = Gtk.Label(label="Açıklama (İsteğe):", xalign=0)
        lbl_comment.get_style_context().add_class("dim-label")
        grid.attach(lbl_comment, 0, 2, 1, 1)
        self.entry_comment = Gtk.Entry(placeholder_text="Ne işe yaradığını kısaca yazın...")
        grid.attach(self.entry_comment, 1, 2, 1, 1)

        self.check_terminal = Gtk.CheckButton(label="Terminalde (Ekranda) çalıştır")
        self.check_terminal.set_tooltip_text("İşaretlenirse, script siyah bir terminal penceresinde açılır.")
        grid.attach(self.check_terminal, 1, 3, 1, 1)
        
        if app:
            self.entry_name.set_text(app.name)
            self.entry_cmd.set_text(app.cmd)
            self.entry_comment.set_text(app.comment)
            self.check_terminal.set_active(app.terminal)
            
        self.show_all()

    def on_browse_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(title="Çalıştırılacak Dosyayı Seçin", parent=self, action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons("İptal", Gtk.ResponseType.CANCEL, "Seç", Gtk.ResponseType.OK)
        
        filter_all = Gtk.FileFilter()
        filter_all.set_name("Tüm Dosyalar")
        filter_all.add_pattern("*")
        dialog.add_filter(filter_all)
        
        filter_sh = Gtk.FileFilter()
        filter_sh.set_name("Script Dosyaları (.sh, .py, .pl)")
        filter_sh.add_pattern("*.sh")
        filter_sh.add_pattern("*.py")
        filter_sh.add_pattern("*.pl")
        dialog.add_filter(filter_sh)
        
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filepath = dialog.get_filename()
            if " " in filepath:
                self.entry_cmd.set_text(f'"{filepath}"')
            else:
                self.entry_cmd.set_text(filepath)
                
            if not self.entry_name.get_text().strip():
                name_no_ext = os.path.splitext(os.path.basename(filepath))[0]
                self.entry_name.set_text(name_no_ext.replace("-", " ").replace("_", " ").title())
            
            if filepath.endswith(".sh") or filepath.endswith(".py"):
                self.check_terminal.set_active(True)
                
        dialog.destroy()

class AutostartManager(Gtk.Window):
    def __init__(self):
        super().__init__(title="Başlangıç Uygulamaları Yöneticisi")
        self.set_default_size(850, 600)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_icon_name("preferences-system")
        self.current_selection = None

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.set_title(self.get_title())
        hb.set_subtitle("Sistem ve Kullanıcı uygulamalarını yönetin")
        self.set_titlebar(hb)

        btn_add = Gtk.Button()
        btn_add.add(Gtk.Image.new_from_icon_name("list-add-symbolic", Gtk.IconSize.BUTTON))
        btn_add.set_tooltip_text("Yeni uygulama veya script ekle")
        btn_add.connect("clicked", self.on_add_clicked)
        btn_add.get_style_context().add_class("suggested-action")
        hb.pack_start(btn_add)

        self.btn_remove = Gtk.Button()
        self.btn_remove.add(Gtk.Image.new_from_icon_name("user-trash-symbolic", Gtk.IconSize.BUTTON))
        self.btn_remove.set_tooltip_text("Seçili olanı listeden sil")
        self.btn_remove.connect("clicked", self.on_remove_clicked)
        self.btn_remove.get_style_context().add_class("destructive-action")
        self.btn_remove.set_sensitive(False)
        hb.pack_start(self.btn_remove)

        self.btn_edit = Gtk.Button()
        self.btn_edit.add(Gtk.Image.new_from_icon_name("document-edit-symbolic", Gtk.IconSize.BUTTON))
        self.btn_edit.set_tooltip_text("Ayarları düzenle")
        self.btn_edit.connect("clicked", self.on_edit_clicked)
        self.btn_edit.set_sensitive(False)
        hb.pack_start(self.btn_edit)

        self.btn_start = Gtk.Button()
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        box.pack_start(Gtk.Image.new_from_icon_name("media-playback-start-symbolic", Gtk.IconSize.BUTTON), False, False, 0)
        box.pack_start(Gtk.Label(label="Başlat"), False, False, 0)
        self.btn_start.add(box)
        self.btn_start.set_tooltip_text("Uygulamayı hemen çalıştırarak test et")
        self.btn_start.connect("clicked", self.on_start_clicked)
        self.btn_start.set_sensitive(False)
        hb.pack_end(self.btn_start)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(vbox)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        box_lists = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        box_lists.set_margin_start(10)
        box_lists.set_margin_end(10)
        box_lists.set_margin_top(15)
        box_lists.set_margin_bottom(15)
        
        lbl_user = Gtk.Label(xalign=0)
        lbl_user.set_markup("<span size='large' weight='bold' color='#2A7BDE'>Kullanıcı Uygulamaları</span>")
        box_lists.pack_start(lbl_user, False, False, 0)
        
        self.store_user = Gtk.ListStore(str, str, str, str, bool, str, str, bool)
        self.tree_user = self.create_treeview(self.store_user)
        box_lists.pack_start(self.tree_user, False, False, 0)
        
        box_lists.pack_start(Gtk.Separator(), False, False, 10)
        
        lbl_sys = Gtk.Label(xalign=0)
        lbl_sys.set_markup("<span size='large' weight='bold' color='#E35D5D'>Sistem Uygulamaları</span>")
        box_lists.pack_start(lbl_sys, False, False, 0)
        
        self.store_sys = Gtk.ListStore(str, str, str, str, bool, str, str, bool)
        self.tree_sys = self.create_treeview(self.store_sys)
        box_lists.pack_start(self.tree_sys, False, False, 0)
        
        scroll.add(box_lists)
        vbox.pack_start(scroll, True, True, 0)

        os.makedirs(AUTOSTART_DIR, exist_ok=True)
        self.load_apps()

    def create_treeview(self, model):
        tree = Gtk.TreeView(model=model)
        tree.set_rules_hint(True)
        tree.connect("row-activated", self.on_row_activated)
        
        selection = tree.get_selection()
        selection.connect("changed", self.on_selection_changed, tree)
        
        col_name = Gtk.TreeViewColumn("Uygulama Adı")
        col_name.set_resizable(True)
        col_name.set_expand(True)
        render_icon = Gtk.CellRendererPixbuf()
        render_icon.set_property("stock-size", Gtk.IconSize.DND)
        col_name.pack_start(render_icon, False)
        col_name.add_attribute(render_icon, "icon-name", 0)
        
        render_name = Gtk.CellRendererText()
        render_name.set_property("weight", 600)
        col_name.pack_start(render_name, True)
        col_name.add_attribute(render_name, "text", 1)
        tree.append_column(col_name)

        col_cmd = Gtk.TreeViewColumn("Dosya Yolu / Komut")
        col_cmd.set_resizable(True)
        col_cmd.set_expand(True)
        render_cmd = Gtk.CellRendererText()
        render_cmd.set_property("ellipsize", 3)
        render_cmd.set_property("foreground", "gray")
        col_cmd.pack_start(render_cmd, True)
        col_cmd.add_attribute(render_cmd, "text", 2)
        tree.append_column(col_cmd)
        
        col_term = Gtk.TreeViewColumn("Terminal")
        render_term = Gtk.CellRendererText()
        col_term.pack_start(render_term, False)
        col_term.set_cell_data_func(render_term, lambda col, cell, m, i, d: cell.set_property("text", "Evet" if m[i][7] else "Hayır"))
        tree.append_column(col_term)
        
        return tree

    def parse_desktop_file(self, path):
        name = os.path.basename(path).replace(".desktop", "")
        cmd, comment, hidden, icon, terminal = "", "", False, "application-x-executable", False
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("Name="): name = line.split("=", 1)[1]
                    elif line.startswith("Exec="): cmd = line.split("=", 1)[1]
                    elif line.startswith("Comment="): comment = line.split("=", 1)[1]
                    elif line.startswith("Icon="): icon = line.split("=", 1)[1]
                    elif line.lower().startswith("terminal=true"): terminal = True
                    elif line.startswith("Hidden=true") or line.startswith("X-GNOME-Autostart-enabled=false"):
                        hidden = True
        except: pass
        if "/" in icon: icon = "application-x-executable"
        return AutostartApp(os.path.basename(path), name, cmd, comment, hidden, path.startswith("/etc"), path, icon, terminal)

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
            if not app.hidden and app.cmd:
                all_apps.append(app)
                
        all_apps.sort(key=lambda x: x.name.lower())
                
        for app in all_apps:
            row = [app.icon, app.name, app.cmd, app.comment, app.is_sys, app.path, app.filename, app.terminal]
            if app.is_sys:
                self.store_sys.append(row)
            else:
                self.store_user.append(row)

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

    def write_desktop_file(self, filename, name, cmd, comment, terminal):
        path = os.path.join(AUTOSTART_DIR, filename)
        term_str = "true" if terminal else "false"
        content = f"[Desktop Entry]\nType=Application\nName={name}\nExec={cmd}\nComment={comment}\nIcon=application-x-executable\nTerminal={term_str}\nX-GNOME-Autostart-enabled=true\n"
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    def on_add_clicked(self, widget):
        dialog = AppDialog(self, "Yeni Başlangıç Öğesi Ekle")
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            name = dialog.entry_name.get_text()
            cmd = dialog.entry_cmd.get_text()
            comment = dialog.entry_comment.get_text()
            terminal = dialog.check_terminal.get_active()
            if name and cmd:
                filename = name.lower().replace(" ", "-").replace("/", "") + ".desktop"
                self.write_desktop_file(filename, name, cmd, comment, terminal)
                self.load_apps()
        dialog.destroy()

    def on_edit_clicked(self, widget):
        if not self.current_selection: return
        model, treeiter = self.current_selection
        path = model[treeiter][5]
        app = self.parse_desktop_file(path)
        
        dialog = AppDialog(self, "Öğeyi Düzenle", app)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            name = dialog.entry_name.get_text()
            cmd = dialog.entry_cmd.get_text()
            comment = dialog.entry_comment.get_text()
            terminal = dialog.check_terminal.get_active()
            if name and cmd:
                self.write_desktop_file(app.filename, name, cmd, comment, terminal)
                self.load_apps()
        dialog.destroy()

    def on_remove_clicked(self, widget):
        if not self.current_selection: return
        model, treeiter = self.current_selection
        filename = model[treeiter][6]
        is_sys = model[treeiter][4]
        user_path = os.path.join(AUTOSTART_DIR, filename)
        
        dialog = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.WARNING,
                                   buttons=Gtk.ButtonsType.YES_NO, text="Bu öğeyi başlangıçtan kaldırmak istiyor musunuz?")
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
        path = model[treeiter][5]
        
        try:
            app_info = Gio.DesktopAppInfo.new_from_filename(path)
            if app_info:
                context = Gdk.Display.get_default().get_app_launch_context()
                app_info.launch([], context)
            else:
                cmd = model[treeiter][2]
                cmd_clean = cmd.replace("%f", "").replace("%u", "").replace("%F", "").replace("%U", "")
                subprocess.Popen(shlex.split(cmd_clean), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
            d = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK, text="Uygulama/Script Başlatıldı!")
            d.run()
            d.destroy()
        except Exception as e:
            d = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK, text="Çalıştırma Hatası!")
            d.format_secondary_text(str(e))
            d.run()
            d.destroy()

if __name__ == "__main__":
    app = AutostartManager()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()
