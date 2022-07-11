###############################################################################################################
#     reminder.py   Copyright (C) <2022>  <Kevin Scott>                                                       #                                                                                                             #                                                                                                             #
#     A simple class that holds the data for a reminder.                                                      #
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

from datetime import datetime
from operator import itemgetter

import src.reminder.reminder_utils as ru
import src.reminder.notification as notification

from src.projectPaths import *

class reminders():
    """  Adds individual reminders to a reminders database.
         The reminders are stored as pickles on a shelve.

         The reminders are saved as a list of attributes.
            REMINDER_ID           = 0
            REMINDER_TIME_LEFT    = 1
            REMINDER_EVENT        = 2
            REMINDER_DESCRIPTION  = 3
            REMINDER_DATE_DUE     = 4
            REMINDER_TIME_DUE     = 5
            REMINDER_AUTO_DELETE  = 6
            REMINDER_RECURRING    = 7
            REMINDER_DISPLAYED    = 8
            REMINDER_30_DAYS      = 9
            REMINDER_15_DAYS      = 10
            REMINDER_5_DAYS       = 11


         NOTE - key and all fields in shelve are strings

         Maybe some of the logic in add() & check_due() should be moved into a separate file.
    """


    def __init__(self):
        self.database_name = reminder_data_file


    def no_of_reminders(self):
        """  Return the number of contacts, length of database.
        """
        with shelve.open(self.database_name) as database:
            _length = str(len(database))

        return _length


    def add(self, items):
        """  Adds the reminder to the reminders database.
        """
        if items[REMINDER_DATE_DUE] == "":                #  If date is blank, insert today's date'
            items[REMINDER_DATE_DUE] = datetime.now().strftime("%d %B %Y")

        old_date = datetime.strptime(items[REMINDER_DATE_DUE], "%d %B %Y")  #  If date is before today, assume meant next year.
        cur_date = datetime.now().date()
        if (old_date.date() < cur_date):
            new_date                  = ru.add_one_year(old_date)
            items[REMINDER_DATE_DUE]  = new_date

        _days = self.get_day_interval(items[REMINDER_DATE_DUE])
        print(f"days = {_days}")
        match _days:
            case _days if 5 >= _days < 15:
                print("5 - 15")
                items[REMINDER_05_DAYS]  = False
            case _days if 15 >= _days < 30:
                print("15 - 30")
                items[REMINDER_15_DAYS] = False
                items[REMINDER_30_DAYS] = False
            case _days if _days > 30:
                print("30")
                items[REMINDER_30_DAYS] = False


        #current_hour   = datetime.now().hour
        #current_minute = datetime.now().minute

        #hrs, mns = items[REMINDER_TIME_DUE].split(":")              #  Get the reminder due time.
                                                                    ##
        #if int(hrs) < current_hour:                                 #  Is the house less then the current hour.
            #hrs = current_hour                                      #  If so, make the hours equal to the current hour.
        #elif int(mns) < current_minute:                             #  Is the mins less then the current minute
            #mns = current_minute                                    #  if so, make the minute equal to the current minute

        with shelve.open(self.database_name, writeback=True) as database:
            no_of_reminders    = str(len(database))           #  len() is not zero based.
            items[REMINDER_ID] = no_of_reminders

            database[no_of_reminders] = items

        self.renumber_reminders()       #  Renumber.


    def save(self, items):
        """  Saves an existing reminder with amended data.
        """
        with shelve.open(self.database_name, writeback=True) as database:
            items[REMINDER_DISPLAYED]    = "False"       #  If reminder is saved, set displayed flag to false.
            database[items[REMINDER_ID]] = items


    def delete(self, line_no):
        """  Deletes an existing reminder at position line_no.
             After delete, which creates a hole, the reminders are renumbered.
        """
        with shelve.open(self.database_name, writeback=True) as database:
            database.pop(line_no)       #  DELETE.

        self.renumber_reminders()       #  Renumber.


    def list_reminders(self):
        """  Creates a list of the individual reminder items for display.

        """
        with shelve.open(self.database_name) as database:
            reminder_list = []
            for items in database.items():
                item = items[1]
                reminder_list.append(item)

        reminder_list.sort(key=itemgetter(REMINDER_TIME_LEFT))      #  I love python, oh and the internet as well :-)
        return reminder_list


    def get_reminder(self, line_no):
        """  Return the items on a reminder at line_no as a list.

             If an error occurs on read, will return an empty list.
        """
        with shelve.open(self.database_name) as database:
            rem = database[line_no]

        return rem


    def renumber_reminders(self):
        """  After a reminder has been deleted, it leaves a hole in the sequential ID.
             This method is called to readdress that problem.
             It goes through all the reminders in order and sets ID back in order.
        """
        reminders_list = self.list_reminders()
        reminders_list.sort(key=itemgetter(REMINDER_TIME_LEFT))      #  I love python, oh and the internet as well :-)
        new_id   = 0

        with shelve.open(self.database_name, writeback=True) as database:
            database.clear()                                         #  clear, so we rebuild afresh.
            for items in reminders_list:
                items[REMINDER_ID]    = str(new_id)
                database[str(new_id)] = items

                new_id += 1


    def check_due(self, start_up=False):
        """  For each reminder determine the time left before it's due.
             Issue a warning if any are due now.
             Unless auto delete is checked, then delete reminder.

             if start_up is True, then this is the first time this has been called.
             Then instead of deleting the auto_delele reminders, show then first.
             If they had matured when the pyKlock wad not running, they could be just deleted.
        """
        deleted  = False
        x_pos    = 10
        y_pos    = 10

        with shelve.open(self.database_name, writeback=True) as database:
            db_keys  = database.keys()
            for _id in db_keys:
                items = database[_id]

                due_interval              = self.get_minute_interval(items[REMINDER_DATE_DUE], items[REMINDER_TIME_DUE])
                items[REMINDER_TIME_LEFT] = due_interval
                self.save(items)

                print(f"{due_interval}  :: {items}")
                match due_interval:
                    case due_interval if MINUTES_05_DAYS >= due_interval < MINUTES_15_DAYS:                #  Reminder in 5 days.
                        if items[REMINDER_05_DAYS] == "False":
                            _day = self.get_day_interval(items[REMINDER_DATE_DUE])
                            message = f"{items[REMINDER_EVENT]} : {items[REMINDER_DESCRIPTION]} :: Reminder is Due in {_day} days."
                            notification.popup(message, x_pos, y_pos, YELLOW)
                            items[REMINDER_05_DAYS] == "True"
                            self.save(items)
                            y_pos += 65

                    case due_interval if MINUTES_15_DAYS >= due_interval < MINUTES_30_DAYS:                #  Reminder in 15 days.
                        if items[REMINDER_15_DAYS] == "False":
                            _day = self.get_day_interval(items[REMINDER_DATE_DUE])
                            message = f"{items[REMINDER_EVENT]} : {items[REMINDER_DESCRIPTION]} :: Reminder is Due in {_day} days."
                            notification.popup(message, x_pos, y_pos, YELLOW)
                            items[REMINDER_15_DAYS] == "True"
                            self.save(items)
                            y_pos += 65

                    case due_interval if _days > MINUTES_30_DAYS:                                   #  Reminder in 30 days.
                        if items[REMINDER_30_DAYS] == "False":
                            _day = self.get_day_interval(items[REMINDER_DATE_DUE])
                            message = f"{items[REMINDER_EVENT]} : {items[REMINDER_DESCRIPTION]} :: Reminder is Due in {_day} days."
                            notification.popup(message, x_pos, y_pos, YELLOW)
                            items[REMINDER_30_DAYS] == "True"
                            self.save(items)
                            y_pos += 65

                    case due_interval if due_interval == 0:
                        if items[REMINDER_DISPLAYED] == "False":
                            message = f"{items[REMINDER_EVENT]} : {items[REMINDER_DESCRIPTION]} :: Reminder is Due."
                            notification.popup(message, x_pos, y_pos, YELLOW)
                            y_pos += 65

                    case due_interval if due_interval < 0:                 #  Reminder is set to recurring
                        if items[REMINDER_RECURRING] == "True":            #  add one to the year.
                            old_date = datetime.datetime.strptime(items[REMINDER_DATE_DUE], "%d %B %Y")
                            new_date = ru.add_one_year(old_date)
                            items[REMINDER_DATE_DUE]  = new_date
                            self.save(items)

                        elif items[REMINDER_AUTO_DELETE] == "True":        #  If auto delete is set to true
                            if start_up:
                                message = f"{items[REMINDER_EVENT]} : {items[REMINDER_DESCRIPTION]} :: Reminder is Due."
                                notification.popup(message, x_pos, y_pos, YELLOW)
                                y_pos += 65
                            else:
                                database.pop(items[REMINDER_ID])           #  Need to do a hard delete and renumber at the end of the loop.
                                deleted = True

                        elif items[REMINDER_DISPLAYED] == "False":
                            message = f"{items[REMINDER_EVENT]} : {items[REMINDER_DESCRIPTION]} :: Reminder is past please either delete or amend."
                            notification.popup(message, x_pos, y_pos, RED)
                            items[REMINDER_DISPLAYED] = "True"
                            if y_pos > 10:          #  Only increase y_pos if a reminder has already been displayed.
                                y_pos += 65
                            self.save(items)

        if deleted:                         #  Items have been delete, so renumber
            self.renumber_reminders()       #  Renumber.


    def get_minute_interval(self, due_date, due_time):
        """  Return the interval in minutes between the due date and now.
        """
        _now = datetime.now()

        if due_date == "":
            due_date = _now.strftime("%d %B %Y")

        due_date_time = f"{due_date} {due_time}"

        _target_date  = datetime.strptime(due_date_time, "%d %B %Y %H:%M")                #  Combine the date and time into one.

        return round((_target_date - _now).total_seconds() / 60)                          #  Return to minutes, rounded to nearest integer.


    def get_day_interval(self, due_date):

        old_date = datetime.strptime(due_date, "%d %B %Y")  #  If date is before today, assume meant next year.
        cur_date = datetime.now().date()
        delta = old_date.date() - cur_date

        return delta.days



