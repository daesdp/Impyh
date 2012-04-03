#!/usr/bin/python

#    <Impy comfortable screen capture.>
#    <2012>  <Por DaeS>

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Librerias
from gi.repository import Gtk, Gdk, GdkPixbuf
from gi.repository.GdkPixbuf import Pixbuf
import os

# Variables
user = os.path.expanduser("~")
v_logo ="icons/logo.png"
v_fl_impyh = user + "/.impyh"
v_mtmp = user + "/.impyh/.temp"
v_inter = GdkPixbuf.InterpType.BILINEAR

# Valida tiempo        
def val_time(v_time):
    try:
        v_vtime = int(v_time)
        if v_vtime <= 0:
            v_ntime = 1
        else:
           v_ntime = int(v_time)
    except:
        v_ntime = 1
    return v_ntime

# Limpia carpeta temporal
def val_foler():
    if os.path.isdir(v_mtmp):
        os.system("rm -fr " + v_mtmp)
    os.system("mkdir " + v_mtmp)

# Obtiene nombre nueva imagen
def val_count():
    global v_count
    try:
        v_count = v_count + 1
    except:
        v_count = 1
    v_scount = str(v_count)    
    v_new_img = v_mtmp + "/" + v_scount + ".png"
    return v_new_img

# Obtiene nombre actual imagen
def val_old_count():
    v_scount = str(v_count)    
    v_old_img = v_mtmp + "/" + v_scount + ".png"
    return v_old_img

