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

import src.Config as Config
import src.Logger as Logger
import src.utils.pyDigitalKlock_utils as utils

PROJECT_PATH  = pathlib.Path(__file__).parent
MAIN_PATH     = pathlib.Path(__file__).parent.parent
PROJECT_UI    = PROJECT_PATH / "pyDigitalKlock.ui"
RESOURCE_PATH = MAIN_PATH / "resources"
CONFIG_PATH   = MAIN_PATH / "config.toml"
LOGGER_PATH   = MAIN_PATH / "pyDigitalKlock.log"

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

        #  Set the time.
        strTime = strNow.strftime("%H:%M:%S")
        var     = self.builder.get_variable('current_time')
        var.set(f"{strTime}")

        #  Set the date
        strDate = strNow.strftime("%A %d %B %Y")
        var     = self.builder.get_variable("today_date")
        var.set(f"{strDate}")

        #  Set the state
        state = utils.get_state()
        var   = self.builder.get_variable('current_state')
        var.set(f"{state}")

        #  Set the state
        idle    = int(utils.get_idle_duration())
        if idle > 5:                                                #  Only print idles time if greater then 5 seconds.
            strIdle = f"idle : {utils.formatSeconds(idle)}"
            length  = len(strIdle)
            strIdle = strIdle.rjust(58-length, " ")                 #  Guess at 58 characters for right justification.
        else:
            strIdle = ""

        var     = self.builder.get_variable('idle_time')        #  This could change if the font is changed.
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


    def run(self):
        self.mainwindow.mainloop()


def main():
    """  Main function to run the thing.
    """
    logger   = Logger.get_logger(str(LOGGER_PATH))          # Create the logger.
    myConfig = Config.Config(CONFIG_PATH,logger)            # Create the config.


    logger.info("-" * 100)
    logger.info(f"  Running {myConfig.NAME} Version {myConfig.VERSION} ")

    app = FirstApp()
    app.run()

    logger.info(f"  Ending {myConfig.NAME} Version {myConfig.VERSION} ")
    logger.info("-" * 100)


if __name__ == '__main__':
    main()

