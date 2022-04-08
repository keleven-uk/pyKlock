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
from tkinter.colorchooser import askcolor

import pygubu

import sys
import platform
import datetime

import src.Config as Config
import src.Logger as Logger
import src.About as About
import src.Fonts as Fonts
import src.utils.pyDigitalKlock_utils as utils
import src.utils.fonts_utils as fu

from src.projectPaths import *



class FirstApp:
    """  Support logic for the GUI of pyDigitalKlock.

         GUI elements held in pyDigitalKlock.ui, created using pygubu-designer.
    """
    def __init__(self, myConfig, logger, master=None):

        self.logger  = logger
        self.config  = myConfig
        self.foreground = self.config.FOREGROUND
        self.background = self.config.BACKGROUND
        self.transparent = False

        self.row1 = 0
        self.new_font = None

        # Create a builder and setup resources path (if you have images)
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(RESOURCE_PATH)

        # Load an ui file
        builder.add_from_file(PROJECT_UI)

        # Create the mainwindow
        self.mainwindow = builder.get_object('mainwindow', master)
        self.width      = self.mainwindow.cget("width")
        self.mainwindow.overrideredirect(True)

        # Create transparent window
        self.mainwindow.wm_attributes("-topmost", True)
        self.mainwindow.wm_attributes("-transparentcolor", 'gray')
        self.mainwindow.wait_visibility()

        self.myAbout = About.About(self.mainwindow, self.config.NAME, self.config.VERSION)
        self.myFont  = Fonts.Font(self.mainwindow, logger)

        self.lbl_current_time  = builder.get_object("lblTime", master)
        self.lbl_today_date    = builder.get_object("lblDate", master)
        self.lbl_current_state = builder.get_object("lblState", master)
        self.lbl_idle_time     = builder.get_object("lblIdle", master)

        # Set main menu
        self.mainmenu = mainmenu = builder.get_object('mainmenu', self.mainwindow)
        self.mainwindow.configure(menu=mainmenu)
        self.mainmenu.bind_all("<Control-q>", self.quit)        #  Bind menu quit option to self.quit.

        # Connect to Delete event
        self.mainwindow.protocol("WM_DELETE_WINDOW", self.quit)

        # Connect callbacks
        builder.connect_callbacks(self)

        #  Bind mouse, so app can be moved.
        self.mainwindow.bind("<Button-1>", self.startMove)
        self.mainwindow.bind("<ButtonRelease-1>", self.stopMove)
        self.mainwindow.bind("<B1-Motion>", self.moving)

        self.mainwindow.geometry("+%s+%s" % (self.config.X_POS, self.config.Y_POS))

        self.set_check()
        self.set_colours()
        self.set_time_date()


    def on_items_clicked(self, itemid):
        """  Handle the menu options.
        """
        if itemid == 'mfile_quit':
            self.quit()
        if itemid == 'mhelp_about':
            self.show_about_dialog()
        if itemid == 'mFonts_fonts':
            self.show_font_dialog()
        if itemid == 'mColour_foreground':
            colours = askcolor(title="Choose colour of foreground")
            self.foreground = colours[1]
            self.set_colours()
        if itemid == 'mColour_background':
            colors = askcolor(title="Choose colour of background")
            self.background = colors[1]
            self.set_colours()
        if itemid == 'mcolour_transparent':
            self.set_colours()


    def show_about_dialog(self):
        """  Call the about dialog.
        """
        self.logger.info(f"    Running About Dialog ")
        self.myAbout.show_about_dialog()
        self.logger.info(f"    Closing About Dialog ")

    def show_font_dialog(self):
        """  Call the font dialog.
        """
        self.logger.info(f"    Running Font Dialog ")
        self.myFont.show_font_dialog()
        self.logger.info(f"    Closing Font Dialog ")

    def set_time_date(self):
        """  Update the screen, current time, date & idle time.

             TODO Stop guessing at length of idle time and try and use ttk measure function.
        """

        strNow  = datetime.datetime.now()

        #  Set the time.
        var = self.builder.get_variable("current_time")
        var.set(f"{strNow:%H:%M:%S}")

        #  Set the date
        var = self.builder.get_variable("today_date")
        var.set(f"{ strNow:%A %d %B %Y}")

        #  Set the state
        var = self.builder.get_variable("current_state")
        var.set(f"{utils.get_state()}")

        #  Set the state
        idle = int(utils.get_idle_duration())
        if idle > 5:                                                #  Only print idles time if greater then 5 seconds.
            strIdle = f"idle : {utils.formatSeconds(idle)}"
            length  = len(strIdle)
            strIdle = strIdle.rjust(58-length, " ")                 #  Guess at 58 characters for right justification.
        else:
            strIdle = ""

        var = self.builder.get_variable("idle_time")            #  This could change if the font is changed.
        var.set(f"{strIdle}")

        self.set_row()

        # Call the set_time_date() function every 1 second.
        self.mainwindow.after(1000, self.set_time_date)

    def set_row(self):
        if self.myFont.row == -1:
            return
        if self.myFont.row != self.row1:
            self.row1 = self.myFont.row
            print(self.new_font)
            self.new_font = fu.set_font(self.row1)

    def set_check(self):
        variable = self.builder.get_variable("mcolour_transparent_clicked")
        variable.set(self.config.TRANSPARENT)

    def set_colours(self):
        variable = self.builder.get_variable("mcolour_transparent_clicked")
        self.transparent = variable.get()

        if self.transparent:
            big = "grey"
            self.config.TRANSPARENT = True
        else:
            big = self.background
            self.config.TRANSPARENT = False

        self.mainwindow.configure(background=big)
        self.mainmenu.configure(background=big,  foreground=self.foreground)
        self.lbl_current_time.configure(background=big,  foreground=self.foreground)
        self.lbl_today_date.configure(background=big,    foreground=self.foreground)
        self.lbl_current_state.configure(background=big, foreground=self.foreground)
        self.lbl_idle_time.configure(background=big,     foreground=self.foreground)

        if self.new_font:
            self.lbl_current_time.configure(font=self.new_font)


    #  Used to move the app.
    def startMove(self,event):
        self.x = event.x
        self.y = event.y

    def stopMove(self,event):
        self.x = None
        self.y = None

    def moving(self,event):
        x = (event.x_root - self.x)
        y = (event.y_root - self.y)
        self.config.X_POS = x
        self.config.Y_POS = y
        self.mainwindow.geometry("+%s+%s" % (x, y))

    def quit(self, event=None):
        self.config.FOREGROUND = self.foreground
        self.config.BACKGROUND = self.background
        self.config.writeConfig()

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
    logger.debug(f" {platform.uname()}")
    logger.debug(f" Python Verion {platform.python_version()}")
    #logger.debug("")
    #logger.debug(f" PROJECT_PATH :: {PROJECT_PATH}")
    #logger.debug(f" MAIN_PATH    :: {MAIN_PATH}")
    #logger.debug(f" PROJECT_UI   :: {PROJECT_UI}")
    #logger.debug(f" RESOURCE_PATH:: {RESOURCE_PATH}")
    #logger.debug(f" FONTS_PATH   :: {FONTS_PATH}")
    #logger.debug(f" CONFIG_PATH  :: {CONFIG_PATH}")
    #logger.debug(f" LOGGER_PATH  :: {LOGGER_PATH}")
    #logger.debug("")

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        logger.debug("  Running in a PyInstaller bundle")
    else:
        logger.debug("  Running in a normal Python process")

    app = FirstApp(myConfig, logger)
    app.run()

    logger.info(f"  Ending {myConfig.NAME} Version {myConfig.VERSION} ")
    logger.info("-" * 100)


if __name__ == '__main__':
    main()

