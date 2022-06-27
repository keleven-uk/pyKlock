###############################################################################################################
#     contacts.py   Copyright (C) <2022>  <Kevin Scott>                                                       #                                                                                                             #                                                                                                             #
#     A simple class that holds the data for the contacts.                                                    #
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

from operator import itemgetter

from src.projectPaths import *


class contacts():
    """  Adds individual contact to a contacts database.
         The contacts are stored as pickles on a shelve.

         The contacts are saved as a list of attributes.
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
            CONTACT_NOTE        = 15


         NOTE - key and all fields in shelve are strings
    """


    def __init__(self):
        self.database_name = contacts_data_file


    def no_of_contacts(self):
        """  Return the number of contacts, length of database.
        """
        database = shelve.open(self.database_name)

        try:
            _length = str(len(database))
        finally:
            database.close()

        return _length


    def add(self, items):
        """  Adds the contact to the contacts database.
        """
        database          = shelve.open(self.database_name, writeback=True)
        _no_of_contacts   = str(len(database))           #  len() is not zero based.
        items[CONTACT_ID] = _no_of_contacts

        try:
            database[_no_of_contacts] = items
        finally:
            database.close()


    def save(self, items):
        """  Saves an existing contact with amended data.
        """
        database = shelve.open(self.database_name, writeback=True)

        try:
            database[items[CONTACT_ID]] = items
        finally:
            database.close()


    def delete(self, line_no):
        """  Deletes an existing contact at position line_no.
             After delete, which creates a hole, the contacts are renumbered.
        """
        database = shelve.open(self.database_name, writeback=True)

        try:
            database.pop(line_no)       #  DELETE.
        finally:
            database.close()

        self.renumber_contacts()   #  Renumber.


    def list_contacts(self):
        """  Creates a list of the individual contacts items for display.
        """
        database      = shelve.open(self.database_name, writeback=True)
        contacts_list = []

        try:
            for items in database.items():
                contacts_list.append(items[1])
        finally:
            database.close()

        contacts_list = sorted(contacts_list, key=itemgetter(2))      #  I love python, oh and the internet as well :-)
        self.renumber_contacts()   #  Renumber.
        return contacts_list


    def get_contact(self, line_no):
        """  Return the items on a contact at line_no as a list.

             If an error occurs on read, will return an empty list.
        """
        contact      = []
        database = shelve.open(self.database_name)

        try:
            contact = database[line_no]
        finally:
            database.close()

        return contact


    def renumber_contacts(self):
        """  After a contact has been deleted, it leaves a hole in the sequential ID.
             This method is called to readdress that problem.
             It goes through all the contacts in order and sets ID back in order.
        """
        database = shelve.open(self.database_name, writeback=True)
        new_db  = {}
        db_keys = database.keys()
        new_id  = 0

        try:
            for _id in db_keys:
                items               = database[_id]
                items[CONTACT_ID]   = str(new_id)
                new_db[str(new_id)] = items

                new_id += 1

            #  Dangerous stuff.
            database.clear()
            database.update(new_db)
        finally:
            database.close()


