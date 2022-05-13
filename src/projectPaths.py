###############################################################################################################
#    projectPaths.py   Copyright (C) <2022>  <Kevin Scott>                                                    #                                                                                                             #                                                                                                             #
#    Holds common directory paths for the project.                                                            #
#        Must sit in src directory                                                                            #
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

import sys
import pathlib

PROJECT_PATH  = pathlib.Path(__file__).parent
MAIN_PATH     = pathlib.Path(__file__).parent.parent

#  If running as an executable i.e. from using auto-py-to-exe.
#  Some of the paths needs to be toe working directory.
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    CONFIG_PATH   = "config.toml"
    LOGGER_PATH   = "pyDigitalKlock.log"
    FONTS_PATH    = "fonts"
    RESOURCE_PATH = "resources"
else:
    CONFIG_PATH   = MAIN_PATH / "config.toml"
    LOGGER_PATH   = MAIN_PATH / "logs/pyDigitalKlock.log"
    FONTS_PATH    = MAIN_PATH / "fonts"
    RESOURCE_PATH = MAIN_PATH / "resources"

