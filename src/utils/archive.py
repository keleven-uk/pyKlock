###############################################################################################################
#    archive.py   Copyright (C) <2022>  <Kevin Scott>                                                         #                                                                                                             #                                                                                                             #
#     Helper routines to archive reminders & contacts.                                                        #
#                                                                                                             #
#     For changes see history.txt                                                                             #
#                                                                                                             #
###############################################################################################################
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

import PySimpleGUI as sg

import pathlib

from zipfile import ZipFile, ZIP_DEFLATED, is_zipfile

from src.projectPaths import *


def save_database(db_type):
    """  Saves a database to a filename in zip format.

         filename = name of the zip file.
         db_type  = type of database to zip, either "reminders" or "contacts"
    """
    filename = sg.popup_get_file(title=f"Save {db_type} database.",
                                 message=f"Please enter a file name to save {db_type} to [Don't forget the .zip].",
                                 save_as=True,
                                 initial_folder=MAIN_PATH)

    if filename != None and filename != "":                     #  filename is None if cancel is selected,
        with ZipFile(filename, "w", ZIP_DEFLATED) as zip_file:  #  but "" if ok is selected without a files chosen.
            for entry in DATA_PATH.rglob(f"{db_type}.*"):
                if entry.suffix != ".zip":                                  #  don't add existing zip files.
                    zip_file.write(entry, entry.relative_to(DATA_PATH))


def load_database(db_type):
    """  Loads a database of type db_type, expects to be in zip format.

         filename = name of the zip file.
         db_type  = type of database to zip, either "reminders" or "contacts"

         The files will be exacted to DATA_PATH - data directory in the main application directory.
    """
    filename = sg.popup_get_file(title=f"Load {db_type} database.",
                                 message=f"Please enter a file name to load {db_type} from.",
                                 save_as=False,
                                 initial_folder=MAIN_PATH)

    file_path = DATA_PATH / f"{db_type}.dat"
    if file_path.is_file():
        choice = sg.popup_yes_no("file already exist - overwrite?")
        if choice == "No":                                          #  Do not overwrite - then return.
            return

        if is_zipfile(filename):
            if filename != "":                                      #  filename is None if cancel is selected,
                with ZipFile(filename, "r") as zip_file:
                    zip_file.extractall(DATA_PATH)
        else:
            sg.popup_error(f"Error {filename} is not a zip file.", title="ERROR")

    else:
        sg.popup_error(f"Error {filename} is not a file.", title="ERROR")






