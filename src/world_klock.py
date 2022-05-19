###############################################################################################################
#     countdown.py   Copyright (C) <2022>  <Kevin Scott>                                                      #                                                                                                             #                                                                                                             #
#     A simple class that implements a countdown timer.                                                       #
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

import zoneinfo
from datetime import datetime
import re

class world_klock:
    """  A Simple class that implements a World Klock.

         The World Klock currently only ticks once every second.

         Usage:
            my_world_klock = world_klock()
            my_world_klock - available_timezones        #  Returns  sorted list of available timezones.
            my_world_klock.get_local_time(timezone)     #  Returns the time in the specified timezone relevant to the local time.

        The timezone in chosen from a combobox.

        The returned list is not only sorted alphabetically, but also has had old and depreciated entries removed.
        Thanks to https://adamj.eu/tech/2021/05/06/how-to-list-all-timezones-in-python/
        The file backwards [which resides in the src directory] is from the download at https://www.iana.org/time-zones

        Need to install tzdata  i.e.  pip install tzdata
    """

    def __init__(self):
        self.tzlist = sorted(self.get_timezones())      #  Sorted() returns a list, which is want we want.  :-)

    @property
    def available_timezones(self):
        return self.tzlist

    def get_local_time(self, timezone):
        tz = zoneinfo.ZoneInfo(timezone)
        dt = datetime.now(tz).strftime("%H:%M:%S")
        return dt


    def deprecated_aliases(self):
        aliases = set()
        with open("backward", "r") as fp:
            for line_full in fp:
                line = line_full.strip()
                if not line.startswith("Link\t"):
                    continue
                _link, _dest, source = re.split("\t+", line)
                aliases.add(source)
        return aliases

    def get_timezones(self):
        return zoneinfo.available_timezones() - self.deprecated_aliases()
