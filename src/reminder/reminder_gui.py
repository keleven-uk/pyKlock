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

import src.reminder.reminder as reminder
import src.reminder.reminder_utils as ru


def run_reminders(window, mode="",  line_no=-1):
    """  A Simple dialog.
         Collects the data for a reminder - key, description, date/time due.

         if window is True then display window - if false just return list of reminders.
         Mode will be default[""] to display window,
            mode = "EDIT" will allow the reminder to be edited,
            mode = "DELETE" will delete the reminder.
        line_no will gibe the row number of the reminder to edited/deleted.
    """

    #  Create reminders database
    reminder_db    = reminder.reminders()

    if window:
        #  Create the reminder event type list.
        events = ru.get_events()

        sg.theme("SandyBeach")

        layout = [
            [sg.Text("Please enter your reminder", key="-FORM_TEXT-")],
            [sg.Text("Event",       size =(15, 1)),sg.Combo(events, key="-REMIDER_EVENT-", default_value=events[0], size=(14,1),  font=("TkDefaultFont", 10))],
            [sg.Text("Description", size =(15, 1)), sg.InputText(key="-REMINDER_DESCRIPTION-")],
            [sg.Text("Date Due",    size =(15, 1)), sg.Input(key="-REMINDER_DATE_DUE-", size=(20,1)),
            sg.CalendarButton("Choose Date",  target="-REMINDER_DATE_DUE-", format="%d-%m-%y")],
            [sg.Text("Time Due",          size =(15, 1)),
            sg.Spin([x+1 for x in range(23)], key="-REMINDER_DUE_TIME_HOURS-", size=(6,1),  font=("TkDefaultFont", 12), initial_value=0),
            sg.Spin([x+1 for x in range(59)], key="-REMINDER_DUE_TIME_MINS-",  size=(6,1),  font=("TkDefaultFont", 12), initial_value=0)],
            [sg.Text("Recuring reminder", size =(15, 1)), sg.Checkbox("", key="-REMINDER_RECURING-", default=False)],
            [sg.Submit(), sg.Cancel()]
            ]

        #  Create window
        window = sg.Window("Reminders", layout)
        window.finalize()

        #  get_reminder returns a list of the attributes of the reminder
        #  position 0 = ID
        #           1 = reminder type
        #           2 = reminder description
        #           3 = reminder due date
        #           4 = reminder due time
        #           5 = reminder recuring

        if mode == "EDIT":
            disp_reminder = reminder_db.get_reminder(str(line_no+1))
            hrs, min = disp_reminder[4].split(":")

            window["-FORM_TEXT-"].update("Please edit your reminder")
            window["-REMIDER_EVENT-"].update(value=disp_reminder[1])
            window["-REMINDER_DESCRIPTION-"].update(disp_reminder[2])
            window["-REMINDER_DATE_DUE-"].update(disp_reminder[3])
            window["-REMINDER_DUE_TIME_HOURS-"].update(value=hrs)
            window["-REMINDER_DUE_TIME_MINS-"].update(value=min)
            window["-REMINDER_RECURING-"].update(disp_reminder[5])


        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window.read(timeout=1000)

            match event:
                case (sg.WIN_CLOSED|"Cancel"):
                    break
                case "Submit":
                    event       = values["-REMIDER_EVENT-"]
                    description = values["-REMINDER_DESCRIPTION-"]
                    date_due    = values["-REMINDER_DATE_DUE-"]
                    hrs         = values["-REMINDER_DUE_TIME_HOURS-"]
                    mns         = values["-REMINDER_DUE_TIME_MINS-"]
                    time_due    = f"{hrs}:{mns}"
                    recuring    = values["-REMINDER_RECURING-"]

                    new_reminder = reminder.reminder(event, description, date_due, time_due, recuring)

                    if mode == "EDIT":
                        reminder_db.save(str(line_no+1), event, description, date_due, time_due, recuring)
                    else:
                        reminder_db.add(new_reminder)

                    break


        window.close(); del window

    return reminder_db.list_reminders()





