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

import datetime

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


def check_date(date_due):
    """  If the reminder is recurring, check that the date is in the future.
         A recurring date could be entered with correct day and month, but with a
         current year.  It date is in the past add one to the year.
    """
    _now = datetime.datetime.now()
    _due = datetime.datetime.strptime(date_due, "%d %B %Y")

    if _due < _now:
        return add_one_year(_due)
    else:
        return date_due



def add_one_year(due):
    """  Add one year to date.
    """
    if due.month == 2 and due.day == 29:                            #  If current date is 29 February in a leap year,
        new_date = due.replace(year=due.year + 1, day=28)           #  make the future day 28 February.
    else:
        new_date = due.replace(year=due.year + 1)

    return new_date.strftime ("%d %B %Y")


def str_to_bool(s):
    """  Converts to strings 'True' and 'False' to their Boolean equivalents.
         bool() doesn't work with mu strings
    """
    if s == 'True':
         return True
    elif s == 'False':
         return False


def format_minutes(minutes):
    """  Formats number of minutes into a human readable form i.e. days:hours:minutes
    """

    days  = int (minutes / 1440)
    hours = int (minutes % 1440 / 60)
    mins  = int (minutes % 60)

    return f"{days:3}:{hours:2}:{mins:2}"




