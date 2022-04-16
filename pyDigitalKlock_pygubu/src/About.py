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


import pygubu

from src.projectPaths import *

class About():
    """  A Simple about dialog.
         Just displays the product name and version and a copyright notice.

         Create with:  myAbout = About.About(self.mainwindow, NAME, VERSION)
         Display with: myAbout.show_about_dialog()
    """

    def __init__(self, parent, NAME, VERSION):
        self.parent  = parent
        self.NAME    = NAME
        self.VERSION = VERSION
        self.about_dialog = None

        self.builder = builder = pygubu.Builder()

        # Load an ui file
        builder.add_from_file(PROJECT_UI)

    def show_about_dialog(self):
        if self.about_dialog is None:
            dialog = self.builder.get_object('dlg_about', self.parent)
            self.about_dialog = dialog

            def dialog_btnclose_clicked():
                dialog.close()

            btnclose = self.builder.get_object('about_btnclose')
            btnclose['command'] = dialog_btnclose_clicked

            var = self.builder.get_variable('product_name')
            var.set(f"{self.NAME}")
            var = self.builder.get_variable('product_version')
            var.set(f"{self.VERSION}")
            var = self.builder.get_variable('product_copyright')
            var.set("Copyright (C) <2022>  <Kevin Scott>")

            dialog.run()
        else:
            self.about_dialog.show()