class main:

    # Ventana de trabajo Principal
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("main.ui")
        self.m_windows = builder.get_object("window_main")
        self.image = builder.get_object("image")
        self.seg_img = builder.get_object("seg_entry")
        self.dg_save = builder.get_object("dialog_save")
        self.dg_about = builder.get_object("aboutdialog")
        self.a_save = builder.get_object("save")
        self.a_msave = builder.get_object("menu_save")
        self.a_zminc = builder.get_object("zoom_inc")
        self.a_zmdec = builder.get_object("zoom_dec")
        self.a_zmori = builder.get_object("zoom_ori")
        self.a_zmbest = builder.get_object("zoom_best")
        self.tray_menu = builder.get_object("popmenu")
        self.view_port = builder.get_object("viewport2")
        self.view_port_img = builder.get_object("viewport1")

        # Conector tray icon menu
        self.tray_pyh = builder.get_object("statusicon")
        self.tray_pyh.connect("popup_menu", self.pop_menu)
        self.v_status_tray = True
        
        # Senales
        dict = {"onclik_area": self.imp_area,
                "onclik_pant": self.imp_pant,
                "onclik_zm_inc": self.inc_zoom,
                "onclik_zm_dec": self.dec_zoom,
                "onclik_zmorig": self.orig_zoom,
                "onclik_zmbest": self.best_zoom,
                "onclik_about": self.show_about,
                "onclik_save": self.show_save,
                "onclik_exit": self.app_exit,
                "onclik_tray": self.click_tray}
        builder.connect_signals(dict)

        # Conf window main
        self.m_windows.set_size_request(650,400)
        self.a_save.set_sensitive(False)
        self.a_msave.set_sensitive(False)
        self.a_zminc.set_sensitive(False)
        self.a_zmdec.set_sensitive(False)
        self.a_zmori.set_sensitive(False)
        self.a_zmbest.set_sensitive(False)

        # Crea carpetas
        if os.path.isdir(v_fl_impyh):
            None
        else:
            os.system("mkdir " + v_fl_impyh)
        val_foler()

        # carga logo
        impyh_logo = Pixbuf.new_from_file(v_logo)
        self.image.set_from_pixbuf(impyh_logo)
        self.image.show()

        # Lista imagenes
        self.liststore = Gtk.ListStore(str)
        treeview = Gtk.TreeView()
        treeview.set_model(self.liststore)
        self.view_port.add(treeview)
        treeview.append_column(Gtk.TreeViewColumn("Imagenes", Gtk.CellRendererText(), text=0))
        self.m_windows.show_all()
        
        # Conector vista previa
        self.liststore.connect("row-changed", self.imp_prev)
        
        # Conector select
        selection = treeview.get_selection()
        selection.connect("changed", self.slct_item)
        
    # Genera imagen area
    def imp_area(self,widget):
        new_cap = val_count()
        os.system("scrot -s " + new_cap)
        self.a_save.set_sensitive(True)
        self.a_msave.set_sensitive(True)
        self.a_zminc.set_sensitive(True)
        self.a_zmdec.set_sensitive(True)
        self.a_zmori.set_sensitive(True)
        self.a_zmbest.set_sensitive(True)

        # Actualiza lista imagenes
        if os.path.isfile(new_cap):
            v_num_cap = str(v_count)
            self.liststore.append(["Captura " + v_num_cap])
            self.m_windows.show_all()

    # Genera imagen completa
    def imp_pant(self,widget):
        v_time = self.seg_img.get_text()
        f_stime = str(val_time(v_time))
        new_cap = val_count()
        os.system("scrot -d " + f_stime + " " + new_cap)
        self.a_save.set_sensitive(True)
        self.a_msave.set_sensitive(True)
        self.a_zminc.set_sensitive(True)
        self.a_zmdec.set_sensitive(True)
        self.a_zmori.set_sensitive(True)
        self.a_zmbest.set_sensitive(True)

        # Actualiza lista imagenes
        if os.path.isfile(new_cap):
            v_num_cap = str(v_count)
            self.liststore.append(["Captura " + v_num_cap])
            self.m_windows.show_all()

    # Vista previa
    def imp_prev(self, liststore, path, iter):
        if self.v_status_tray == False:
            self.v_status_tray = True

        v_item_val = self.liststore.get_value(iter, 0)
        self.v_item_actual = val_old_count()
        pixbuf = Pixbuf.new_from_file(self.v_item_actual)
        ancho_pixbuf = pixbuf.get_width()
        alto_pixbuf = pixbuf.get_height()
        prev_pixbuf = pixbuf.scale_simple(ancho_pixbuf, alto_pixbuf, v_inter)
        self.image.set_from_pixbuf(prev_pixbuf)
        self.image.show()

    # Seleciona item
    def slct_item(self, selection):
        model, tree_iter = selection.get_selected()
        v_item_val = model.get_value(tree_iter, 0)
        v_num = v_item_val[8:99]
        self.v_item_actual = v_mtmp + "/" + v_num + ".png"
        pixbuf = Pixbuf.new_from_file(self.v_item_actual)
        ancho_pixbuf = pixbuf.get_width()
        alto_pixbuf = pixbuf.get_height()
        prev_pixbuf = pixbuf.scale_simple(ancho_pixbuf, alto_pixbuf, v_inter)
        self.image.set_from_pixbuf(prev_pixbuf)
        self.image.show()

    # Aumnta zoom
    def inc_zoom(self,widget):
        pixbuf = Pixbuf.new_from_file(self.v_item_actual)
        ancho_pixbuf = pixbuf.get_width() *1.5
        alto_pixbuf = pixbuf.get_height() *1.5
        prev_pixbuf = pixbuf.scale_simple(ancho_pixbuf, alto_pixbuf, v_inter)
        self.image.set_from_pixbuf(prev_pixbuf)
        self.image.show()

    # Disminuye zoom
    def dec_zoom(self,widget):
        pixbuf = Pixbuf.new_from_file(self.v_item_actual)
        ancho_pixbuf = pixbuf.get_width() /1.5
        alto_pixbuf = pixbuf.get_height() /1.5
        prev_pixbuf = pixbuf.scale_simple(ancho_pixbuf, alto_pixbuf, v_inter)
        self.image.set_from_pixbuf(prev_pixbuf)
        self.image.show()

    # Zoom original
    def orig_zoom(self,widget):
        pixbuf = Pixbuf.new_from_file(self.v_item_actual)
        ancho_pixbuf = pixbuf.get_width()
        alto_pixbuf = pixbuf.get_height()
        prev_pixbuf = pixbuf.scale_simple(ancho_pixbuf, alto_pixbuf, v_inter)
        self.image.set_from_pixbuf(prev_pixbuf)
        self.image.show()

    # Zoom automatico
    def best_zoom(self,widget):
        rect = self.view_port_img.get_allocation()
        pixbuf = Pixbuf.new_from_file(self.v_item_actual)
        ancho_pixbuf = pixbuf.get_width()
        alto_pixbuf = pixbuf.get_height()

        if ancho_pixbuf > alto_pixbuf:
            base = ancho_pixbuf - rect.width
            ancho = int(rect.width - 6)
            relacion = (alto_pixbuf*100 - 6)/ancho_pixbuf
            alto = int(ancho * relacion/100)
        else:
            base = alto_pixbuf - rect.height
            alto = int(rect.height - 6)
            relacion = (ancho_pixbuf*100 - 6)/alto_pixbuf
            ancho = int(alto * (relacion/100))
        
        prev_pixbuf = pixbuf.scale_simple(ancho, alto, v_inter)    
        self.image.set_from_pixbuf(prev_pixbuf)    
        self.image.show()

    # Muestra about
    def show_about(self,widget):
        self.dg_about.run()
        self.dg_about.hide()

    # Guarda imagen
    def show_save(self,widget):
        v_valida = self.dg_save.run()
        self.dg_save.hide()
        
        if v_valida == -5:
            v_urlimg = self.dg_save.get_filename()
            os.system("cp " + self.v_item_actual + " " + v_urlimg)

    # Sale del programa
    def app_exit(self,widget):
        val_foler()
        Gtk.main_quit()
    
    # Minimizar a tray icon
    def click_tray(self,widget):
        if self.v_status_tray == True:
            self.m_windows.hide()
            self.v_status_tray = False
        else:
            self.m_windows.show()
            self.v_status_tray = True

    # Menu tray icon
    def pop_menu(self,widget,button,time,data=None ):
        self.tray_menu.show_all()
        self.tray_menu.popup(None,None,None,None, 3,time)

# Ejecucion del programa
if __name__ == "__main__":
    main()
    Gtk.main()
