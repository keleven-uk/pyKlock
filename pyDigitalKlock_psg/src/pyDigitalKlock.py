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

from tkinter.colorchooser import askcolor

import datetime

import src.utils.pyDigitalKlock_utils as utils

def main():
    txt_colour = "black"                        #  Default or initial foreground colour for the text labels.
    sg.theme('LightGreen4')                     #  Default of initial theme.
    sg.SetOptions(element_padding=(0, 0))

    # Create the Window
    window = win_layout()

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read(timeout=1000)

        if event in (sg.WIN_CLOSED, 'Quit'):                        # if user closes window or clicks quit
            break

        strNow = datetime.datetime.now()
        window['-CURRENT_TIME-'].update(f"{strNow:%H:%M:%S}")
        window['-CURRENT-STATUS-'].update(f"{utils.get_state()}")
        window['-CURRENT-DATE-'].update(f"{ strNow:%A %d %B %Y}")
        window['-CURRENT-IDLE-'].update(utils.get_idle_duration())

        match event:
            case "About":
                window.disappear()
                sg.popup('pyDigitalKlock', 'Version 2022.26', 'PySimpleGUI Version', sg.version,  grab_anywhere=True)
                window.reappear()
            case "Foreground":
                window.disappear()
                for_colour = askcolor(title="Choose colour of foreground")
                txt_colour = for_colour[1]
                update_text_colour(window, txt_colour)
                window.reappear()
            case "Background":
                window.disappear()
                bac_colour = askcolor(title="Choose colour of background")
                sg.theme_background_color(bac_colour[1])
                sg.theme_element_background_color(bac_colour[1])
                sg.theme_text_element_background_color(bac_colour[1])
                window = win_layout()
                update_text_colour(window, txt_colour)
                window.reappear()

    window.close()


def update_text_colour(window, txt_colour):
    """  Set the foreground colour of the text labels to the specified colour.

         It seems that the theme text foreground call doesn't work.
    """
    window['-CURRENT_TIME-'].update(text_color=txt_colour)
    window['-CURRENT-STATUS-'].update(text_color=txt_colour)
    window['-CURRENT-DATE-'].update(text_color=txt_colour)
    window['-CURRENT-IDLE-'].update(text_color=txt_colour)


def win_layout():
    """  Sets up the windows and menu layout.
         Returns a finalized windows object.

         In it's own def so that it can be easily called twice.
         This is so the windows can be re done after a background colour change.
         A bit klunky, but a work around to reload the theme at run time.
    """
    strNow = datetime.datetime.now()

    menu_def = [["File",  ["Quit"]],
                ["Colour",["Foreground", "Background", "Transparent"]],
                ["Font",  ["Font"]],
                ["Help",  ["License", "About"]]
               ]

    layout = [[sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
              [sg.Text(f"{strNow:%H:%M:%S}",      justification="center", key="-CURRENT_TIME-", font=("Twobit",72))],   #  Current time.
              [sg.Text(f"{strNow:%A %d %B %Y}",   justification="left",   key="-CURRENT-DATE-"),   sg.Push(),           #  Current Date
               sg.Text(f"{utils.get_state()}",    justification="center", key="-CURRENT-STATUS-"), sg.Push(),           #  Current status.
               sg.Text(utils.get_idle_duration(), justification="right",  key="-CURRENT-IDLE-")],                       #  Current idle time.
             ]

    #window = sg.Window('Window Title', layout, no_titlebar=True, alpha_channel=0.5)
    win =  sg.Window('L.E.D. Klock', layout, alpha_channel=0.6, size=(400, 150))
    win.finalize()
    win.keep_on_top_set()

    return win


if __name__ == '__main__':
    #  Call main is script is run directly.
    main()
