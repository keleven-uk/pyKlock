###############################################################################################################
#    klock.py   Copyright (C) <2022>  <Kevin Scott>                                                           #                                                                                                             #                                                                                                             #
#     The klock GUI layout and supporting functions.                                                          #
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

import src.utils.pyDigitalKlock_utils as utils

def update_text_colour(window, txt_colour):
    """  Set the foreground colour of the text labels to the specified colour.

         It seems that the theme text foreground call doesn't work.
    """
    window['-CURRENT_TIME-'].update(text_color=txt_colour)
    window['-CURRENT-STATUS-'].update(text_color=txt_colour)
    window['-CURRENT-DATE-'].update(text_color=txt_colour)
    window['-CURRENT-IDLE-'].update(text_color=txt_colour)


def update_text(window):
    strNow = datetime.datetime.now()
    window['-CURRENT_TIME-'].update(f"{strNow:%H:%M:%S}")
    window['-CURRENT-STATUS-'].update(f"{utils.get_state()}")
    window['-CURRENT-DATE-'].update(f"{ strNow:%A %d %B %Y}")
    window['-CURRENT-IDLE-'].update(utils.get_idle_duration())


def win_layout(win_colour, txt_colour, my_config, transparent=False, change_theme=False):
    """  Sets up the windows and menu layout.
         Returns a finalized windows object.

         In it's own def so that it can be easily called twice.
         This is so the windows can be re done after a background colour change.
         A bit klunky, but a work around to reload the theme at run time and to set transparency.
    """
    win_location = (my_config.X_POS, my_config.Y_POS)
    win_size     = (400, 150)

    if not change_theme:                                    #  If changing theme, ignore foreground and background colours.
        sg.theme_background_color(win_colour)               #  Sets all the backgrounds to win_colour [background colour]
        sg.theme_element_background_color(win_colour)
        sg.theme_text_element_background_color(win_colour)

    strNow = datetime.datetime.now()

    #  Change the menu text to reflect transparency or to set back to normal.
    if transparent:
        menu_def = [["File",  ["Quit"]],
                    ["Colour",["Foreground", "Background", "Theme", "Normal"]],
                    ["Font",  ["Font"]],
                    ["Help",  ["License", "About"]]
                   ]
    else:
        menu_def = [["File",  ["Quit"]],
                    ["Colour",["Foreground", "Background", "Theme", "Transparent"]],
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
    if transparent:
        win =  sg.Window('L.E.D. Klock', layout, alpha_channel=0.6, location=win_location, size= win_size, transparent_color=win_colour, no_titlebar=True)
    else:
        win =  sg.Window('L.E.D. Klock', layout, alpha_channel=0.6, location=win_location, size= win_size, no_titlebar=True)

    win.finalize()
    win.keep_on_top_set()

    if not change_theme:                                    #  If changing theme, ignore foreground and background colours.
        update_text_colour(win, txt_colour)                 #  Set all text foreground colour to txt_colour.

    #  Update current time to saved font.
    win['-CURRENT_TIME-'].update(font=(my_config.FONT_NAME, my_config.FONT_SIZE))

    #  Bind mouse, so klock can be moved.
    win.bind("<Button-1>", "-STARTMOVE-")
    win.bind("<ButtonRelease-1>", "-STOPMOVE-")
    win.bind("<B1-Motion>", "-MOVING-")

    return win


