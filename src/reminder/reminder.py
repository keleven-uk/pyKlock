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
import datetime

import src.reminder.notification as notification

from src.projectPaths import *

GREEN  = "#B9DA8C"
YELLOW = "#D7DA97"
BLUE   = "#00FDFF"
RED    = "#DA8C8C"
BLACK  = "#000000"

class reminders():
    """  Adds individual reminders to a reminders database.
         The reminders are stored as pickles on a shelve.

         the reminders are saved has a list of attributes.
            items -  [ID, event, description, date_due, time_due, recurring, displayed]

         NOTE - key and all fields in shelve are strings
    """

    def __init__(self):
        self.database_name = reminder_data_file


    def add(self, items):
        """  Adds the reminder to the reminders database.
        """
        database        = shelve.open(self.database_name, writeback=True)
        no_of_reminders = str(len(database))           #  len() is not zero based.
        items[0]        = no_of_reminders
        items.append("False")
        try:
            database[no_of_reminders] = items
        finally:
            database.close()


    def save(self, items):
        """  Saves an existing reminder with amended data.
        """
        database = shelve.open(self.database_name, writeback=True)
        try:
            database[items[0]] = items
        finally:
            database.close()


    def delete(self, line_no):
        """  Deletes an existing reminder at position line_no.
             After delete, which creates a hole, the reminders a renumbered.
        """
        database = shelve.open(self.database_name, writeback=True)
        try:
            database.pop(line_no)       #  DELETE.
            self.renumber_reminders()   #  Renumber.
        finally:
            database.close()


    def list_reminders(self):
        """  Creates a list of the individual reminder items for display.
        """
        database = shelve.open(self.database_name, writeback=True)

        reminder_list = []

        try:
            for items in database.items():
                reminder_list.append(items[1])
        finally:
            database.close()

        return reminder_list


    def get_reminder(self, line_no):
        """  Return a all the reminder items as a list.

             If an error occurs on read, will return an empty list.
        """
        rem = []
        database = shelve.open(self.database_name)
        try:
            rem = database[line_no]
        finally:
            database.close()

        return rem


    def renumber_reminders(self):
        """  After a reminder has been deleted, it leaves a hole in the sequential ID.
             This method is called to readdress that probem.
             It goes through all the reminders in order and sets ID back in order.
        """
        database = shelve.open(self.database_name)
        new_db  = {}
        db_keys = database.keys()
        new_id  = 0

        try:
            for _id in db_keys:
                items = database[_id]
                items[0] = str(new_id)
                new_db[str(new_id)] = items

                new_id += 1

            #  Dangerous stuff.
            database.clear()
            database.update(new_db)
        finally:
            database.close()


    def check_due(self):
        """  For each reminder determine the time left before it's due.
             Issue a warning if any are due now.
        """
        database = shelve.open(self.database_name)
        db_keys  = database.keys()
        x_pos = 10
        y_pos = 10

        try:
            for _id in db_keys:
                items = database[_id]
                print(items, len(items))
                if len(items) == 6:
                    items.append("False")

                due_interval = self.get_interval(items[3], items[4])

                match due_interval:
                    case due_interval if due_interval <5 and due_interval >0:
                        if items[6] == "False":
                            message = f"{items[1]} : {items[2]} :: Reminder Due in less then five minutes."
                            notification.popup(message, x_pos, y_pos, YELLOW)
                            items[6] = "True"
                            y_pos += 65
                            self.save(items)
                    case due_interval if due_interval <0:
                        if items[6] == "False":
                            message = f"{items[1]} : {items[2]} :: Reminder is past please either delete or amend."
                            notification.popup(message, x_pos, y_pos, RED)
                            items[6] = "True"
                            y_pos += 65
                            self.save(items)
        finally:
            database.close()


    def get_interval(self, due_date, due_time):
        """  Return the interval in minutes between the due date and now.
        """
        _now = datetime.datetime.now()

        if due_date == "":
            due_date = _now.strftime("%d %B %Y")

        due_date_time = f"{due_date} {due_time}"

        target_date  = datetime.datetime.strptime(due_date_time, "%d %B %Y %H:%M")       #  Combine the date and time into one.
        return int((target_date - _now).total_seconds() / 60)                            #  Return to minutes







