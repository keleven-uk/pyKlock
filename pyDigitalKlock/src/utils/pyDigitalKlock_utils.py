###############################################################################################################
#    pyDigitalKlock_utils   Copyright (C) <2022>  <Kevin Scott>                                               #                                                                                                             #                                                                                                             #
#    Contains utility functions for pyDigitalKlock.py.                                                        #
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
    return millis / 1000.0
