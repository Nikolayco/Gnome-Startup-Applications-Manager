#!/usr/bin/env python3
import os
import glob
import shlex
import subprocess
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib

AUTOSTART_DIR = os.path.expanduser("~/.config/autostart")
SYS_AUTOSTART_DIR = "/etc/xdg/autostart"

class AutostartApp:
    def __init__(self, filename, name, cmd, comment, hidden, is_sys, path, icon):
        self.filename = filename
        self.name = name
        self.cmd = cmd
        self.comment = comment
        self.hidden = hidden
        self.is_sys = is_sys
        self.path = path
        self.icon = icon

class AppDialog(Gtk.Dialog):
    def __init__(self, parent, title, app=None):
        super().__init__(title=title, transient_for=parent, flags=Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT)
        self.set_default_size(450, 200)
        
        self.add_buttons(
            "İptal", Gtk.ResponseType.CANCEL,
            "Kaydet", Gtk.ResponseType.OK
        )
        # Style the save button
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
        
        # Name
        lbl_name = Gtk.Label(label="Uygulama Adı:", xalign=0)
        lbl_name.get_style_context().add_class("dim-label")
        grid.attach(lbl_name, 0, 0, 1, 1)
        self.entry_name = Gtk.Entry(placeholder_text="Örn: Yedekleme Scripti")
        self.entry_name.set_hexpand(True)
        grid.attach(self.entry_name, 1, 0, 1, 1)
        
        # Command / Browse
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
        
        # Comment
        lbl_comment = Gtk.Label(label="Açıklama (İsteğe Bağlı):", xalign=0)
        lbl_comment.get_style_context().add_class("dim-label")
        grid.attach(lbl_comment, 0, 2, 1, 1)
        self.entry_comment = Gtk.Entry(placeholder_text="Ne işe yaradığını kısaca yazın...")
        grid.attach(self.entry_comment, 1, 2, 1, 1)
        
        if app:
            self.entry_name.set_text(app.name)
            self.entry_cmd.set_text(app.cmd)
            self.entry_comment.set_text(app.comment)
            
        self.show_all()

    def on_browse_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Çalıştırılacak Dosyayı veya Scripti Seçin",
            parent=self,
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons("İptal", Gtk.ResponseType.CANCEL, "Seç", Gtk.ResponseType.OK)
        
        # Filter for scripts/executables
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
                filepath = f'"{filepath}"'
            self.entry_cmd.set_text(filepath)
        dialog.destroy()

