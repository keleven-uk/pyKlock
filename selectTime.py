import datetime
import time
import math

class SelectTime:

    #  GLOBAL variables used in several fimction
    __types = ("Fuzzy Time", "Time in Words", "GMT Time", "Local Time", "UTC Time", "Swatch Time", "NET Time")

    __hours = ("twelve", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",  "eleven", "twelve")
    __units = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve")
    __tens = ("zero", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty")

#
#  the class is access bt the following properties only.
#  timeFuncs can't be made a proper property, this seems to upset the dictionary of functions - there not callable.

    @property
    def timeTypes(self):
        """ Returns a tuple of available Time types."""
        return self.__types

    def timeFuncs(self, position=0):
        """ Returns a function to return the time as position f in timeTypes."""
        return self.__funcs[position](self)


# -------------------------------------------------------------------------------- time functions ----------------------
#
# The time functions can't be made property's, this seems to upset the dictionary of functions - there not callable.
#
# ------------------------------------------------------------------------------------- getGMTTime --------------------
    def getGMTTime(self):
        """ returns current time as GMT."""
        return time.strftime("%H:%M:%S", time.gmtime())

# ------------------------------------------------------------------------------------- getLocalTime -------------------
    def getLocalTime(self):
        """ returns current time as Local time."""
        return time.strftime("%H:%M:%S", time.localtime())

# ------------------------------------------------------------------------------------- getUTCTim ----------------------
    def getUTCTime(self):
        """ returns current time as UTC time."""
        return "{:%H:%M:%S}".format(datetime.datetime.utcnow())

# ------------------------------------------------------------------------------------- getFuzzyTime -------------------
    def getFuzzyTime(self):
        """ Returns current time as Fuzzy Time."""

        minsText = {0: "", 5: "five past", 10: "ten past", 15: "quarter past", 20: "twenty past",
                   25: "twenty-five past", 30: "half past", 35: "twenty-five to", 35: "twenty-five to",
                   40: "twenty to", 45: "quarter to", 50: "ten to", 55: "five to", 60: ""}

        now = datetime.datetime.now()

        __hour = now.hour
        __mins = now.minute
        __nrms = __mins - (__mins % 5)  # gets nearest five minutes
        __sRtn = ""

        __ampm = "in the morning" if __hour < 12 else "pm"

        if (__mins % 5) > 2:
            __nrms += 5  # closer to next five minutes, go to next

        __sRtn = minsText[__nrms]  # look up text for minutes.

        if __nrms > 30:
            __hour += 1

        # generate output string according to the hour of the day.

        #   if the hour is 0 or 24 and no minutes - it must be midnight.
        #   if the hour is 12 and no minutes - it must be noon.

        #   if "pm" then afternoon, subtract 12 - only use 12 hour clock.

        if __hour == 12 and __sRtn == "":
            __fuzzyTime = "about Noon"
        elif __hour == 0 and __sRtn == "":
            __fuzzyTime = "about Midnight"
        elif __hour == 24 and __sRtn == "":
            __fuzzyTime = "about Midnight"
        else:
            if __ampm == "pm":
                __hour -= 12
                __ampm = "in the evening" if __hour > 5 else "in the afternoon"
            if __sRtn == "":
                __fuzzyTime = "about {0}'ish {1}".format(self.__hours[__hour], __ampm)
            else:
                __fuzzyTime = "{0} {1} {2}".format(__sRtn, self.__hours[__hour], __ampm)

        return __fuzzyTime

# ------------------------------------------------------------------------------------- getWordsTime -------------------
    def getWordsTime(self):
        """ Returns current time in words."""

        now = datetime.datetime.now()

        __hour = now.hour
        __mins = now.minute
        __pasTo = "past"

        __ampm = "in the morning" if __hour < 12 else "pm"

        if __mins > 30:                                         # past the half hour - minutes to the hour.
            __hour += 1
            __pasTo = "to"
            __mins = 60 - __mins

        # generate output string according to the hour of the day.

        # if "pm" then afternoon, subtract 12 - only use 12 hour clock.

        if __ampm == "pm":
            __hour -= 12
            __ampm = "in the evening" if __hour >= 5 else "in the afternoon"

        if __mins == 0:
            __minsStr = "{0} o'clock {1}".format(self.__hours[__hour], __ampm)
        elif 1 <= __mins <= 9:
            __minsStr = "{0} minutes {1} {2} {3}".format(self.__units[__mins], __pasTo, self.__hours[__hour], __ampm)
        elif 10 <= __mins <= 20:
            __minsStr = "{0} minutes {1} {2} {3}".format(self.__tens[__mins-9], __pasTo, self.__hours[__hour], __ampm)
        elif 21 <= __mins <= 29:
            __minsTens = math.floor(__mins / 10)
            __minsUnit = __mins - (__minsTens * 10)
            __minsStr = "twenty{0} minutes {1} {2} {3}".format(self.__units[__minsUnit], __pasTo, self.__hours[__hour], __ampm)
        else:
            __minsStr = "thirty minutes past {0} {1}".format(self.__hours[__hour], __ampm)

        return __minsStr

# ------------------------------------------------------------------------------------- getSwatchTime ------------------
    def getSwatchTime(self):
        """   returns UTC [+1 hour] time as Swatch Time.
        Swatch time is made up of 1000 beats per day i.e. 1 beat = 86.4 seconds.
        This is then encoded into a string.

        see http://en.wikipedia.org/wiki/Swatch_Internet_Time"""

        __utcNow = datetime.datetime.utcnow()
        __utcPlus1 = __utcNow + datetime.timedelta(hours=+1)
        __noOfSeconds = (__utcPlus1.hour * 3600) + (__utcPlus1.minute * 60) + __utcPlus1.second
        __noOfBeats = __noOfSeconds / 86.4

        return "@ {0:.2f} BMT".format(__noOfBeats)

    def getNETTime(selfself):
        """    Returns UTC time as New Earth Time.
        New Earth Time [or NET] splits the day into 260 degrees. each degree is
        further split into 60 minutes and further into 60 seconds.

        Only shows degrees and minutes - at the moment.

        see http://en.wikipedia.org/wiki/New_Earth_Time"""

        now = datetime.datetime.now()

        __hour = now.hour
        __mins = now.minute
        __secs = now.second

        __deg = __hour * 15 + (__mins // 4)
        __min = __mins - ((__mins // 4) * 4)
        __sec = (__secs + (__min * 60)) / 4

        return "{0} deg {1} mins".format(__deg, int(__sec))


    # GLOBAL Dictionary that holds references to all the time functions.
    __funcs = {"Fuzzy Time": getFuzzyTime,
               "Time in Words": getWordsTime,
               "GMT Time": getGMTTime,
               "Local Time": getLocalTime,
               "UTC Time": getUTCTime,
               "Swatch Time": getSwatchTime,
               "NET Time" : getNETTime}



# ----------------------------------------------------- called to test, if run as main (nit imported) ------------------
if __name__ == "__main__":
    import tkinter as tk
    import tkinter.ttk as ttk

    def update_timeText():
        # Get the current time
        current = s.timeFuncs(position=timeCombo.get())

        # Update the timeText label box with flexi time.
        timeText.configure(text=current)

        root.wm_title("SelectTime Test :: " + time.strftime("%H:%M:%S", time.localtime()))

        # Call the update_timeText() function every 1 second.
        root.after(1000, update_timeText)

    s = SelectTime()

    root = tk.Tk()
    root.wm_title("SelectTime Test")

    # create a conbobox
    timevar = tk.StringVar()
    timeCombo = ttk.Combobox(root, textvariable=timevar, values=list(s.timeTypes))
    timeCombo.current(0)
    timeCombo.pack()

    # create a timeText label (a text box)
    timeText = ttk.Label(root, text="", font=("Helvetica", 20))
    timeText.pack()

    update_timeText()
    root.mainloop()
