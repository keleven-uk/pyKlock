###############################################################################################################
#     notification.py   Copyright (C) <2022>  <Kevin Scott>                                                   #                                                                                                             #                                                                                                             #
#     displays a toast [pop up] notification.                                                                 #
#                                                                                                             #
#     For changes see history.txt                                                                             #
#                                                                                                             #
###############################################################################################################
#    Copyright (C) <2022>  <Kevin Scott>                                                                      #
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

import winsound

import PySimpleGUI as sg


GREEN  = "#B9DA8C"
YELLOW = "#D7DA97"
BLUE   = "#00FDFF"
RED    = "#DA8C8C"
BLACK  = "#000000"


"""  Displays a toast [pop up] notification.

     The message, x_pos, y_pos and background colour can be specified.
"""

def popup(message, x_pos, y_pos, reminder_colour):
    #  Play a sound when popup is called.
    #  This can fail if system sounds are disabled - hence the try finally block.
    try:
        winsound.PlaySound("Notification", winsound.SND_ALIAS)
    finally:
        sg.Window("", [[sg.Text(message, background_color=reminder_colour, text_color=BLACK)],
                      [sg.Button("Clear", key="-REMINDER_CLEAR-")]],
                       background_color=reminder_colour,
                       location=(x_pos, y_pos),
                       size=(600,60),
                       no_titlebar=True,
                       alpha_channel=0.6,
                       finalize=True,
                       keep_on_top=True)





