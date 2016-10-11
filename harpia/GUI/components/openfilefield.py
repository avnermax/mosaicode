import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

import os

from harpia.GUI.components.field import Field
from harpia.GUI.fieldtypes import *


class OpenFileField(Field, Gtk.HBox):

    # --------------------------------------------------------------------------

    def __init__(self, data, event):
        if not isinstance(data, dict):
            return

        self.check_value(data, "name", "")
        self.check_value(data, "value", "")

        self.file = data["value"]
        self.parent_window = None
        Gtk.HBox.__init__(self, False)
        self.label = Gtk.Label(data["name"])
        self.label.set_property("halign", Gtk.Align.START)
        self.add(self.label)

        self.field = Gtk.Entry()
        self.field.set_text(self.file)
        if event != None:
            self.field.connect("changed", event)
        self.add(self.field)

        button = Gtk.Button.new_from_icon_name("gtk-file", Gtk.IconSize.BUTTON)
        button.connect("clicked", self.on_choose_file)
        self.add(button)
        self.show_all()

    # --------------------------------------------------------------------------
    def set_parent_window(self, widget):
        self.parent_window = widget

    # --------------------------------------------------------------------------
    def on_choose_file(self, widget):
        dialog = Gtk.FileChooserDialog("Open...",
                                       self.parent_window,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN,
                                        Gtk.ResponseType.OK)
                                       )
        current_dir = ""
        if os.path.isdir(self.field.get_text()):
            current_dir = self.field.get_text()
        else:
            current_dir = os.path.dirname(self.field.get_text())
        dialog.set_current_folder(current_dir)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.field.set_text(dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            pass
        dialog.destroy()

    # --------------------------------------------------------------------------
    def get_type(self):
        return HARPIA_OPEN_FILE

    # --------------------------------------------------------------------------
    def get_value(self):
        return self.field.get_text()

# --------------------------------------------------------------------------
