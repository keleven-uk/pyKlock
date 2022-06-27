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

        #  fields in the contact items list
            CONTACT_ID          = 0
            CONTACT_TITLE       = 1
            CONTACT_LAST_NAME   = 2
            CONTACT_MIDDLE_NAME = 3
            CONTACT_FIRST_NAME  = 4
            CONTACT_TEL_NO      = 5
            CONTACT_EMAIL       = 6
            CONTACT_DOB         = 7
            CONTACT_HOUSE_NO    = 8
            CONTACT_STREET      = 9
            CONTACT_ADDRESS_1   = 10
            CONTACT_ADDRESS_2   = 11
            CONTACT_COUNTY      = 12
            CONTACT_POST_CODE   = 13
            CONTACT_COUNTRY     = 14
            CONTACT_NOTE        = 14
    """

    if window:

        sg.theme("SandyBeach")

        layout = [
            [sg.Text("Please enter your contact", key="-FORM_TEXT-")],
            [sg.Text("")],
            [sg.Text("Title          ", size=(12, 1)), sg.InputText(key="-CONTACT-TITLE-",       size=(18, 1)),
             sg.Text("Last Name      ", size=(12, 1)), sg.InputText(key="-CONTACT-LAST-NAME-",   size=(18, 1))],
            [sg.Text("Middle Name    ", size=(12, 1)), sg.InputText(key="-CONTACT-MIDDLE-NAME-", size=(18, 1)),
             sg.Text("First Name     ", size=(12, 1)), sg.InputText(key="-CONTACT-FIRST-NAME-",  size=(18, 1))],
            [sg.Text("Tel. No.       ", size=(12, 1)), sg.InputText(key="-CONTACT-TEL-NO-",      size=(18, 1)),
             sg.Text("eMail          ", size=(12, 1)), sg.InputText(key="-CONTACT-EMAIL-",       size=(18, 1))],
            [sg.Text("D.O.B.         ", size=(12, 1)), sg.InputText(key="-CONTACT-DOB-",         size=(18, 1)),
             sg.Text("               ", size=(12, 1)), sg.CalendarButton("Choose Date",          target="-CONTACT-DOB-", format="%d %B %Y")],
            [sg.Text("House No.      ", size=(12, 1)), sg.InputText(key="-CONTACT-HOUSE-NO-",    size=(18, 1)),
             sg.Text("Street         ", size=(12, 1)), sg.InputText(key="-CONTACT-STREET-",      size=(18, 1))],
            [sg.Text("Address Line 1 ", size=(12, 1)), sg.InputText(key="-CONTACT-ADDRESS-1-",   size=(18, 1)),
             sg.Text("Address Line 2 ", size=(12, 1)), sg.InputText(key="-CONTACT-ADDRESS-2-",   size=(18, 1))],
            [sg.Text("County         ", size=(12, 1)), sg.InputText(key="-CONTACT-COUNTY-",      size=(18, 1)),
             sg.Text("Post Code      ", size=(12, 1)), sg.InputText(key="-CONTACT-POST-CODE-",   size=(18, 1))],
            [sg.Text("Country        ", size=(12, 1)), sg.InputText(key="-CONTACT-COUNTRY-",     size=(18, 1))],
            [sg.Text("Note           ", size=(12, 1)), sg.InputText(key="-CONTACT-NOTE-",        size=(51, 1))],
            [sg.Text("")],
            [sg.Button("Delete", key="-DELETE-",  visible=False, pad=(1,1)), sg.Button("Submit", key="-SUBMIT-",  visible=True, pad=(1,1)), sg.Cancel(pad=(1,1))]
            ]

        #  Create window
        contact_window = sg.Window("contacts", layout)
        contact_window.finalize()

        if mode in ("EDIT", "DELETE"):
            disp_contacts = contacts_db.get_contact(str(line_no))      #  now a list.

            contact_window["-CONTACT-TITLE-"].update(disp_contacts[CONTACT_TITLE])
            contact_window["-CONTACT-LAST-NAME-"].update(disp_contacts[CONTACT_LAST_NAME])
            contact_window["-CONTACT-MIDDLE-NAME-"].update(disp_contacts[CONTACT_MIDDLE_NAME])
            contact_window["-CONTACT-FIRST-NAME-"].update(disp_contacts[CONTACT_FIRST_NAME])
            contact_window["-CONTACT-TEL-NO-"].update(disp_contacts[CONTACT_TEL_NO])
            contact_window["-CONTACT-EMAIL-"].update(disp_contacts[CONTACT_EMAIL])
            contact_window["-CONTACT-DOB-"].update(disp_contacts[CONTACT_DOB])
            contact_window["-CONTACT-HOUSE-NO-"].update(disp_contacts[CONTACT_HOUSE_NO])
            contact_window["-CONTACT-STREET-"].update(disp_contacts[CONTACT_STREET])
            contact_window["-CONTACT-ADDRESS-1-"].update(disp_contacts[CONTACT_ADDRESS_1])
            contact_window["-CONTACT-ADDRESS-2-"].update(disp_contacts[CONTACT_ADDRESS_2])
            contact_window["-CONTACT-COUNTY-"].update(disp_contacts[CONTACT_COUNTY])
            contact_window["-CONTACT-POST-CODE-"].update(disp_contacts[CONTACT_POST_CODE])
            contact_window["-CONTACT-COUNTRY-"].update(disp_contacts[CONTACT_COUNTRY])
            contact_window["-CONTACT-NOTE-"].update(disp_contacts[CONTACT_NOTE])


        if mode == "DELETE":
            contact_window["-FORM_TEXT-"].update("Please chose your reminder to DELETE")
            contact_window["-DELETE-"].update(visible=True)
            contact_window["-SUBMIT-"].update(visible=False)

        # Event Loop to process "contacts" and get the "values" of the inputs
        while True:
            event, values = contact_window.read(timeout=1000)

            match event:
                case (sg.WIN_CLOSED|"Cancel"):
                    break
                case "-SUBMIT-":
                    title       = values["-CONTACT-TITLE-"].capitalize()
                    last_name   = values["-CONTACT-LAST-NAME-"].capitalize()
                    middle_name = values["-CONTACT-MIDDLE-NAME-"].capitalize()
                    first_name  = values["-CONTACT-FIRST-NAME-"].capitalize()
                    tel_no      = values["-CONTACT-TEL-NO-"]
                    email       = values["-CONTACT-EMAIL-"]
                    dob         = values["-CONTACT-DOB-"]
                    house_no    = values["-CONTACT-HOUSE-NO-"]
                    street      = values["-CONTACT-STREET-"].title()
                    add_1       = values["-CONTACT-ADDRESS-1-"].title()
                    add_2       = values["-CONTACT-ADDRESS-2-"].title()
                    county      = values["-CONTACT-COUNTY-"].title()
                    post_code   = values["-CONTACT-POST-CODE-"].upper()
                    country     = values["-CONTACT-COUNTRY-"].title()
                    note        = values["-CONTACT-NOTE-"]

                    items = [str(line_no), title, last_name, middle_name, first_name, tel_no, email, dob, house_no, street, add_1, add_2, county, post_code, country, note]

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

        contact_window.close(); del contact_window

    return contacts_db.list_contacts()





