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

"""  A place to hold all the common project paths.
     Also, holds some common constants used in the project.
"""
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

contacts_data_file   = r"data/contacts"

#  Colours for the reminder background.
GREEN  = "#B9DA8C"
YELLOW = "#D7DA97"
BLUE   = "#00FDFF"
RED    = "#DA8C8C"
BLACK  = "#000000"

#  fields in the reminder items list.
REMINDER_ID           = 0
REMINDER_TIME_LEFT    = 1
REMINDER_DISP_LEFT    = 2
REMINDER_EVENT        = 3
REMINDER_DESCRIPTION  = 4
REMINDER_DATE_DUE     = 5
REMINDER_TIME_DUE     = 6
REMINDER_AUTO_DELETE  = 7
REMINDER_RECURRING    = 8
REMINDER_DISPLAYED    = 9
REMINDER_05_DAYS      = 10
REMINDER_15_DAYS      = 11
REMINDER_30_DAYS      = 12

#  fields in the contact items list
CONTACT_ID          = 0
CONTACT_TITLE       = 1
CONTACT_LAST_NAME   = 2
CONTACT_MIDDLE_NAME = 3
CONTACT_FIRST_NAME  = 4
CONTACT_TEL_NO      = 5
CONTACT_EMAIL       = 6
CONTACT_DOB         = 7
CONTACT_HOUSE_NO    = 8
CONTACT_STREET      = 9
CONTACT_ADDRESS_1   = 10
CONTACT_ADDRESS_2   = 11
CONTACT_COUNTY      = 12
CONTACT_POST_CODE   = 13
CONTACT_COUNTRY     = 14
CONTACT_NOTE        = 14





