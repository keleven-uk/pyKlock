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

from pathlib import Path

import src.utils.fonts_utils as fu

def run_fonts(time_type):
    """  A Simple dialog.
         Displays the contents of the font directory and allows a font to be chosen.
         If the font is installed, return the font object, if not display an error.

         fu.list_fonts() - return a list of fonts.
    """
    ret_font    = None
    font_name   = None
    font_size   = fu.DEFAULT_FONT_SIZE
    font_length = fu.DEFAULT_FONT_LENGTH
    font_height = fu.DEFAULT_FONT_HEIGHT

    sg.theme("NeutralBlue")

    layout = [[sg.Listbox(values=fu.list_fonts(), size=(80, 10), horizontal_scroll=True, select_mode="LISTBOX_SELECT_MODE_SINGLE", key="-FONT-")],
              [sg.OK(), sg.Cancel()]
             ]

    #  Create window
    window = sg.Window("Fonts", layout)

    #Event loop to process events
    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == "OK":
            font_list = window["-FONT-"].get()          #  Returns a list even though select single is specified.
            if font_list:                               #  If ok is clicked without a font chosen, an empty list is returned.
                font_path = font_list[0]
            else:
                break
            font_name = f"{font_path.stem}"                                         #  Grab the font name form the font path.
            if fu.check_font(font_name):                                            #  Check if the font is  installed.
                ret_font, font_name, font_size = fu.set_font(font_name, time_type)  #  Returns a font object.
                break
            else:
                sg.popup_error("Font not installed, Please install and try again.\n\n Ot choose another font.")

    window.close(); del window

    return ret_font, font_name, font_size
