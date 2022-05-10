###############################################################################################################
#    pyKlock   Copyright (C) <2022>  <Kevin Scott>                                                            #                                                                                                             #                                                                                                             #
#     Display the current local time in many forms.                                                           #
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

import platform
import subprocess

import src.theme        as theme
import src.fonts        as fonts
import src.config       as Config
import src.logger       as Logger
import src.license      as license
import src.selectTime   as time
import src.klock_layout as klock

import src.utils.fonts_utils as fu
import src.utils.klock_utils as utils

from src.projectPaths import *



def run_klock(my_logger, my_config):
    """  Builds and runs the Klock.
    """
    current_time = time.SelectTime()                                           #  Object with the varied time codes.

    font_name    = my_config.FONT_NAME                                         #  Initial name of the font used.
    font_size    = my_config.FONT_SIZE                                         #  Initial size of the font used.
    win_location = (my_config.X_POS, my_config.Y_POS)                          #  Initial windows location.
    win_size     = (my_config.WIN_WIDTH, my_config.WIN_HEIGHT)                 #  Initial windows size.
    time_type    = my_config.TIME_TYPE                                         #  Initial time type.
    sg.theme(my_config.THEME)                                                  #  Initial theme.
    pr_button    = "-FUZZY-"                                                   #  Initial view.

    sg.SetOptions(element_padding=(0, 0))

    # Create the Window
    window = klock.win_layout(my_config, win_location, win_size, current_time.timeTypes, font_name, font_size, time_type)  #  Creates the initial window.

    utils.update_status_bar(window)
    window["-CURRENT_TIME-"].update(current_time.getTime(time_type))

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read(timeout=1000)

        if event in (sg.WIN_CLOSED, 'Exit', "-EXIT-"):            # if user closes window or clicks quit
            break

        utils.update_status_bar(window)
        window["-CURRENT_TIME-"].update(current_time.getTime(time_type))

        match event:
            case ("-BTN_FUZZY-"|"-BTN_WORLD-"|"-BTN_COUNTDOWN-"|"-BTN_TIMER-"):                     #  Button pressed, change views.
                pressed = "-" + event[5:-1] +"-"
                window[pr_button].update(visible=False)
                window[pressed].update(visible=True)
                pr_button = pressed
            case "-TIME_TYPES-":                                                                    #  Another choice selected from the combo box.
                window.disappear()
                time_type = values["-TIME_TYPES-"]
                ret_font, font_name, font_size = fu.set_font(font_name, time_type)  #  Returns a font object.
                window = klock.win_layout(my_config, win_location, win_size, current_time.timeTypes, font_name, font_size, time_type)
                window["-CURRENT_TIME-"].update(current_time.getTime(time_type))
                my_logger.debug(f"Time Type {time_type}  Font name = {font_name}  Font size = {font_size}")
                window.reappear()
            case "LCD Klock":                                                                       #  Run the sub project pyDigitalKlock_psg have to
                window.hide()                                                                       #  hide window, if use disappear the window
                sg.execute_py_file(pyfile="main.py", cwd="pyDigitalKlock_psg", wait=True)           #  appears almost immediately.  Probably because
                window.un_hide()                                                                    #  running an .py file and not a internal sg call.
            case "License":                                                                         #  Display License info.
                window.disappear()
                license.run_license(my_config.NAME, my_config.VERSION)
                window.reappear()
            case "About":                                                                           #  Display About info, triggered from the menu option.
                window.disappear()
                sg.popup(my_config.NAME, f"V {my_config.VERSION}", "PySimpleGUI Version", sg.version, grab_anywhere=True)
                window.reappear()
            case "Theme":                                                                           #  Change the theme, triggered from the menu option.
                window.disappear()
                sg.theme(theme.run_theme())
                window = klock.win_layout(my_config, win_location, win_size, current_time.timeTypes, font_name, font_size, time_type)
                window["-CURRENT_TIME-"].update(current_time.getTime(time_type))
                window.reappear()
            case "Font":                                                                             #  Change the font, triggered from the menu option.
                window.disappear()
                new_font, font_name, font_size = fonts.run_fonts(time_type)
                if new_font:                            #  Cancel was selected in font window, or no font selected.
                    window = klock.win_layout(my_config, win_location, win_size, current_time.timeTypes, font_name, font_size, time_type)
                    window['-CURRENT_TIME-'].update(font=new_font)
                    window["-CURRENT_TIME-"].update(current_time.getTime(time_type))
                    my_logger.debug(f"Font name = {font_name}  Font size = {font_size}")

                window.reappear()


    try:                                                                                #  Saves the current configuration and closes app.
        my_config.FONT_NAME  = font_name                                                #  Final name of the font used.
        my_config.FONT_SIZE  = font_size                                                #  Final size of the font used.
        my_config.WIN_WIDTH  = window.Size[0]                                           #  Final windows width.
        my_config.WIN_HEIGHT = window.Size[1]                                           #  Final windows height.
        my_config.X_POS      = window.current_location()[0]                             #  Final windows X position.
        my_config.Y_POS      = window.current_location()[1]                             #  Final windows Y position.
        my_config.TIME_TYPE  = time_type                                                #  Final time type.
        my_config.THEME      = sg.theme()
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




