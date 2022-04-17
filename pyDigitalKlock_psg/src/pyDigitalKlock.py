###############################################################################################################
#    pyDigitalKlock   Copyright (C) <2022>  <Kevin Scott>                                                     #                                                                                                             #                                                                                                             #
#     An attempt to re-create a LCD Klock [using pySimpleGUI].                                                #
#                                                                                                             #
#     For changes see history.txt                                                                             #
#                                                                                                             #
###############################################################################################################
#    Copyright (C) <2020-2021>  <2022>                                                                        #
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

import src.utils.pyDigitalKlock_utils as utils

def main():
    sg.theme('LightGreen4')
    sg.SetOptions(element_padding=(0, 0))
    strNow = datetime.datetime.now()

    layout = [[sg.Text(f"{strNow:%H:%M:%S}", font=("Twobit",72), key="-CURRENT_TIME-", justification="center")],   #  Current time.
              [sg.Text(f"{strNow:%A %d %B %Y}", justification="left", key="-CURRENT-DATE-"), sg.Push(),            #  Current Date
               sg.Text(f"{utils.get_state()}", justification="center", key="-CURRENT-STATUS-"), sg.Push(),         #  Current status.
               sg.Text(utils.get_idle_duration(), justification="right", key="-CURRENT-IDLE-")],                   #  Current idle time.
             ]

    # Create the Window
    #window = sg.Window('Window Title', layout, no_titlebar=True, alpha_channel=0.5)
    window = sg.Window('L.E.D. Klock', layout, alpha_channel=0.6, size=(400, 150))


    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read(timeout=1000)

        if event in (sg.WIN_CLOSED, 'Exit'):                        # if user closes window or clicks cancel
            break

        strNow = datetime.datetime.now()
        window['-CURRENT_TIME-'].update(f"{strNow:%H:%M:%S}")
        window['-CURRENT-STATUS-'].update(f"{utils.get_state()}")
        window['-CURRENT-DATE-'].update(f"{ strNow:%A %d %B %Y}")
        window['-CURRENT-IDLE-'].update(utils.get_idle_duration())

    window.close()


if __name__ == '__main__':
    main()
