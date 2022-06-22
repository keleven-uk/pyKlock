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


import src.contacts.contacts as contacts

from src.projectPaths import *

def run_contacts(window, contacts_db, mode="", line_no=-1):
    """  A Simple dialog.
         Collects the data for a contact - key, description, date/time due.

         if window is True then display window - if false just return list of contacts.
         Mode will be default[""] to display window,
            mode = "EDIT" will allow the contact to be edited,
            mode = "DELETE" will delete the contact.
        line_no will gibe the row number of the contact to edited/deleted.
    """

    if window:

        sg.theme("SandyBeach")

        layout = [
            [sg.Text("Please enter your contact", key="-FORM_TEXT-")],
            [sg.Text("Last Name",   size =(15, 1)), sg.InputText(key="-CONTACT-LAST-NAME-")],
            [sg.Text("Middle Name", size =(15, 1)), sg.InputText(key="-CONTACT-MIDDLE-NAME-")],
            [sg.Text("First Name",  size =(15, 1)), sg.InputText(key="-CONTACT-LAST-NAME-")],
            [sg.Button("Delete", key="-DELETE-",  visible=False), sg.Button("Submit", key="-SUBMIT-",  visible=True), sg.Cancel()]
            ]

        #  Create window
        rem_window = sg.Window("contacts", layout)
        rem_window.finalize()

        #  get_contact returns a list of the attributes of the reminder
        #  position 0 = ID
        #           1 = Last Name
        #           2 = First Name
        #           3 = Tel. No.
        #           4 = D.O.B.
        #           5 = Address
        #           6 = Post Code

        if mode in ("EDIT", "DELETE"):
            disp_contacts = contacts_db.get_contact(str(line_no))      #  now a list.
            hrs, min = disp_reminder[TIME_DUE].split(":")

            reminder_displayed = disp_reminder[DISPLAYED]
            auto_delete        = ru.str_to_bool(disp_reminder[AUTO_DELETE])
            recurring          = ru.str_to_bool(disp_reminder[RECURRING])


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
                    last_name   = values["-CONTACT-LAST-NAME-"]
                    middle_name = values["-CONTACT-MIDDLE-NAME-"]
                    first_name  = values["-CONTACT-LAST-NAME-"]


                    items = [str(line_no), last_name, middle_name, first_name]

                    if mode == "EDIT":
                        contacts_db.save(items)
                    else:
                        contacts_db.add(items)
                    break
                case "-DELETE-":
                    choice = sg.popup_ok_cancel('Do you really want to delete?')
                    if choice == "OK":
                        contacts_db.delete(str(line_no))

                    break

        rem_window.close(); del rem_window

    return contacts_db.list_contacts()





