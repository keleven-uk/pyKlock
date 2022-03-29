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

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font
from tkinter import messagebox

import pygubu

import datetime

import src.Config as Config
import src.Logger as Logger
import src.About as About
import src.utils.pyDigitalKlock_utils as utils

from src.projectPaths import *



class FirstApp:
    """  Support logic for the GUI of pyDigitalKlock.

         GUI elements held in pyDigitalKlock.ui, created using pygubu-designer.
    """
    def __init__(self, myConfig, logger, master=None):

        self.myAbout = About.About(self.mainwindow, myConfig)
        self.logger  = logger

        # Create a builder and setup resources path (if you have images)
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(RESOURCE_PATH)

        # Load an ui file
        builder.add_from_file(PROJECT_UI)

        # Create the mainwindow
        self.mainwindow = builder.get_object('mainwindow', master)
        self.width      = self.mainwindow.cget("width")

        # Set main menu
        self.mainmenu = mainmenu = builder.get_object('mainmenu', self.mainwindow)
        self.mainwindow.configure(menu=mainmenu)

        # Connect to Delete event
        self.mainwindow.protocol("WM_DELETE_WINDOW", self.quit)

        # Connect callbacks
        builder.connect_callbacks(self)

        self.check_font()
        self.set_time_date()


    def on_items_clicked(self, itemid):
        """  Handle the menu options.
        """
        if itemid == 'mfile_quit':
            self.quit()
        if itemid == 'mhelp_about':
            self.logger.info(f"  Running About Dialog ")
            self.show_about_dialog()
            self.logger.info(f"  Closing About Dialog ")


    def show_about_dialog(self):
        """  Call the about dialog.
        """
        self.myAbout.show_about_dialog()


    def set_time_date(self):
        """  Update the screen, current time, date & idle time.

             TODO Stop guessing at length of idle time and try and use ttk measure function.
        """
        strNow  = datetime.datetime.now()

        #  Set the time.
        strTime = strNow.strftime("%H:%M:%S")
        var     = self.builder.get_variable('current_time')
        var.set(f"{strTime}")

        #  Set the date
        strDate = strNow.strftime("%A %d %B %Y")
        var     = self.builder.get_variable("today_date")
        var.set(f"{strDate}")

        #  Set the state
        var   = self.builder.get_variable('current_state')
        var.set(f"{utils.get_state()}")

        #  Set the state
        idle    = int(utils.get_idle_duration())
        if idle > 5:                                                #  Only print idles time if greater then 5 seconds.
            strIdle = f"idle : {utils.formatSeconds(idle)}"
            length  = len(strIdle)
            strIdle = strIdle.rjust(58-length, " ")                 #  Guess at 58 characters for right justification.
        else:
            strIdle = ""

        var     = self.builder.get_variable('idle_time')            #  This could change if the font is changed.
        var.set(f"{strIdle}")

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


    def quit(self, event=None):
        self.mainwindow.quit()

    def run(self):
        self.mainwindow.mainloop()


def main():
    """  Main function to run the thing.
    """
    logger   = Logger.get_logger(str(LOGGER_PATH))          # Create the logger.
    myConfig = Config.Config(CONFIG_PATH,logger)            # Create the config.


    logger.info("-" * 100)
    logger.info(f"  Running {myConfig.NAME} Version {myConfig.VERSION} ")

    app = FirstApp(myConfig, logger)
    app.run()

    logger.info(f"  Ending {myConfig.NAME} Version {myConfig.VERSION} ")
    logger.info("-" * 100)


if __name__ == '__main__':
    main()

