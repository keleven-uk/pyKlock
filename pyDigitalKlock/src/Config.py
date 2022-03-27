###############################################################################################################
#    myConfig.py    Copyright (C) <2020-2021>  <Kevin Scott>                                                       #
#                                                                                                             #
#    A class that acts has a wrapper around the configure file - config.toml.                                 #
#    The configure file is first read, then the properties are made available.                                #
#    The configure file is currently in toml format.                                                          #
#                                                                                                             #
###############################################################################################################
#    Copyright (C) <2020-2021>  <Kevin Scott>                                                                      #
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

import pathlib

import toml


class Config():
    """  A class that acts has a wrapper around the configure file - config.toml.
         The configure file is hard coded and lives in the same directory has the main script.
         The configure file is first read, then the properties are made available.

         If config.toml is not found, a default configure file is generated.

         Use single quotes :-(

         usage:
            myConfig = myConfig.Config()
    """

    def __init__(self, CONFIG_PATH, logger):

        self.FILE_NAME= CONFIG_PATH

        try:
            with open(self.FILE_NAME, "r") as configFile:       # In context manager.
                self.config = toml.load(configFile)             # Load the configure file, in toml.
        except FileNotFoundError:
            logger.debug(f"Configure file not found.")
            logger.debug(f"Writing default configure file.")
            self._writeDefaultConfig()
            logger.debug(f"Running program with default configure settings.")
        except toml.TomlDecodeError:
            logger.debug(f"Error reading configure file.")
            logger.debug(f"Writing default configure file.")
            self._writeDefaultConfig()
            logger.debug(f"Running program with default configure settings.")

    @property
    def NAME(self):
        """  Returns application name.
        """
        return self.config['INFO']['myNAME']

    @property
    def VERSION(self):
        """  Returns application Version.
        """
        return self.config['INFO']['myVERSION']

    def _writeDefaultConfig(self):
        """ Write a default configure file.
            This is hard coded  ** TO KEEP UPDATED **
        """
        config = dict()

        config['INFO'] = {'myVERSION': '2022.15',
                          'myNAME'   : 'pyDigitalKlock'}

        config['APPLICATION'] = {'notification': True}

        st_toml = toml.dumps(config)

        with open(self.FILE_NAME, "w") as configFile:       # In context manager.
            configFile.write("#   Configure files for pyDigitalKlock.py \n")
            configFile.write("#\n")
            configFile.write("#   true and false are lower case \n")
            configFile.write("#   location needs double \ i.e. c:\\tmp\\music - well, on windows any way. \n")
            configFile.write("#\n")
            configFile.write("#   March 2022    (c) Kevin Scott \n")
            configFile.write("\n")
            configFile.writelines(st_toml)                  # Write configure file.

        with open(self.FILE_NAME, "r") as configFile:       # In context manager.
            self.config = toml.load(configFile)             # Load the configure file, in toml.
