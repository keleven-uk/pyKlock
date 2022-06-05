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
    def __init__(self, event, description, date_due, time_due, recuring):
        self.id          = "0"
        self.event       = event
        self.description = description
        self.date_due    = date_due
        self.time_due    = time_due
        self.recuring    = recuring

    def items_list(self):
        return [self.id, self.event, self.description, self.date_due, self.time_due, self.recuring]

    #def __str__(self):
        #return f"{self.id}:{self.event}:{self.description}:{self.date_due}:{self.time_due}:{self.recuring}"



class reminders():
    """  Adds individual reminders to a reminders database.
         The reminders are stored as pickles on a shelve.

         NOTE - key and all fields in shelve are strings
         NOTE - also no __init__
    """

    def add(self, reminder):
        """  Adds the reminder to the reminders database.
        """
        self.database = shelve.open(reminder_data_file, writeback=True)
        self.no_of_reminders = len(self.database)
        reminder.id = str(self.no_of_reminders)
        try:
            self.database[reminder.id] = reminder.items_list()
        finally:
            self.database.close()


    def save(self, line_no, event, description, date_due, time_due, recuring):
        """  Saves an existing reminder with amended data.
        """
        self.database = shelve.open(reminder_data_file, writeback=True)
        try:
            self.database[line_no] = [line_no, event, description, date_due, time_due, recuring]
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






