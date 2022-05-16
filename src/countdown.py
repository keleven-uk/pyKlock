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

import time

from src.projectPaths import *

import src.utils.klock_utils as utils


class countdown():
    """  A Simple class that implements a countdown timer.

         A copy of the window object needs to be passed in because when the countdown has finished,
         it can then pass back an event by writing to the main window event loop.

         Usage:
            my_countdown = countdown(window)
            my_countdown.start(n)               #  Starts the countdown of n minutes.)
            my_countdown.tick()                 #  Decrements the countdown, should be called regularly [i.e. every second].
                                                #  Tick also return the current countdown value.
            my_countdown.clear                  #  Cancels the current countdown and sets everything back to the start.

    """
    def __init__(self, window):
        self.window     = window
        self.is_running = False
        self.target     = 0

    def start(self, target_time):
        """  Start the countdown timer, which will count down until target_time is zero.
             The target time is passed in minutes and converted to seconds.
             NB  the event loop is called every second.
        """
        self.is_running = True
        self.target     = target_time * 60

    @property
    def countdown_running(self):
        return self.is_running

    def tick(self):
        if self.is_running:
            self.target -= 1

            return self.elapsed_time
        else:
            return "00:00:00"

    @property
    def elapsed_time(self):
        """  Returns the current value [ticks] in hours, minutes seconds {00:00:00}
             The countdown currently only ticks once every second.

             If the countdown is not running "00:00:00" is returned.
        """

        if self.target == 0:
            self.window.write_event_value("-COUNTDOWN_EVENT-", ("Finished"))
            self.is_running = False
            return "00:00:00"

        minutes, seconds = divmod(self.target, 60)
        hours, minutes   = divmod(minutes, 60)

        trg = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        return trg


    def clear(self):
        self.is_running = False


def run_countdown(event, window, my_countdown, values):
    """  Control the visibility of the buttons, only display the relevant buttons.
         Call the appropriate countdown functions.
    """
    match event:
        case "-+15-":
            window["-COUNTDOWN_START-"].update(visible=False)
            window["-COUNTDOWN_STOP-"].update(visible=True)
            window["-+15-"].update(visible=False)
            window["-+30-"].update(visible=False)
            window["-+45-"].update(visible=False)
            window["-+60-"].update(visible=False)
            my_countdown.start(15)
        case "-+30-":
            window["-COUNTDOWN_START-"].update(visible=False)
            window["-COUNTDOWN_STOP-"].update(visible=True)
            window["-+15-"].update(visible=False)
            window["-+30-"].update(visible=False)
            window["-+45-"].update(visible=False)
            window["-+60-"].update(visible=False)
            my_countdown.start(30)
        case "-+45-":
            window["-COUNTDOWN_START-"].update(visible=False)
            window["-COUNTDOWN_STOP-"].update(visible=True)
            window["-+15-"].update(visible=False)
            window["-+30-"].update(visible=False)
            window["-+45-"].update(visible=False)
            window["-+60-"].update(visible=False)
            my_countdown.start(45)
        case "-+60-":
            window["-COUNTDOWN_START-"].update(visible=False)
            window["-COUNTDOWN_STOP-"].update(visible=True)
            window["-+15-"].update(visible=False)
            window["-+30-"].update(visible=False)
            window["-+45-"].update(visible=False)
            window["-+60-"].update(visible=False)
            my_countdown.start(60)
        case "-COUNTDOWN_START-":
            window["-COUNTDOWN_START-"].update(visible=False)
            window["-COUNTDOWN_STOP-"].update(visible=True)
            window["-+15-"].update(visible=False)
            window["-+30-"].update(visible=False)
            window["-+45-"].update(visible=False)
            window["-+60-"].update(visible=False)
            my_countdown.start(int(values["-COUNTDOWN_TARGET-"]))
        case "-COUNTDOWN_STOP-":
            window["-COUNTDOWN_START-"].update(visible=True)
            window["-COUNTDOWN_STOP-"].update(visible=False)
            window["-+15-"].update(visible=True)
            window["-+30-"].update(visible=True)
            window["-+45-"].update(visible=True)
            window["-+60-"].update(visible=True)
            window["-COUNTDOWN-TEXT-"].update("00:00:00")
            window["-COUNTDOWN_TARGET-"].update(value=1)
            my_countdown.clear()
        case "-COUNTDOWN_EVENT-":
            window["-COUNTDOWN_START-"].update(visible=True)
            window["-COUNTDOWN_STOP-"].update(visible=False)
            window["-+15-"].update(visible=True)
            window["-+30-"].update(visible=True)
            window["-+45-"].update(visible=True)
            window["-+60-"].update(visible=True)
            window["-COUNTDOWN_TARGET-"].update(value=1)
            action = values["-COUNTDOWN-ACTION-"]
            utils.play_warning(action)

