###############################################################################################################
#    pyKlock   Copyright (C) <2022>  <Kevin Scott>                                                            #                                                                                                             #                                                                                                             #
#     An attempt to re-create a Klock [using pySimpleGUI].                                                    #
#                                                                                                             #
#     For changes see history.txt                                                                             #
#                                                                                                             #
###############################################################################################################
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

import PySimpleGUI as sg

from tkinter.colorchooser import askcolor

import datetime
import platform

import src.fonts   as fonts
import src.theme   as theme
import src.config  as Config
import src.logger  as Logger
import src.license as license

from src.projectPaths import *

from src.layouts.fuzzy_time_layout  import fuzzy_time_layout
from src.layouts.world_klock_layout import world_klock_layout
from src.layouts.countdown_layout   import countdown_layout
from src.layouts.timer_layout       import timer_layout
from src.layouts.menu_defs          import menu_def

def run_klock(my_logger, my_config):
    """  Builds and runs the Klock.
    """

    #  Create actual layout using columns and a row of buttons
    layout = [[sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
              [sg.Column(fuzzy_time_layout,  visible=True,  key="-FUZZY-"),
               sg.Column(world_klock_layout, visible=False, key="-WORLD-"),
               sg.Column(countdown_layout,   visible=False, key="-COUNTDOWN-"),
               sg.Column(timer_layout,       visible=False, key="-TIMER-")],
              [sg.Button("Fuzzy Time",  key="-BTN_FUZZY-"),
               sg.Button("World Klock", key="-BTN_WORLD-"),
               sg.Button("Countdown",   key="-BTN_COUNTDOWN-"),
               sg.Button("Timer",       key="-BTN_TIMER-")]
             ]

    pr_button = "-FUZZY-"
    window = sg.Window("pyKlock", layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        match event:
            case ("-BTN_FUZZY-"|"-BTN_WORLD-"|"-BTN_COUNTDOWN-"|"-BTN_TIMER-"):
                pressed = "-" + event[5:-1] +"-"
                window[pr_button].update(visible=False)
                window[pressed].update(visible=True)
                pr_button = pressed
            case "License":
                window.disappear()
                license.run_license(my_config.NAME, my_config.VERSION)
                window.reappear()
            case "About":
                window.disappear()
                sg.popup(f"{my_config.NAME}    V {my_config.VERSION}", "PySimpleGUI Version", sg.version, grab_anywhere=True)
                window.reappear()

    window.close(); del window




def main():
    """  Sets up the logger and config objects and runs the klock.
    """
    my_logger  = Logger.get_logger(str(LOGGER_PATH))    # Create the logger.
    my_config  = Config.Config(CONFIG_PATH, my_logger)  # Create the config.

    my_logger.info("-" * 100)
    my_logger.info(f"  Running {my_config.NAME} Version {my_config.VERSION} ")
    my_logger.debug(f" {platform.uname()}")
    my_logger.debug(f" Python Version {platform.python_version()}")
    my_logger.debug("")
    my_logger.debug(f" CONFIG_PATH :: {CONFIG_PATH}")
    my_logger.debug(f" LOGGER_PATH :: {LOGGER_PATH}")
    my_logger.debug(f" FONTS_PATH  :: {FONTS_PATH}")
    my_logger.debug("")

    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        my_logger.debug("  Running in a PyInstaller bundle")
    else:
        my_logger.debug("  Running in a normal Python process")

    run_klock(my_logger, my_config)

    my_logger.info(f"  Ending {my_config.NAME} Version {my_config.VERSION} ")
    my_logger.info("-" * 100)


if __name__ == '__main__':
    #  Call main is script if run directly.
    main()




