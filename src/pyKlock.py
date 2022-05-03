###############################################################################################################
#    pyDigitalKlock   Copyright (C) <2022>  <Kevin Scott>                                                     #                                                                                                             #                                                                                                             #
#     An attempt to re-create a LCD Klock [using pySimpleGUI].                                                #
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

import src.theme        as theme
import src.klock_layout as klock
import src.config       as Config
import src.logger       as Logger
import src.license      as license

from src.projectPaths import *



def run_klock(my_logger, my_config):
    """  Builds and runs the Klock.
    """
    pr_button = "-FUZZY-"

    sg.theme(my_config.THEME)                           #  Default or initial theme.
    sg.SetOptions(element_padding=(0, 0))

    # Create the Window
    window = klock.win_layout(my_config)  #  Creates the initial window.

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read(timeout=1000)

        if event in (sg.WIN_CLOSED, 'Exit', "-EXIT-"):            # if user closes window or clicks quit
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
                sg.popup(my_config.NAME, f"V {my_config.VERSION}", "PySimpleGUI Version", sg.version, grab_anywhere=True)
                window.reappear()
            case "Theme":
                window.disappear()
                sg.theme(theme.run_theme())
                window = klock.win_layout(my_config)
                txt_colour = sg.theme_text_color()
                win_colour = sg.theme_background_color()
                window.reappear()
            case "-STARTMOVE-":                                                                      #  Left click, start move.
                off_x = window.CurrentLocation()[0] - window.mouse_location()[0]                     #  Offset from window top left hand corner
                off_y = window.CurrentLocation()[1] - window.mouse_location()[1]                     #  to mouse position.
            case "-STOPMOVE-":                                                                       #  Not currently used.
                pass
            case "-MOVING-":                                                                         #  The mouse has been moved
                my_config.X_POS = window.mouse_location()[0] + off_x                                 #  Calculate the new windows position.
                my_config.Y_POS = window.mouse_location()[1] + off_y
                window.move(my_config.X_POS, my_config.Y_POS)                                        #  Move the window.

    try:                                                                                             #  Saves the current configuration and closes app.
        my_config.THEME = sg.theme()
        my_config.writeConfig()
    except Exception as e:
        my_logger.debug(f" Error occurred during saving of config: {e}")

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




