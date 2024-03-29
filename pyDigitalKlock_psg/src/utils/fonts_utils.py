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

DEFAULT_FONT_LENGTH = 72


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


def set_font(font_name):
    """   return a font object from a font_name.

          Adds a bit to length and width for padding and the second tow of text.
    """
    font_length = font.Font(family=font_name, size=DEFAULT_FONT_LENGTH, weight="normal").measure("00:00:00")  + 24
    font_height = font.Font(family=font_name, size=DEFAULT_FONT_LENGTH, weight="normal").metrics("linespace") + 36

    ret_font = font.Font(family=font_name, size=DEFAULT_FONT_LENGTH, weight="normal")
    return ret_font, font_name, font_length, font_height


