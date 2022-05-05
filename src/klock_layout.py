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


def win_layout(my_config, win_location, win_size, timetypes):
    """  Sets up the windows and menu layout.
         Returns a finalized windows object.

         In it's own def so that it can be easily called multiple times.
         This is so the windows can be re done after a layout change.
         A bit klunky, but a work around to reload the theme at run time and to set transparency.
    """
    strNow = datetime.datetime.now()

    #  Change the menu text to reflect transparency or to set back to normal.

    menu_def = [["File",  ["Theme", "---", "Quit"]],
                ["Help",  ["License", "About"]]
                ]

    fuzzy_left_row_layout= [[sg.Combo(list(timetypes), key="-TIME_TYPES-", default_value="Fuzzy Time")]
                           ]

    fuzzy_right_row_layout = [[sg.Text("00:00:00", key="-CURRENT_TIME-", font=("Twobit",28))]
                             ]

    fuzzy_time_layout = [[sg.Text("Fuzzy Time")],
                         [sg.Text(" ")],
                         [sg.Frame("", layout=fuzzy_left_row_layout), sg.Text(" "), sg.Frame("", layout=fuzzy_right_row_layout, size=(680, 55))]
                        ]

    world_klock_layout = [[sg.Text("World Klock")],
                          [sg.Text("World Klock"), sg.Button("1")]
                         ]

    countdown_layout = [[sg.Text("Countdown")],
                        [sg.Text("Countdown"), sg.Button("1")]
                       ]

    timer_layout = [[sg.Text("Timer")],
                    [sg.Text("Timer"), sg.Button("1")]
                   ]


    button_layout = [[sg.Button("Fuzzy Time",  key="-BTN_FUZZY-"),
                      sg.Button("World Klock", key="-BTN_WORLD-"),
                      sg.Button("Countdown",   key="-BTN_COUNTDOWN-"),
                      sg.Button("Timer",       key="-BTN_TIMER-"),
                      sg.Button("Exit",        key="-EXIT-")]]

    screen_layout = [sg.Column(fuzzy_time_layout,  visible=True,  key="-FUZZY-"),
                     sg.Column(world_klock_layout, visible=False, key="-WORLD-"),
                     sg.Column(countdown_layout,   visible=False, key="-COUNTDOWN-"),
                     sg.Column(timer_layout,       visible=False, key="-TIMER-")]

    status_bar = [[sg.Text("", justification="left",   key="-CURRENT-DATE-"),   sg.Push(),         #  Current Date
                   sg.Text("", justification="center", key="-CURRENT-STATUS-"), sg.Push(),         #  Current status.
                   sg.Text("", justification="right",  key="-CURRENT-IDLE-")]]                     #  Current idle time.

    #  Create actual layout using columns and a row of buttons
    klock_layout = [[sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
                    [screen_layout],
                    [sg.Text(" ")],
                    [sg.Frame("Choose Wisely", layout=button_layout)],
                    [status_bar]
                    ]

    #window = sg.Window('Window Title', layout, no_titlebar=True, alpha_channel=0.5)
    win =  sg.Window('pyKlock', klock_layout, location=win_location, size= win_size)

    win.finalize()

    return win


