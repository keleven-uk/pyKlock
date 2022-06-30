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

         The contact are held in last name order.

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

         contacts_db = contacts.contacts()     #  To initialise a contacts database.

         contacts_db.add(items)                #  Adds a new contact, the attributes of the contact are made up of the list(items).
         contacts_db.save(items)               #  Save new items to an existing contact at place CONTACT_ID in the shelve.
         contacts_db.delete(str(line_no))      #  Deletes a contacts at position line_no in the shelve.
         list_contacts()                       #  Returns a list of all the contacts items, a list of lists.
         get_contact(line_no)                  #  Returns a list of one contact at position line_no in the shelve.

         renumber_contacts()                   #  Resorts and renumbers the shelve after a contact has been either added or deleted.

         all methods open and close the shelve, the shelve is not left open between method calling.
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

        self.renumber_contacts()        #  Resort and renumber contacts, to maintain last name sort order.


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

        self.renumber_contacts()        #  Resort and renumber contacts, to maintain last name sort order.


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
        """  When a contact has either been added or deleted, the sorted order is now incorrect.
             So, a list is made of the contacts and re-sorted and this is re-written to the shelve.
        """
        contacts_list = self.list_contacts()
        contacts_list = sorted(contacts_list, key=itemgetter(CONTACT_LAST_NAME))      #  I love python, oh and the internet as well :-)
        database = shelve.open(self.database_name, writeback=True)
        new_id   = 0

        try:
            for items in contacts_list:
                items[CONTACT_ID]     = str(new_id)
                database[str(new_id)] = items

                new_id += 1
        finally:
            database.close()


