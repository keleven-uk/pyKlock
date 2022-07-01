###############################################################################################################
#    fonts.py   Copyright (C) <2022>  <Kevin Scott>                                                           #                                                                                                             #                                                                                                             #
#     The font GUI layout and supporting functions.                                                           #
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

from datetime import datetime

import src.reminder.reminder as reminder
import src.reminder.reminder_utils as ru

from src.projectPaths import *

def run_reminders(window, reminder_db, mode="", line_no=-1):
    """  A Simple dialog.
         Collects the data for a reminder - key, description, date/time due.

         if window is True then display window - if false just return list of reminders.
         Mode will be default[""] to display window,
            mode = "EDIT" will allow the reminder to be edited,
            mode = "DELETE" will delete the reminder.
        line_no will gibe the row number of the reminder to edited/deleted.

        #  fields in the reminder items list.
            REMINDER_ID           = 0
            REMINDER_EVENT        = 1
            REMINDER_DESCRIPTION  = 2
            REMINDER_DATE_DUE     = 3
            REMINDER_TIME_DUE     = 4
            REMINDER_AUTO_DELETE  = 5
            REMINDER_RECURRING    = 6
            REMINDER_DISPLAYED    = 7

    """

    current_hour   = datetime.now().hour
    current_minute = datetime.now().minute

    if window:
        #  Create the reminder event type list.
        events = ru.get_events()

        sg.theme("SandyBeach")

        layout = [
            [sg.Text("Please enter your reminder", key="-FORM_TEXT-")],
            [sg.Text("Event",       size=(15, 1)), sg.Combo(events, key="-REMIDER_EVENT-", default_value=events[0], font=("TkDefaultFont", 10))],
            [sg.Text("Description", size=(15, 1)), sg.InputText(key="-REMINDER_DESCRIPTION-")],
            [sg.Text("Date Due",    size=(15, 1)), sg.Input(key="-REMINDER_DATE_DUE-", size=(20,1)),
             sg.CalendarButton("Choose Date",      target="-REMINDER_DATE_DUE-",       format="%d %B %Y")],
            [sg.Text("Time Due",    size =(15, 1)),
             sg.Spin([x for x in range(24)], key="-REMINDER_DUE_TIME_HOURS-", size=(6,1),  font=("TkDefaultFont", 12), initial_value=current_hour,   readonly=True),
             sg.Spin([x for x in range(60)], key="-REMINDER_DUE_TIME_MINS-",  size=(6,1),  font=("TkDefaultFont", 12), initial_value=current_minute, readonly=True)],
            [sg.Text("Recurring reminder", size=(15, 1), justification="right"), sg.Checkbox("", key="-REMINDER_RECURRING-",   default=False),
             sg.Text("Auto Delete",        size=(15, 1), justification="right"), sg.Checkbox("", key="-REMINDER_AUTO_DELETE-", default=False)],
            [sg.Button("Delete", key="-DELETE-",  visible=False, pad=(1,1)), sg.Button("Submit", key="-SUBMIT-",  visible=True, pad=(1,1)), sg.Cancel(pad=(1,1))]
            ]

        #  Create window
        rem_window = sg.Window("Reminders", layout)
        rem_window.finalize()

        if mode in ("EDIT", "DELETE"):
            disp_reminder = reminder_db.get_reminder(str(line_no))      #  now a list.
            hrs, min = disp_reminder[REMINDER_TIME_DUE].split(":")

            reminder_displayed = disp_reminder[REMINDER_DISPLAYED]
            auto_delete        = ru.str_to_bool(disp_reminder[REMINDER_AUTO_DELETE])
            recurring          = ru.str_to_bool(disp_reminder[REMINDER_RECURRING])

            rem_window["-FORM_TEXT-"].update("Please chose your reminder to EDIT")
            rem_window["-REMIDER_EVENT-"].update(value=disp_reminder[REMINDER_EVENT])
            rem_window["-REMINDER_DESCRIPTION-"].update(disp_reminder[REMINDER_DESCRIPTION])
            rem_window["-REMINDER_DATE_DUE-"].update(disp_reminder[REMINDER_DATE_DUE])
            rem_window["-REMINDER_DUE_TIME_HOURS-"].update(value=hrs)
            rem_window["-REMINDER_DUE_TIME_MINS-"].update(value=min)
            rem_window["-REMINDER_AUTO_DELETE-"].update(REMINDER_AUTO_DELETE)
            rem_window["-REMINDER_RECURRING-"].update(REMINDER_RECURRING)

        if mode == "DELETE":
            rem_window["-FORM_TEXT-"].update("Please chose your reminder to DELETE")
            rem_window["-DELETE-"].update(visible=True)
            rem_window["-SUBMIT-"].update(visible=False)

        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = rem_window.read(timeout=1000)

            match event:
                case (sg.WIN_CLOSED|"Cancel"):
                    break
                case "-SUBMIT-":
                    event              = values["-REMIDER_EVENT-"]
                    description        = values["-REMINDER_DESCRIPTION-"].capitalize()
                    date_due           = values["-REMINDER_DATE_DUE-"]
                    hrs                = values["-REMINDER_DUE_TIME_HOURS-"]
                    mns                = values["-REMINDER_DUE_TIME_MINS-"]
                    time_due           = f"{hrs:02}:{mns:02}"
                    auto_delete        = str(values["-REMINDER_AUTO_DELETE-"])
                    recurring          = str(values["-REMINDER_RECURRING-"])
                    reminder_displayed = "False"

                    if recurring == "True":                                         #  If recurring, check date is in the past,
                        date_due = ru.check_date(values["-REMINDER_DATE_DUE-"])     #  if so add one year.

                    items = [str(line_no), event, description, date_due, time_due, auto_delete, recurring, reminder_displayed]

                    if mode == "EDIT":
                        reminder_db.save(items)
                    else:
                        reminder_db.add(items)
                    break
                case "-DELETE-":
                    choice = sg.popup_ok_cancel('Do you really want to delete?')
                    if choice == "OK":
                        reminder_db.delete(str(line_no))

                    break

        rem_window.close(); del rem_window

    return reminder_db.list_reminders()





