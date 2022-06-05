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


class reminders():
    """  Adds individual reminders to a reminders database.
         The reminders are stored as pickles on a shelve.

         NOTE - key and all fields in shelve are strings
         NOTE - also no __init__
    """

    def add(self, items):
        """  Adds the reminder to the reminders database.
        """
        self.database = shelve.open(reminder_data_file, writeback=True)
        no_of_reminders = str(len(self.database))
        items[0] = no_of_reminders
        try:
            self.database[no_of_reminders] = items
        finally:
            self.database.close()


    def save(self, items):
        """  Saves an existing reminder with amended data.
        """
        self.database = shelve.open(reminder_data_file, writeback=True)
        try:
            self.database[items[0]] = items
        finally:
            self.database.close()


    def delete(self, line_no):
        """  Deletes an existing reminder at position line_no.
        """
        self.database = shelve.open(reminder_data_file, writeback=True)
        try:
            self.database.pop(line_no)  # DELETE
            self.renumber_reminders()
        finally:
            self.database.close()


    def list_reminders(self):
        """  Creates a list of the individual reminder items for display.
        """
        self.database = shelve.open(reminder_data_file, writeback=True)

        reminder_list = []

        try:
            for items in self.database.items():
                reminder_list.append(items[1])
        finally:
            self.database.close()

        return reminder_list


    def get_reminder(self, line_no):
        """  Return a single reminder at position line_no.

             If an error occurs on read, will return an empty reminder.
        """
        rem = []
        self.database = shelve.open(reminder_data_file)
        try:
            rem = self.database[line_no]
        finally:
            self.database.close()

        return rem


    def renumber_reminders(self):
        """  After a reminder has been deleted, it leaves a hole in the sequential ID.
             This method is called to readdress that probem.
             It goes through all the reminders in order and sets ID back in order.
        """
        self.database = shelve.open(reminder_data_file)
        new_db  = {}
        db_keys = self.database.keys()
        new_id  = 0

        try:
            for _id in db_keys:
                items = self.database[_id]
                items[0] = str(new_id)
                new_db[str(new_id)] = items

                new_id += 1

            #  Dangerous stuff.
            self.database.clear()
            self.database.update(new_db)
        finally:
            self.database.close()






