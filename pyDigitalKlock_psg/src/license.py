###############################################################################################################
#    license.py   Copyright (C) <2022>  <Kevin Scott>                                                         #                                                                                                             #                                                                                                             #
#     The license GUI layout and supporting functions.                                                        #
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

from src.utils.License_text import license_text

def run_license(NAME, VERSION):
    """  A Simple dialog.
         Just displays the licence text..
    """

    sg.theme("NeutralBlue")

    layout = [[sg.Multiline(key="-licence_text-", size=(60,20))],
              [sg.OK()]
             ]

    #  Create window
    window = sg.Window("Licence", layout)
    window.finalize()
    window['-licence_text-'].print(f"{NAME}     {VERSION}      Copyright (C) 2022  Kevin Scott")     # Routed to your multiline element
    window['-licence_text-'].print(license_text)

    #Event loop tp process events
    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'OK'):
            break


    window.close()
