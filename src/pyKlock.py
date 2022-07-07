###############################################################################################################
#    pyKlock   Copyright (C) <2017-2022>  <Kevin Scott>                                                       #                                                                                                             #                                                                                                             #
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
from psgtray import SystemTray

from tkinter.colorchooser import askcolor

import datetime
import platform
import threading

import src.theme        as theme
import src.fonts        as fonts
import src.config       as Config
import src.logger       as Logger
import src.license      as license
import src.selectTime   as time
import src.klock_layout as klock
import src.stopwatch    as stopwatch
import src.countdown    as countdown
import src.world_klock  as world_klock

import src.reminder.reminder     as reminder
import src.reminder.reminder_gui as reminder_gui

import src.contacts.contacts     as contacts
import src.contacts.contacts_gui as contacts_gui

import src.utils.fonts_utils as fu
import src.utils.klock_utils as utils
import src.utils.archive     as archive

from src.projectPaths import *



def run_klock(my_logger, my_config):
    """  Builds and runs the Klock.
    """
    current_time   = time.SelectTime()                                           #  Object with the varied time codes.
    my_stopwatch   = stopwatch.timer()
    my_world_klock = world_klock.world_klock(backward_file_path)

    font_name      = my_config.FONT_NAME                                         #  Initial name of the font used.
    font_size      = my_config.FONT_SIZE                                         #  Initial size of the font used.
    win_location   = (my_config.X_POS, my_config.Y_POS)                          #  Initial windows location.
    win_size       = (my_config.WIN_WIDTH, my_config.WIN_HEIGHT)                 #  Initial windows size.
    time_type      = my_config.TIME_TYPE                                         #  Initial time type.
    pr_button      = "-FUZZY-"                                                   #  Initial view.
    pressed        = "-FUZZY-"
    tray_displayed = False
    sg.theme(my_config.THEME)                                                  #  Initial theme.

    sg.SetOptions(element_padding=(0, 0))

    # Create the Window and Tray.
    window = klock.win_layout(my_config, my_world_klock, win_location, win_size, current_time.timeTypes, font_name, font_size, time_type)    #  Creates the initial window.
    tray   = SystemTray(klock.tray_menu, single_click_events=False, window=window, tooltip=klock.tray_tooltip, icon=sg.DEFAULT_BASE64_ICON)  #  Create the tray.

    #  Create my_countdown
    my_countdown = countdown.countdown(window)

    #  Create reminders database
    reminder_db = reminder.reminders()
    reminder_db.check_due()

    #  Create contacts database.
    contacts_db = contacts.contacts()

    utils.right_alignment_tables(window)

    utils.set_title(window, pr_button, my_stopwatch, my_countdown, current_time, reminder_db, contacts_db)
    utils.update_status_bar(window)
    window["-CURRENT_TIME-"].update(current_time.getTime(time_type))

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        win, event, values = sg.read_all_windows(timeout=1000)      #  Use read_all_windows - so, we can read and close the reminders.

        # IMPORTANT step. It's not required, but convenient. Set event to value from tray
        # if it's a tray event, change the event variable to be whatever the tray sent
        if event == tray.key:
            event = values[event]       # use the System Tray's event as if was from the window

        match event:

            case (sg.WIN_CLOSED|"Exit"|"-EXIT-"):
                break

            case ("-BTN_FUZZY-"|"-BTN_WORLD-"|"-BTN_COUNTDOWN-"|"-BTN_TIMER-"|"-BTN_REMINDER-"|"-BTN_CONTACT-"):    #  Button pressed, change views.
                pressed = "-" + event[5:-1] +"-"
                window[pr_button].update(visible=False)
                window[pressed].update(visible=True)
                pr_button = pressed
                utils.set_title(window, pressed, my_stopwatch, my_countdown, current_time, reminder_db, contacts_db)

                if not "-REMINDER-":                                                                #  Tries to stop the table refresh for every event loop.
                    refresh_reminder_table = False
                else:
                    refresh_reminder_table = True

                if not "-CONTACT-":                                                                #  Tries to stop the table refresh for every event loop.
                    refresh_contacts_table = False
                else:
                    refresh_contacts_table = True

            case "-HIDE-":
                tray.change_icon(sg.EMOJI_BASE64_HAPPY_JOY)                                         #  Sad icon.
                #tray.change_icon(sg.EMOJI_BASE64_FRUSTRATED)                                       #  Sad icon.
                window.hide()
                tray.show_icon()        # if hiding window, better make sure the icon is visible
                tray_displayed = True

            case "Show pyKlock":
                window.un_hide()
                window.bring_to_front()
                tray_displayed = False

            case "-TIME_TYPES-":                                                                    #  Another choice selected from the combo box.
                window.close()
                time_type = values["-TIME_TYPES-"]
                ret_font, font_name, font_size = fu.set_font(font_name, time_type)  #  Returns a font object.
                window = klock.win_layout(my_config, my_world_klock, win_location, win_size, current_time.timeTypes, font_name, font_size, time_type)
                window["-CURRENT_TIME-"].update(current_time.getTime(time_type))
                my_logger.debug(f"Time Type {time_type}  Font name = {font_name}  Font size = {font_size}")

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
                window.close()
                sg.theme(theme.run_theme())
                window = klock.win_layout(my_config, my_world_klock, win_location, win_size, current_time.timeTypes, font_name, font_size, time_type)
                window["-CURRENT_TIME-"].update(current_time.getTime(time_type))

            case "Font":
                #  Change the font, triggered from the menu option.
                    window.disappear()
                    new_font, font_name, font_size = fonts.run_fonts(time_type)
                    if new_font:                            #  Cancel was selected in font window, or no font selected.
                        window.close()
                        window = klock.win_layout(my_config, my_world_klock, win_location, win_size, current_time.timeTypes, font_name, font_size, time_type)
                        window['-CURRENT_TIME-'].update(font=new_font)
                        window["-CURRENT_TIME-"].update(current_time.getTime(time_type))
                        my_logger.debug(f"Font name = {font_name}  Font size = {font_size}")
                    else:
                        window.reappear()

            case "Save Reminders":
                archive.save_database("reminders")

            case "Save Contacts":
                archive.save_database("contacts")

            case "Load Reminders":
                archive.load_database("reminders")

            case "Load Contacts":
                archive.load_database("contacts")

            case ("-TIMER_START-"|"-TIMER_RESUME-"|"-TIMER_STOP-"|"-TIMER_PAUSE-"|"-TIMER_CLEAR-"):
                #  Stopwatch functions called - pass to my_stopwatch.
                stopwatch.run_stopwatch(event, window, my_stopwatch)

            case ("-+15-"|"-+30-"|"-+45-"|"-+60-"|"-COUNTDOWN_START-"|"-COUNTDOWN_STOP-"|"-COUNTDOWN_TARGET-"|"-COUNTDOWN_EVENT-"):
                #  Countdown functions called - pass to my_countdown.
                countdown.run_countdown(event, window, my_countdown, values)

            case "-WORLD_ZONE-":
                #  World Klock functions called - pass to my_world_klock.
                timezone = values["-WORLD_ZONE-"]
                window["-WORLD_TEXT-"].update(my_world_klock.get_local_time(timezone))

            case "-REMINDER_ADD-":                                                      #  Doesn't need a row selected.
                reminder_list = reminder_gui.run_reminders(True, reminder_db)
                window["-REMINDER_TABLE-"].update(reminder_list)

            case ("-REMINDER_EDIT-"|"-REMINDER_DELETE-"):
                if values["-REMINDER_TABLE-"] != []:                                    #  Check a row has been selected.
                    line_number = values["-REMINDER_TABLE-"][0]
                    if event == "-REMINDER_EDIT-":
                        item_list = reminder_gui.run_reminders(True, reminder_db, "EDIT", line_number)
                    else:  # must be delete.
                        item_list = reminder_gui.run_reminders(True, reminder_db, "DELETE", line_number)
                    window["-REMINDER_TABLE-"].update(item_list)

            case "-CONTACT_ADD-":                                                      #  Doesn't need a row selected.
                contacts_list = contacts_gui.run_contacts(True, contacts_db)
                window["-CONTACT_TABLE-"].update(contacts_list)

            case ("-CONTACT_EDIT-"|"-CONTACT_DELETE-"):
                if values["-CONTACT_TABLE-"] != []:                                    #  Check a row has been selected.
                    line_number = values["-CONTACT_TABLE-"][0]

                    if event == "-CONTACT_EDIT-":
                        item_list = contacts_gui.run_contacts(True, contacts_db, "EDIT", line_number)
                    else:  # must be delete.
                        item_list = contacts_gui.run_contacts(True, contacts_db, "DELETE", line_number)
                    window["-CONTACT_TABLE-"].update(item_list)


        #  Update stuff at the end of the event loop.
        if pressed == "-FUZZY-":
            window["-CURRENT_TIME-"].update(current_time.getTime(time_type))
        if my_stopwatch.timer_running:
            window["-TIMER_TEXT-"].update(my_stopwatch.elapsed_time)
        if my_countdown.countdown_running:
            window["-COUNTDOWN_TEXT-"].update(my_countdown.tick())
        if pressed == "-WORLD-":
            timezone = values["-WORLD_ZONE-"]
            window["-WORLD_TEXT-"].update(my_world_klock.get_local_time(timezone))
        if pressed == "-REMINDER-":
            if refresh_reminder_table:                                                 #  Should fire first time around.
                reminder_db.check_due()
                reminder_list = reminder_db.list_reminders()
                window["-REMINDER_TABLE-"].update(values=reminder_list)
                refresh_reminder_table = False
        if pressed == "-CONTACT-":
            if refresh_contacts_table:                                                 #  Should fire first time around.
                contacts_list = contacts_gui.run_contacts(False, contacts_db)
                window["-CONTACT_TABLE-"].update(values=contacts_list)
                refresh_contacts_table = False

        #  Check for any reminders due every 1 minutes.
        min_now = datetime.datetime.now().minute
        sec_now = datetime.datetime.now().second
        if sec_now == 0:
            reminder_db.check_due()
            reminder_list = reminder_db.list_reminders()
            window["-REMINDER_TABLE-"].update(values=reminder_list)

        if tray_displayed and (min_now % 10 == 0) and (sec_now == 0):
            tray.show_message(title="PyKlock - Current Time", message=current_time.getTime(time_type))

        utils.set_title(window, pr_button, my_stopwatch, my_countdown, current_time, reminder_db, contacts_db)
        utils.update_status_bar(window)

#   Outside of event loop.
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

    tray.close()
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
    my_logger.debug(f" CONFIG_PATH     :: {CONFIG_PATH}")
    my_logger.debug(f" LOGGER_PATH     :: {LOGGER_PATH}")
    my_logger.debug(f" FONTS_PATH      :: {FONTS_PATH}")
    my_logger.debug(f" RESOURCE_PATH   :: {RESOURCE_PATH}")
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




