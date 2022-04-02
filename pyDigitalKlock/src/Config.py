###############################################################################################################
#    myConfig.py    Copyright (C) <2020-2021>  <Kevin Scott>                                                  #
#                                                                                                             #
#    A class that acts has a wrapper around the configure file - config.toml.                                 #
#    The configure file is first read, then the properties are made available.                                #
#    The configure file is currently in toml format.                                                          #
#                                                                                                             #
###############################################################################################################
#    Copyright (C) <2020-2021>  <Kevin Scott>                                                                 #
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
import datetime

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

        self.FILE_NAME = CONFIG_PATH
        self.logger    = logger

        try:
            with open(self.FILE_NAME, "r") as configFile:       # In context manager.
                self.config = toml.load(configFile)             # Load the configure file, in toml.
        except FileNotFoundError:
            self.logger.debug(f"Configure file not found.")
            self.logger.debug(f"Writing default configure file.")
            self._writeDefaultConfig()
            self. logger.debug(f"Running program with default configure settings.")
        except toml.TomlDecodeError:
            self.logger.debug(f"Error reading configure file.")
            self.logger.debug(f"Writing default configure file.")
            self._writeDefaultConfig()
            self.logger.debug(f"Running program with default configure settings.")


    @property
    def NAME(self):
        """  Returns the application name.
        """
        return self.config['INFO']['myNAME']

    @property
    def VERSION(self):
        """  Returns the application Version.
        """
        return self.config['INFO']['myVERSION']

    @property
    def FOREGROUND(self):
        """  Return the foreground colour.
        """
        return self.config["COLOUR"]["foreground"]

    @FOREGROUND.setter
    def FOREGROUND(self, value):
        """  Sets the foreground colour.
        """
        self.config["COLOUR"]["foreground"] = value

    @property
    def BACKGROUND(self):
        """  Return the background colour.
        """
        return self.config["COLOUR"]["background"]

    @BACKGROUND.setter
    def BACKGROUND(self, value):
        """  Sets the background colour.
        """
        self.config["COLOUR"]["background"] = value

    @property
    def TRANSPARENT(self):
        """  Return the background colour.
        """
        return self.config["COLOUR"]["transparent"]

    @TRANSPARENT.setter
    def TRANSPARENT(self, value):
        """  Sets the background colour.
        """
        self.config["COLOUR"]["transparent"] = value

    @property
    def X_POS(self):
        """  Return the background colour.
        """
        return self.config["POSITION"]["x_pos"]

    @X_POS.setter
    def X_POS(self, value):
        """  Sets the background colour.
        """
        self.config["POSITION"]["x_pos"] = value

    @property
    def Y_POS(self):
        """  Return the background colour.
        """
        return self.config["POSITION"]["y_pos"]

    @Y_POS.setter
    def Y_POS(self, value):
        """  Sets the background colour.
        """
        self.config["POSITION"]["y_pos"] = value





    def writeConfig(self):
        """ Write the current config file.
        """
        strNow  = datetime.datetime.now()
        written = strNow.strftime("%A %d %B %Y  %H:%M:%S")
        st_toml = toml.dumps(self.config)

        with open(self.FILE_NAME, "w") as configFile:       # In context manager.
            configFile.write("#   Configure file for pyDigitalKlock.py \n")
            configFile.write(f"#   (c) Kevin Scott   Written {written}\n")
            configFile.write("#\n")
            configFile.write("#   true and false are lower case \n")
            configFile.write("#   location needs double \ i.e. c:\\tmp\\music - well, on windows any way. \n")
            configFile.write("#\n")

            configFile.writelines(st_toml)


    def _writeDefaultConfig(self):
        """ Write a default configure file.
            This is hard coded  ** TO KEEP UPDATED **
        """
        strNow  = datetime.datetime.now()
        written = strNow.strftime("%A %d %B %Y  %H:%M:%S")
        config  = dict()

        config['INFO'] = {'myVERSION': '2022.19',
                          'myNAME'   : 'pyDigitalKlock'}

        config["COLOUR"] = {"foreground":"#ff0000",
                            "background":"#80ff80",
                            "transparent":"false"}

        config["POSITION"] = {"x_pos":0,
                              "y_pos":0}


        st_toml = toml.dumps(config)

        with open(self.FILE_NAME, "w") as configFile:       # In context manager.
            configFile.write("#   DEFAULT Configure file for pyDigitalKlock.py \n")
            configFile.write(f"#   (c) Kevin Scott   Written {written}\n")
            configFile.write("#\n")
            configFile.write("#   true and false are lower case \n")
            configFile.write("#   location needs double \ i.e. c:\\tmp\\music - well, on windows any way. \n")
            configFile.write("\n")
            configFile.writelines(st_toml)                  # Write configure file.

        with open(self.FILE_NAME, "r") as configFile:       # In context manager.
            self.config = toml.load(configFile)             # Load the configure file, in toml.
