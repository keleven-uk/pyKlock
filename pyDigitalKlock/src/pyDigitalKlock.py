###############################################################################################################
#    pyDigitalKlock   Copyright (C) <2022>  <Kevin Scott>                                                     #                                                                                                             #                                                                                                             #
#     An attempt to re-create a LCD Klock.                                                                    #
#                                                                                                             #
#     For changes see history.txt                                                                             #
#                                                                                                             #
###############################################################################################################
#    Copyright (C) <2020-2021>  <2022>                                                                        #
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

import pathlib
import tkinter as tk
from tkinter import font
import tkinter.ttk as ttk
import pygubu

import datetime

import src.utils.pyDigitalKlock_utils as utils


PROJECT_PATH  = pathlib.Path(__file__).parent
MAIN_PATH     = pathlib.Path(__file__).parent.parent
PROJECT_UI    = PROJECT_PATH / "pyDigitalKlock.ui"
RESOURCE_PATH = MAIN_PATH / "resources"


class FirstApp:
    def __init__(self, master=None):
        # 1: Create a builder and setup resources path (if you have images)
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(RESOURCE_PATH)

        # 2: Load an ui file
        builder.add_from_file(PROJECT_UI)

        # 3: Create the mainwindow
        self.mainwindow = builder.get_object('mainwindow', master)
        self.width      = self.mainwindow.cget("width")

        # 4: Connect callbacks
        builder.connect_callbacks(self)

        self.check_font()
        self.set_time_date()


    def set_time_date(self):
        strNow  = datetime.datetime.now()
        state   = utils.get_state()
        idle    = int(utils.get_idle_duration())

        #  Set the time.
        varname = 'current_time'
        var = self.builder.get_variable(varname)
        strDate = strNow.strftime("%H:%M:%S")
        var.set(f"{strDate}")

        strDate   = strNow.strftime("%A %d %B %Y")
        strStatus = utils.formatStatus(self.width, strDate, state, idle)

        #  Set the date
        varname = 'today_date'
        var = self.builder.get_variable(varname)

        var.set(f"{strStatus}")


        # Call the set_time_date() function every 1 second.
        self.mainwindow.after(1000, self.set_time_date)


    def check_font(self):
        """  Quick check to see if the digital font is present.
        """
        if "DS-Digital" in font.families():
            print("DS-Digital font Found")
        else:
            print("DS-Digital not found, Please install")
        if "Hack" in font.families():
            print("Hack font Found")
        else:
            print("Hack not found, Please install")


    def run(self):
        self.mainwindow.mainloop()


def main():
    """  Main function to run the thing.
    """
    app = FirstApp()
    app.run()


if __name__ == '__main__':
    main()

