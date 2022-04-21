###############################################################################################################
#    fonts.py   Copyright (C) <2022>  <Kevin Scott>                                                           #                                                                                                             #                                                                                                             #
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

from pathlib import Path

import src.utils.fonts_utils as fu

def run_fonts():
    """  A Simple dialog.
         Just displays the licence text..
    """
    font      = None
    font_name = None
    font_size = None

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
            if font_list:
                font_path = font_list[0]
            else:
                break
            font_name = f"{font_path.stem}"
            if fu.check_font(font_name):
                font, font_size = fu.set_font(font_name)           #  Returns a font object.
                break
            else:
                sg.popup_error("Font not installed, Please install and try again.\n\n Ot choose another font.")

    window.close(); del window

    return font, font_name, font_size
