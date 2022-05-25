###############################################################################################################
#     reminder.py   Copyright (C) <2022>  <Kevin Scott>                                                      #                                                                                                             #                                                                                                             #
#     A simple class that holds the data for a reminder.                                                             #
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

import shelve

from src.projectPaths import *


class reminder():
    """   The simple template for an individual reminder.
    """
    def __init__(self, key, description, date_due, time_due, recuring):
        self.id            = "0"
        self.reminder_name = reminder_name
        self.reminder_type = reminder_type
        self.description   = description
        self.date_due      = date_due
        self.time_due      = time_due
        self.recuring      = recuring

    def __str__(self):
        return f"{self.reminder_name}  {self.description}  {self.reminder_type} {self.date_due}  {self.time_due} {self.recuring}"



class reminders():
    """  Adds individual reminders to a reminders database.
         The reminders are stored as pickles on a shelve.
    """

    def __init__(self):
        self.no_of_reminders = 0


    def add(self, reminder):
        """  Adds the reminder to the reminders database.
        """
        self.database = shelve.open(reminder_data_file)
        self.no_of_reminders =+ 1
        reminder.id = str(self.no_of_reminders)
        try:
            self.database[reminder.id] = reminder
        finally:
            self.database.close()


    def list_reminders(self):
        """  Creates a list of the individual reminders for display.
        """
        self.database = shelve.open(reminder_data_file)

        reminder_list = []
        for reminder in self.database:
            reminder_list.append(reminder)

        return reminder_list

        self.database.close()



