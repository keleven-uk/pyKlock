###############################################################################################################
#    license.py   Copyright (C) <2022>  <Kevin Scott>                                                         #                                                                                                             #                                                                                                             #
#    Display a simple license dialog.                                                                         #
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

import pygubu

from src.projectPaths import *
from src.utils.License_text import license_text


class License():
    """  A Simple about dialog.
         Just displays the product name and version and a copyright notice.

         Create with:  myAbout = About.About(self.mainwindow, NAME, VERSION)
         Display with: myAbout.show_about_dialog()
    """

    def __init__(self, parent, NAME, VERSION):
        self.parent  = parent
        self.NAME    = NAME
        self.VERSION = VERSION
        self.license_dialog = None

        self.builder = builder = pygubu.Builder()

        # Load an ui file
        builder.add_from_file(PROJECT_UI)

    def show_license_dialog(self):
        if self.license_dialog is None:
            dialog = self.builder.get_object('dlg_license', self.parent)
            self.license_dialog = dialog

            def license_btnclose_clicked():
                dialog.close()

            btnclose = self.builder.get_object('license_btnclose')
            btnclose['command'] = license_btnclose_clicked

            self.mytextbox = self.builder.get_object('txt_license')
            self.mytextbox.insert(tk.END, f"{self.NAME}     {self.VERSION}      Copyright (C) 2022  Kevin Scott")
            self.mytextbox.insert(tk.END, f"")
            self.mytextbox.insert(tk.END, f"{license_text}")

            dialog.run()
        else:
            self.license_dialog.show()





