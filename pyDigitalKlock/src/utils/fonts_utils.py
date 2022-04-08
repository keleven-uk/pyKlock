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

import os
import shutil
import ctypes
from ctypes import wintypes
import sys
import ntpath
try:
    import winreg
except ImportError:
    import _winreg as winreg

from src.projectPaths import *

from tkinter import font

def list_fonts():
    """  Create a list of all fonts in a given directory.
         Assumes font files end in .ttf.
    """
    path      = pathlib.Path(FONTS_PATH)
    lst_fonts = list(path.rglob("*.ttf"))

    return lst_fonts


def check_font():
    """  Quick check to see if the digital font is present.

         NB : the font file name must be the same as the font name **git status
    """
    for font_path in list_fonts():
        f_name = str(font_path.stem)
        if f_name in font.families():
            print(f" {f_name} font found")
        else:
            print(f" {f_name} font NOT found")
            install_font(font_path)


def set_font(pos):
    """   return a font object and position pois in the font list.
    """
    lst_fonts = list_fonts()
    font_name = f"72{lst_fonts[pos].stem}"
    print(font_name)

    ret_font = font.Font(family=font_name, size=72, weight="normal")
    return ret_font


def install_font(src_path):
    """  copy the font to the Windows Fonts folder

         Found at https://gist.github.com/tushortz/598bf0324e37033ed870c4e46461fb1e
    """

    dst_path = os.path.join(os.environ['SystemRoot'], 'Fonts',
                            os.path.basename(src_path))
    shutil.copy(src_path, dst_path)
    # load the font in the current session
    if not gdi32.AddFontResourceW(dst_path):
        os.remove(dst_path)
        raise WindowsError('AddFontResource failed to load "%s"' % src_path)
    # notify running programs
    user32.SendMessageTimeoutW(HWND_BROADCAST, WM_FONTCHANGE, 0, 0,
                               SMTO_ABORTIFHUNG, 1000, None)
    # store the fontname/filename in the registry
    filename = os.path.basename(dst_path)
    fontname = os.path.splitext(filename)[0]
    # try to get the font's real name
    cb = wintypes.DWORD()
    if gdi32.GetFontResourceInfoW(filename, ctypes.byref(cb), None,
                                  GFRI_DESCRIPTION):
        buf = (ctypes.c_wchar * cb.value)()
        if gdi32.GetFontResourceInfoW(filename, ctypes.byref(cb), buf,
                                      GFRI_DESCRIPTION):
            fontname = buf.value
    is_truetype = wintypes.BOOL()
    cb.value = ctypes.sizeof(is_truetype)
    gdi32.GetFontResourceInfoW(filename, ctypes.byref(cb),
                               ctypes.byref(is_truetype), GFRI_ISTRUETYPE)
    if is_truetype:
        fontname += ' (TrueType)'
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, FONTS_REG_PATH, 0,
                        winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, fontname, 0, winreg.REG_SZ, filename)
