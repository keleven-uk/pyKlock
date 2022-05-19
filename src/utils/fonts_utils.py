###############################################################################################################
#    fonts_utils.py   Copyright (C) <2022>  <Kevin Scott>                                                     #                                                                                                             #                                                                                                             #
#    utility function for fonts.py.                  .                                                        #
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


from src.projectPaths import *

from tkinter import font

from pathlib import Path

MAXIMUM_FONT_SIZE   = 40
DEFAULT_FONT_SIZE   = 32
DEFAULT_FONT_LENGTH = 510
DEFAULT_FONT_HEIGHT = 150


def list_fonts():
    """  Create a list of all fonts in a given directory.
         Assumes font files end in .ttf.
    """
    path      = pathlib.Path(FONTS_PATH)
    lst_fonts = list(path.rglob("*.ttf"))

    return lst_fonts


def check_font(font_name):
    """  Quick check to see if the font is installed on the system.

         NB : the font file name must be the same as the font name.
    """
    if font_name in font.families():
        return True
    else:
        return False


def set_font(font_name, time_type):
    """   return a font object from a font_name.
    """
    font_text   = get_font_text(time_type)
    font_length = font.Font(family=font_name, size=DEFAULT_FONT_SIZE, weight="normal").measure(font_text)
    font_height = font.Font(family=font_name, size=DEFAULT_FONT_SIZE, weight="normal").metrics("linespace")
    font_size   = int(DEFAULT_FONT_SIZE * (DEFAULT_FONT_LENGTH / font_length))

    if font_size > MAXIMUM_FONT_SIZE:
        font_size = MAXIMUM_FONT_SIZE

    #print(f"Time Type {time_type}  Font name = {font_name}  Font size = {font_size}  Font Length {font_length}  font Height {font_height}")
    ret_font = font.Font(family=font_name, size=font_size, weight="normal")
    return ret_font, font_name, font_size


def get_font_text(time_type):
    """
    """
    match time_type:
        case "Fuzzy Time":
            return "quarter past eleven in the evening"
        case "Time in Words":
            return "twelve minutes to twelve in the evening"
        case "Swatch Time":
            return "@888.88 BMT"
        case "New Earth Time":
            return "888 deg 88 mins"
        case ("Julian Time"|"Mars Sol Date"):
            return "8888888.88888"
        case "Decimal Time":
            return"88h 88m 88s"
        case ("True Hex Time"|"Hex Time"|"Oct Time"):
            return "88 88 88"
        case "Binary Time":
            return "000000 000000 000000"
        case "Roman Time":
            return "XX:LV111:XV1111"
        case "Morse Code":
            return "----- -----:----- -----:----- -----"
        case "Percent Time":
            return "88.8888 PMH"
        case "Metric Time":
            return "88.888 Kiloseconds"
        case "Unix Time":
            return "8888888888"
        case _:
            return "00:00:00"