class AutostartManager(Gtk.Window):
    def __init__(self):
        super().__init__(title="Başlangıç Uygulamaları Yöneticisi")
        self.set_default_size(800, 550)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_icon_name("preferences-system")

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.set_title(self.get_title())
        hb.set_subtitle("Uygulama ve scriptlerinizi görsel olarak yönetin")
        self.set_titlebar(hb)

        btn_add = Gtk.Button()
        btn_add.add(Gtk.Image.new_from_icon_name("list-add-symbolic", Gtk.IconSize.BUTTON))
        btn_add.set_tooltip_text("Sistem başlangıcına yeni uygulama veya script ekle")
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
        self.btn_edit.set_tooltip_text("Seçili olanın ayarlarını düzenle")
        self.btn_edit.connect("clicked", self.on_edit_clicked)
        self.btn_edit.set_sensitive(False)
        hb.pack_start(self.btn_edit)

        self.btn_start = Gtk.Button()
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        box.pack_start(Gtk.Image.new_from_icon_name("media-playback-start-symbolic", Gtk.IconSize.BUTTON), False, False, 0)
        box.pack_start(Gtk.Label(label="Başlat"), False, False, 0)
        self.btn_start.add(box)
        self.btn_start.set_tooltip_text("Seçili uygulamayı hemen çalıştırarak test et")
        self.btn_start.connect("clicked", self.on_start_clicked)
        self.btn_start.set_sensitive(False)
        hb.pack_end(self.btn_start)

        # Main view
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(vbox)

        # ListStore: Icon, Name, Command, Comment, IsSys, FilePath, Filename
        self.liststore = Gtk.ListStore(str, str, str, str, str, str, str) 
        self.treeview = Gtk.TreeView(model=self.liststore)
        self.treeview.set_hexpand(True)
        self.treeview.set_vexpand(True)
        self.treeview.set_rules_hint(True) # zebra stripes
        self.treeview.set_margin_top(5)
        
        selection = self.treeview.get_selection()
        selection.connect("changed", self.on_selection_changed)

        # Column 0: App Name with Icon
        col_name = Gtk.TreeViewColumn("Uygulama Adı")
        col_name.set_sort_column_id(1)
        col_name.set_resizable(True)
        col_name.set_expand(True)
        
        render_icon = Gtk.CellRendererPixbuf()
        render_icon.set_property("stock-size", Gtk.IconSize.DND) # Large icons
        col_name.pack_start(render_icon, False)
        col_name.add_attribute(render_icon, "icon-name", 0)
        
        render_name = Gtk.CellRendererText()
        render_name.set_property("weight", 600) # Bold names
        col_name.pack_start(render_name, True)
        col_name.add_attribute(render_name, "text", 1)
        self.treeview.append_column(col_name)

        # Column 1: Command
        col_cmd = Gtk.TreeViewColumn("Dosya Yolu / Komut")
        col_cmd.set_resizable(True)
        col_cmd.set_expand(True)
        render_cmd = Gtk.CellRendererText()
        render_cmd.set_property("ellipsize", 3) # END ellipsize
        render_cmd.set_property("foreground", "gray")
        col_cmd.pack_start(render_cmd, True)
        col_cmd.add_attribute(render_cmd, "text", 2)
        self.treeview.append_column(col_cmd)
        
        # Column 2: System/User
        col_sys = Gtk.TreeViewColumn("Konum")
        render_sys = Gtk.CellRendererText()
        col_sys.pack_start(render_sys, True)
        col_sys.add_attribute(render_sys, "text", 4)
        self.treeview.append_column(col_sys)

        scroll = Gtk.ScrolledWindow()
        scroll.add(self.treeview)
        vbox.pack_start(scroll, True, True, 0)

        os.makedirs(AUTOSTART_DIR, exist_ok=True)
        self.load_apps()

    def parse_desktop_file(self, path):
        name = os.path.basename(path).replace(".desktop", "")
        cmd, comment, hidden, icon = "", "", False, "application-x-executable"
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("Name="): name = line.split("=", 1)[1]
                    elif line.startswith("Exec="): cmd = line.split("=", 1)[1]
                    elif line.startswith("Comment="): comment = line.split("=", 1)[1]
                    elif line.startswith("Icon="): icon = line.split("=", 1)[1]
                    elif line.startswith("Hidden=true") or line.startswith("X-GNOME-Autostart-enabled=false"):
                        hidden = True
        except: pass
        # Fallback to default icon if path-based icon fails to load via icon-name
        if "/" in icon:
            icon = "application-x-executable"
        return AutostartApp(os.path.basename(path), name, cmd, comment, hidden, path.startswith("/etc"), path, icon)

    def load_apps(self):
        self.liststore.clear()
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
                    
        for fname, path in seen.items():
            app = self.parse_desktop_file(path)
            if not app.hidden and app.cmd:
                self.liststore.append([app.icon, app.name, app.cmd, app.comment, "Sistem" if app.is_sys else "Kullanıcı", app.path, app.filename])

    def on_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        has_sel = treeiter is not None
        self.btn_start.set_sensitive(has_sel)
        self.btn_remove.set_sensitive(has_sel)
        self.btn_edit.set_sensitive(has_sel)

    def write_desktop_file(self, filename, name, cmd, comment):
        path = os.path.join(AUTOSTART_DIR, filename)
        content = f"[Desktop Entry]\nType=Application\nName={name}\nExec={cmd}\nComment={comment}\nIcon=application-x-executable\nX-GNOME-Autostart-enabled=true\n"
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    def on_add_clicked(self, widget):
        dialog = AppDialog(self, "Yeni Başlangıç Öğesi Ekle")
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            name = dialog.entry_name.get_text()
            cmd = dialog.entry_cmd.get_text()
            comment = dialog.entry_comment.get_text()
            if name and cmd:
                filename = name.lower().replace(" ", "-").replace("/", "") + ".desktop"
                self.write_desktop_file(filename, name, cmd, comment)
                self.load_apps()
        dialog.destroy()

    def on_edit_clicked(self, widget):
        model, treeiter = self.treeview.get_selection().get_selected()
        if treeiter is None: return
        
        path = model[treeiter][5]
        app = self.parse_desktop_file(path)
        
        dialog = AppDialog(self, "Öğeyi Düzenle", app)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            name = dialog.entry_name.get_text()
            cmd = dialog.entry_cmd.get_text()
            comment = dialog.entry_comment.get_text()
            if name and cmd:
                self.write_desktop_file(app.filename, name, cmd, comment)
                self.load_apps()
        dialog.destroy()

    def on_remove_clicked(self, widget):
        model, treeiter = self.treeview.get_selection().get_selected()
        if treeiter is None: return
        
        filename = model[treeiter][6]
        is_sys = model[treeiter][4] == "Sistem"
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
        model, treeiter = self.treeview.get_selection().get_selected()
        if treeiter is None: return
        cmd = model[treeiter][2]
        try:
            cmd_clean = cmd.replace("%f", "").replace("%u", "").replace("%F", "").replace("%U", "")
            subprocess.Popen(shlex.split(cmd_clean), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            d = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK, text="Uygulama/Script Başlatıldı!")
            d.format_secondary_text(f"Komut: {cmd_clean}")
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
