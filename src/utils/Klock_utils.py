###############################################################################################################
#    pyDigitalKlock_utils   Copyright (C) <2022>  <Kevin Scott>                                               #                                                                                                             #                                                                                                             #
#    Contains utility functions for pyDigitalKlock.py.                                                        #
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


from win32api import GetKeyState
from win32con import VK_CAPITAL, VK_SCROLL, VK_NUMLOCK
from ctypes import Structure, windll, c_uint, sizeof, byref

def get_state():
    """  Checks the current state of Caps Lock, Scroll Lock & Num Lock.
         The results are returned as a sting.
         A Upper case indicates the lock is on, lower case indicates the lock is off.
    """
    state  = ""
    caps   = GetKeyState(VK_CAPITAL)
    scroll = GetKeyState(VK_SCROLL)
    num    = GetKeyState(VK_NUMLOCK)

    if caps:
        state = "C"
    else:
        state = "c"

    if scroll:
        state += "S"
    else:
        state += "s"

    if num:
        state += "N"
    else:
        state += "n"

    return state



class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_uint),
    ]
def get_idle_duration():
    """  Returns the number of seconds the PC has been idle.
         Uses the class LASTINPUTINFO above.

         Stolen from -
         http://stackoverflow.com/questions/911856/detecting-idle-time-in-python
    """
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    windll.user32.GetLastInputInfo(byref(lastInputInfo))
    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    idle   = millis / 1000.0
    idle = int(idle)

    if idle > 5:  #  Only print idles time if greater then 5 seconds.
        return f"idle : {formatSeconds(idle)}"
    else:
        return "      "




def formatSeconds(seconds):
    """  Formats number of seconds into a human readable form i.e. hours:minutes:seconds
    """
    minutes, seconds = divmod(seconds, 60)
    hours, minutes   = divmod(minutes, 60)

    if hours:
        return f"{hours}h:{minutes}m:{seconds}s"
    elif minutes:
        return f"{minutes}m:{seconds}s"
    else:
        return f"{seconds}s"








