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

import PySimpleGUI as sg

import os
import datetime
import winsound

from win32api import GetKeyState
from win32con import VK_CAPITAL, VK_SCROLL, VK_NUMLOCK
from ctypes import Structure, windll, c_uint, sizeof, byref

from src.projectPaths import *

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


def update_status_bar(window):
    """  Updated the text fields to current time, current date, key state and idle time.
    """
    strNow = datetime.datetime.now()
    window['-CURRENT-DATE-'].update(f"{ strNow:%A %d %B %Y}")
    window['-CURRENT-STATUS-'].update(f"{get_state()}")
    window['-CURRENT-IDLE-'].update(get_idle_duration())


def set_title(window, view, my_stopwatch, my_countdown, current_time, reminder_db, contacts_db):
    """  Set the window title to an appropriate thing.
         Adds on the stopwatch value, if running.

         u"\u2609" = circle with dot in the middle.
         u"\u2191" = up arrow.
         u"\u2193" = down arrow.
    """
    symbol = u"\u2609"

    match view:
        case "-FUZZY-":
            title = " Fuzzy Time"
        case "-WORLD-":
            title = " World Time"
        case "-COUNTDOWN-":
            title = " Countdown Timer"
        case "-TIMER-":
            title = " Stopwatch"
        case "-REMINDER-":
            title = f" Reminders  {symbol} {reminder_db.no_of_reminders()} reminders"
        case "-CONTACT-":
            title = f" Contacts  {symbol} {contacts_db.no_of_contacts()} contacts"

    if my_stopwatch.timer_running:
        up_arrow   = u"\u2191"
        title += (f" {symbol} {up_arrow}{my_stopwatch.elapsed_time}")

    if my_countdown.countdown_running:
        down_arrow = u"\u2193"
        title += (f" {symbol} {down_arrow}{my_countdown.elapsed_time}")


    title += (f" {symbol} {current_time.getLocalTime()}")

    window.set_title(f" {title}")


def run_action(action):
    """  /s = shut down PC
         /r = reboot PC
         /h = Hibernate PC
         /l = log off current user

         /a = attempts to cancel reboot
    """

    match action:
        case "Notify + Sound":
            winsound.PlaySound("Notification", winsound.SND_ALIAS)
            sg.SystemTray.notify("Countdown", "Countdown had finished.")
        case "Notify":
            sg.SystemTray.notify("Countdown", "Countdown had finished.")
        case "Pop Up":
            sg.popup("Countdown had finished.", title="Countdown")
        case "Shutdown PC":
            os.system("shutdown /s")
        case "Log Out PC":
            os.system("shutdown /l")


def right_alignment_tables(window):
    """  Right aligns the table headers.
    """
    # Alignment for in reminder table Headings
    table = window["-REMINDER_TABLE-"].Widget
    for cid, anchor in enumerate(["w", "w", "w", "w", "w", "w", "w"]):
        table.heading(cid, anchor=anchor)

    # Alignment for in contact table Headings
    table = window["-CONTACT_TABLE-"].Widget
    for cid, anchor in enumerate(["w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w"]):
        table.heading(cid, anchor=anchor)










