###############################################################################################################
#     stopwatch.py   Copyright (C) <2022>  <Kevin Scott>                                                      #                                                                                                             #                                                                                                             #
#     A simple class that implements a stopwatch.                                                             #
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

class timer():
    """  A Simple class that implements a stopwatch.

         The stopwatch currently only ticks once every second.

    usage:
        stopwatch = timer()
        stopwatch.start()           Starts the stopwatch.
        stopwatch.stop()            Stops the stopwatch, stops the ticks.
        stopwatch.pause()           Pauses the stopwatch, the ticks still continue.
        stopwatch.elapsed_time      Return the current value of the stopwatch.
        stopwatch.timer_running     Returns True if the stopwatch has been started.

        NB  Stop and Pause do the same thing within the class, but could be different in calling code.
    """

    def __init__(self):
        self.is_running   = False
        self.time_elapsed = 0

    def start(self):
        self.is_running = True
        self.start_time = time.time()

    def stop(self):
        self.is_running = False

    def pause(self):
        self.is_running = False

    def resume(self):
        self.is_running = True

    @property
    def timer_running(self):
        return self.is_running

    @property
    def elapsed_time(self):
        """  Returns the current value [ticks] in hours, minutes seconds {00:00:00}
            The stopwatch currently only ticks once every second.

            If the stopwatch is not running "00:00:00" is returned.
        """
        if self.timer_running:
            time_elapsed     = int(time.time() - self.start_time)
            minutes, seconds = divmod(time_elapsed, 60)
            hours, minutes   = divmod(minutes, 60)

            elps = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            return elps
        else:
            return "00:00:00"


def run_stopwatch(event, window, my_stopwatch):
    """  Control the visibility of the buttons, only display the relevant buttons.
         Call the appropriate timer functions.
    """
    match event:
        case "-TIMER_START-":
            window["-TIMER_START-"].update(visible=False)
            window["-TIMER_RESUME-"].update(visible=False)
            window["-TIMER_STOP-"].update(visible=True)
            window["-TIMER_PAUSE-"].update(visible=True)
            window["-TIMER_CLEAR-"].update(visible=False)
            my_stopwatch.start()
        case "-TIMER_RESUME-":
            window["-TIMER_START-"].update(visible=False)
            window["-TIMER_RESUME-"].update(visible=False)
            window["-TIMER_STOP-"].update(visible=True)
            window["-TIMER_PAUSE-"].update(visible=False)
            window["-TIMER_CLEAR-"].update(visible=False)
            my_stopwatch.resume()
        case "-TIMER_STOP-":
            window["-TIMER_START-"].update(visible=True)
            window["-TIMER_RESUME-"].update(visible=False)
            window["-TIMER_STOP-"].update(visible=False)
            window["-TIMER_PAUSE-"].update(visible=False)
            window["-TIMER_CLEAR-"].update(visible=True)
            my_stopwatch.stop()
        case "-TIMER_PAUSE-":
            window["-TIMER_START-"].update(visible=False)
            window["-TIMER_RESUME-"].update(visible=True)
            window["-TIMER_STOP-"].update(visible=True)
            window["-TIMER_PAUSE-"].update(visible=False)
            window["-TIMER_CLEAR-"].update(visible=False)
            my_stopwatch.pause()
        case "-TIMER_CLEAR-":
            window["-TIMER_START-"].update(visible=True)
            window["-TIMER_RESUME-"].update(visible=False)
            window["-TIMER_STOP-"].update(visible=False)
            window["-TIMER_PAUSE-"].update(visible=False)
            window["-TIMER_CLEAR-"].update(visible=False)
            window["-TIMER_TEXT-"].update("00:00:00")
            my_stopwatch.stop()

