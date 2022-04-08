###############################################################################################################
#    About.py   Copyright (C) <2022>  <Kevin Scott>                                                           #                                                                                                             #                                                                                                             #
#    Display a simple about dialog.                  .                                                        #
#                                                                                                             #
#     For changes see history.txt                                                                             #
#                                                                                                             #
###############################################################################################################
#    Copyright (C) <2022>  <Kevin Scott>                                                                      #
#                                                                                                             #
#    This program is free software: you can redistribute it and/or modify it under the terms of the           #
#    GNU General Public License as published by the Free Software Foundation, either Version 3 of the         #
#    License, or (at your option) any later Version.                                                          #
#                                                                                                             #
#    This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without        #
#    even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
#    GNU General Public License for more details.                                                             #
#                                                                                                             #
#    You should have received a copy of the GNU General Public License along with this program.               #
#    If not, see <http://www.gnu.org/licenses/>.                                                              #
#                                                                                                             #
###############################################################################################################

import tkinter as tk
import tkinter.ttk as ttk

import pathlib

import pygubu

from src.projectPaths import *
import src.utils.fonts_utils as fu

class Font():
    """  A Simple about dialog.
         Just displays the product name and version and a copyright notice.

         Create with:  myFont = Font.Font(self.mainwindow)
         Display with: myFont.show_font_dialog()
    """

    def __init__(self, parent, logger):
        self.row = -1
        self.parent = parent
        self.logger = logger
        self.font_dialog = None

        self.builder = builder = pygubu.Builder()

        # Load an ui file
        builder.add_from_file(PROJECT_UI)

    def show_font_dialog(self):
        if self.font_dialog is None:
            self.dialog = self.builder.get_object('dlg_fonts', self.parent)
            self.font_dialog = self.dialog
            self.font_dialog.set_modal("true")

            self.mylistbox = lbox = self.builder.get_object('lst_fonts')

            btnclose = self.builder.get_object('font_btnclose')
            btnclose['command'] = self.dialog_btnclose_clicked

            btnclose = self.builder.get_object('font_btnok')
            btnclose['command'] = self.dialog_btnok_clicked

            self.display_fonts()
            self.dialog.run()
        else:
            self.font_dialog.show()


    def dialog_btnclose_clicked(self):
        self.dialog.close()

    def dialog_btnok_clicked(self):
        self.row = self.mylistbox.curselection()[0]  #  This return a tuple, which must only contain 1 element.
                                                     #  List box has selectmode set to single.
        self.dialog.close()


    def display_fonts(self):
        """  Populates the listbox with a list of fonts.
        """
        fu.check_font()
        self.mylistbox.select_clear(tk.END)

        for font in fu.list_fonts():
            self.mylistbox.insert(tk.END, font)
            self.logger.info(f" font found: {font}")

        self.mylistbox.selection_set(tk.END)



