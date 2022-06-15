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
#  Some of the paths needs to be the working directory.
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    CONFIG_PATH   = "config.toml"
    LOGGER_PATH   = "pyKlock.log"
    FONTS_PATH    = "fonts"
    RESOURCE_PATH = "resources"
    DATA_PATH     = "data"
else:
    CONFIG_PATH   = MAIN_PATH / "config.toml"
    LOGGER_PATH   = MAIN_PATH / "logs/pyKlock.log"
    FONTS_PATH    = MAIN_PATH / "fonts"
    RESOURCE_PATH = MAIN_PATH / "resources"
    DATA_PATH     = MAIN_PATH / "data"


#  Use raw strings, when compiled using pyinstaller, does not like paths.
start_image  = r"resources/Start.png"
resume_image = r"resources/Resume.png"
stop_image   = r"resources/Stop.png"
pause_image  = r"resources/Pause.png"
clear_image  = r"resources/Clear.png"
klock_icon   = r"resources/Klock.ico"

backward_file_path   = r"data/backward"
reminder_data_file   = r"data/reminders"
reminder_events_file = r"data/events.txt"

#  fields in the items list.
ID           = 0
EVENT        = 1
DESCRIPTION  = 2
DATE_DUE     = 3
TIME_DUE     = 4
AUTO_DELETE  = 5
RECURRING    = 6
DISPLAYED    = 7

