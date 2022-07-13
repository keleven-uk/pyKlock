###############################################################################################################
#    klock.py   Copyright (C) <2022>  <Kevin Scott>                                                           #                                                                                                             #                                                                                                             #
#     The klock GUI layout.                                                                                   #
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

import datetime

from copy import deepcopy

from src.projectPaths import *

#  Used to build the tray object in pyKlock.py - hides here.
tray_menu    = ["", ["Show pyKlock","---","Exit"]]
tray_tooltip = "pyKlock"

def win_layout(my_config, my_world_klock, win_location, win_size, timetypes, font_name, font_size, time_type):
    """  Sets up the windows and menu layout.
         Returns a finalized windows object.

         In it's own def so that it can be easily called multiple times.
         This is so the windows can be re done after a layout change.
         A bit klunky, but a work around to reload the theme at run time and to set transparency.
    """
    strNow = datetime.datetime.now()

    #  Menu definitions

    menu_def = [["File",     ["---", "Exit"]],
                ["Settings", ["Theme", "Font"]],
                ["Time",     ["LCD Klock"]],
                ["Archive",  ["Reminders", ["Save Reminders", "Load Reminders"], "Contacts", ["Save Contacts", "Load Contacts"]]],
                ["Help",     ["License", "About"]]
                ]

    #  Fuzzy Time GUI definitions
    fuzzy_left_row_layout  = [[sg.VPush(), sg.Combo(list(timetypes), key="-TIME_TYPES-", default_value=time_type, enable_events=True, readonly=True)]]
    fuzzy_right_row_layout = [[sg.VPush(), sg.Text("00:00:00", key="-CURRENT_TIME-", font=(font_name,font_size))]]

    fuzzy_time_layout = [[sg.Text(" ")],
                         [sg.Frame("", layout=fuzzy_left_row_layout, size=(140, 80)), sg.Text(" "),
                          sg.Frame("", layout=fuzzy_right_row_layout, size=(700, 80))]]


    #  World Klock GUI definitions
    actions = my_world_klock.available_timezones
    world_klock_layout = [[sg.Combo(actions, key="-WORLD_ZONE-", default_value="GMT", enable_events=True, readonly=True, size=(20,1),  font=("TkDefaultFont", 10)),
                           sg.Text("     "), sg.Text("00:00:00", key="-WORLD_TEXT-",  font=("TkDefaultFont", 70))]]


    #  Countdown GUI definitions
    actions = ["None", "Notify", "Notify + Sound", "Pop Up", "Shutdown PC", "Log Out PC"]
    countdown_top_left_layout    = [sg.Spin([x+1 for x in range(120)], key="-COUNTDOWN_TARGET-", size=(8,1),  font=("TkDefaultFont", 16))]
    countdown_bottom_left_layout = [sg.Combo(actions, key="-COUNTDOWN_ACTION-", default_value=actions[0], size=(14,1),  font=("TkDefaultFont", 10))]
    countdown_middle_left_layout = [sg.Text("")]
    countdown_column_left_layout = [countdown_top_left_layout, countdown_middle_left_layout, countdown_bottom_left_layout]

    countdown_layout = [[sg.Column(countdown_column_left_layout),
                         sg.Text("     "), sg.Text("00:00:00", key="-COUNTDOWN_TEXT-",  font=("TkDefaultFont", 56)),
                         sg.Push(),
                         sg.Button("", key="-COUNTDOWN_START-", size=(10,5), visible=True,
                               image_filename=start_image, image_size=(100, 100), tooltip="Start the Countdown"),
                         sg.Button("", key="-COUNTDOWN_STOP-", size=(10,5), visible=False,
                               image_filename=stop_image, image_size=(100, 100), tooltip="Stop the Countdown"),
                         sg.Push(),
                         sg.Button("+15", key="-+15-", size=(5,2)),
                         sg.Button("+30", key="-+30-", size=(5,2)),
                         sg.Button("+45", key="-+45-", size=(5,2)),
                         sg.Button("+60", key="-+60-", size=(5,2))
                       ]]


    #  Stopwatch [Time] GUI definitions
    timer_layout = [[sg.Text("00:00:00", key="-TIMER_TEXT-",  font=("TkDefaultFont", 56)),
                     sg.Text(" "),
                     sg.Button("", key="-TIMER_START-", size=(10,5), visible=True,
                               image_filename=start_image,  image_size=(100, 100), tooltip="Start the Timer"),
                     sg.Button("", key="-TIMER_RESUME-", size=(10,5), visible=False,
                               image_filename=resume_image, image_size=(100, 100), tooltip="Re-start the Timer"),
                     sg.Button("", key="-TIMER_STOP-", size=(10,5), visible=False,
                               image_filename=stop_image,   image_size=(100, 100), tooltip="Stop the Timer"),
                     sg.Button("", key="-TIMER_PAUSE-", size=(10,5), visible=False,
                               image_filename=pause_image,  image_size=(100, 100), tooltip="Pause the Timer"),
                     sg.Button("", key="-TIMER_CLEAR-", size=(10,5), visible=False,
                               image_filename=clear_image,  image_size=(100, 100), tooltip="Clear the Timer")]
                   ]

    #  Reminder GUI definitions
    #  REMINDER_ID           = 0
    #  REMINDER_TIME_LEFT    = 1
    #  REMINDER_DISP_LEFT    = 2
    #  REMINDER_EVENT        = 3
    #  REMINDER_DESCRIPTION  = 4
    #  REMINDER_DATE_DUE     = 5
    #  REMINDER_TIME_DUE     = 6
    #  REMINDER_AUTO_DELETE  = 7
    #  REMINDER_RECURRING    = 8
    #  REMINDER_DISPLAYED    = 9  - not displayed in table.
    #  REMINDER_05_DAYS      = 10
    #  REMINDER_15_DAYS      = 11
    #  REMINDER_30_DAYS      = 12

    reminder_data     = [['' for row in range(5)]for col in range(8)]
    reminder_headings = ["ID", "Time Mins", "Time Left", "Event", "Description", "Date Due", "Time Due", "Auto Delete", "Recurring"]

    reminder_top_button     = [sg.Button("Add",    key="-REMINDER_ADD-",    size=(5,1), pad=(1,1))]
    reminder_middle_button  = [sg.Button("Edit",   key="-REMINDER_EDIT-",   size=(5,1), pad=(1,1))]
    reminder_bottom_button  = [sg.Button("Delete", key="-REMINDER_DELETE-", size=(5,1), pad=(1,1))]
    reminder_button_layout  = [reminder_top_button, reminder_middle_button, reminder_bottom_button]

    reminder_layout = [[sg.Column(reminder_button_layout),
                        sg.Text("      "),
                        sg.Table(values=reminder_data,
                                 headings=reminder_headings,
                                 col_widths=[5, 8, 11, 13, 20, 12, 10, 10, 10, 10],
                                 enable_events=True,
                                 select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                                 background_color="light blue",
                                 auto_size_columns=False,
                                 display_row_numbers=False,
                                 vertical_scroll_only=True,
                                 justification="left",
                                 num_rows=5,
                                 alternating_row_color="lightyellow",
                                 key="-REMINDER_TABLE-",
                                 row_height=15,
                                 tooltip="Reminders Entered")]]

    #  Contacts GUI definitions
    #  CONTACT_ID          = 0
    #  CONTACT_TITLE       = 1
    #  CONTACT_LAST_NAME   = 2
    #  CONTACT_MIDDLE_NAME = 3
    #  CONTACT_FIRST_NAME  = 4
    #  CONTACT_TEL_NO      = 5
    #  CONTACT_EMAIL       = 6
    #  CONTACT_DOB         = 7
    #  CONTACT_HOUSE_NO    = 8
    #  CONTACT_STREET      = 9
    #  CONTACT_ADDRESS_1   = 10
    #  CONTACT_ADDRESS_2   = 11
    #  CONTACT_COUNTY      = 12
    #  CONTACT_POST_CODE   = 13
    #  CONTACT_COUNTRY     = 14
    #  CONTACT_NOTE        = 15

    contact_data     = [['' for row in range(4)]for col in range(15)]
    contact_headings = ["ID", "Title", "Last Name", "Middle name", "First name", "Tel No", "eMail", "D.O.B", "House", "Street", "Add 1", "Add 2", "County", "Post Code", "Country", "Note"]

    contact_top_button     = [sg.Button("Add",    key="-CONTACT_ADD-",    size=(5,1), pad=(1,1))]
    contact_middle_button  = [sg.Button("Edit",   key="-CONTACT_EDIT-",   size=(5,1), pad=(1,1))]
    contact_bottom_button  = [sg.Button("Delete", key="-CONTACT_DELETE-", size=(5,1), pad=(1,1))]
    contact_button_layout  = [contact_top_button, contact_middle_button, contact_bottom_button]

    contact_layout = [[sg.Column(contact_button_layout),
                        sg.Text("      "),
                        sg.Table(values=contact_data,
                                 headings=contact_headings,
                                 col_widths=[4, 5, 12, 10, 10, 12, 17, 13, 6, 13, 12, 12, 12, 10, 10, 20],
                                 enable_events=True,
                                 select_mode=sg.TABLE_SELECT_MODE_BROWSE,
                                 background_color="light blue",
                                 auto_size_columns=False,
                                 display_row_numbers=False,
                                 vertical_scroll_only=False,
                                 justification="left",
                                 num_rows=4,
                                 alternating_row_color="lightyellow",
                                 key="-CONTACT_TABLE-",
                                 row_height=15,
                                 tooltip="Contacts Entered")]]

    #  Buttons GUI definitions
    button_layout = [[sg.Button("Fuzzy Time",  key="-BTN_FUZZY-", pad=(1,1)),
                      sg.Button("World Klock", key="-BTN_WORLD-", pad=(1,1)),
                      sg.Button("Countdown",   key="-BTN_COUNTDOWN-", pad=(1,1)),
                      sg.Button("Timer",       key="-BTN_TIMER-", pad=(1,1)),
                      sg.Button("Reminder",    key="-BTN_REMINDER-", pad=(1,1)),
                      sg.Button("Contacts",    key="-BTN_CONTACT-", pad=(1,1)),
                      sg.Button("Hide",        key="-HIDE-", pad=(1,1)),
                      sg.Button("Exit",        key="-EXIT-", pad=(1,1))]]

    #  Build the screen, only one view visible.
    screen_layout = [sg.Column(fuzzy_time_layout,  visible=True,  key="-FUZZY-"),
                     sg.Column(world_klock_layout, visible=False, key="-WORLD-"),
                     sg.Column(countdown_layout,   visible=False, key="-COUNTDOWN-"),
                     sg.Column(timer_layout,       visible=False, key="-TIMER-"),
                     sg.Column(reminder_layout,    visible=False, key="-REMINDER-"),
                     sg.Column(contact_layout,     visible=False, key="-CONTACT-")]


    #  Status Bar GUI definitions
    status_bar = [[sg.Text("", justification="left",   key="-CURRENT-DATE-"),   sg.Push(),         #  Current Date
                   sg.Text("", justification="center", key="-CURRENT-STATUS-"), sg.Push(),         #  Current status.
                   sg.Text("", justification="right",  key="-CURRENT-IDLE-")]]                     #  Current idle time.


    #  Create actual layout using columns and a row of buttons
    klock_layout = [[sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
                    [screen_layout],
                    [sg.Text(" ")],
                    [sg.Frame("Choose Wisely", layout=button_layout, size=(850, 45))],
                    [status_bar]
                    ]


    #window = sg.Window('Window Title', layout, no_titlebar=True, alpha_channel=0.5)
    win =  sg.Window('pyKlock', klock_layout, location=win_location, size= win_size, icon="Klock.png")

    win.finalize()

    table = win["-REMINDER_TABLE-"]                                #  Code to remove the ID column from the caantacts table display.
    displaycolumns = deepcopy(reminder_headings)                   #  The ID is still needed for deleting, but doesn't need to be shown.
    displaycolumns.remove("ID")
    displaycolumns.remove("Time Mins")
    table.ColumnsToDisplay = displaycolumns                       #  Again found and used from the internet.
    table.Widget.configure(displaycolumns=displaycolumns)         #  https://stackoverflow.com/questions/70263893/deleting-hiding-a-column-of-a-table-in-pysimplegui

    table = win["-CONTACT_TABLE-"]                                #  Code to remove the ID column from the caantacts table display.
    displaycolumns = deepcopy(contact_headings)                   #  The ID is still needed for deleting, but doesn't need to be shown.
    displaycolumns.remove("ID")
    table.ColumnsToDisplay = displaycolumns                       #  Again found and used from the internet.
    table.Widget.configure(displaycolumns=displaycolumns)         #  https://stackoverflow.com/questions/70263893/deleting-hiding-a-column-of-a-table-in-pysimplegui

    return win


