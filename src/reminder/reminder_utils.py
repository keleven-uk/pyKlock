###############################################################################################################
#     reminder_utils.py   Copyright (C) <2022>  <Kevin Scott>                                                 #                                                                                                             #                                                                                                             #
#     Utility functions for the reminders.                                                                    #
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

def get_events():
    """  Read a list of event types from a text file and return in list form.

         the path to the text file is held in reminder_events_file, from projectPaths
    """
    events = []
    with open (reminder_events_file) as event_file:
        for line in event_file:
            events.append(line.strip())

    return events
