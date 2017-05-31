import datetime
import time


class SelectTime:

    __types = ("Fuzzy Time", "GMT Time", "Local Time", "UTC Time")


    @property
    def timeTypes(self):
        """ Returns a tuple of available Time types."""
        return self.__types

    def timeFuncs(self, position=0):
        """ Returns a fuction to return the time as position f in timeTypes."""
        return self.__funcs[position](self)


# -------------------------------------------------------------------------------- time functions ----------------------
#
# The time functions can't be made property's, this seems to upset the dictionary of functions - there not callable.

    def getGMTTime(self):
        """ returns current time as GMT."""
        return time.strftime("%H:%M:%S", time.gmtime())

    def getLocalTime(self):
        """ returns current time as Local time."""
        return time.strftime("%H:%M:%S", time.localtime())

    def getUTCTime(self):
        """ returns current time as UTC time."""
        return "{:%H:%M:%S}".format(datetime.datetime.utcnow())

    def getFuzzyTime(self):
        """ Returns current time as Fuzzy Time."""

        hours = {0: "twelve", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six",
                 7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve"}

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
        #   This looks more complicated then it should be, maybe separate if then's would be better.

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
                __fuzzyTime = "about {0}'ish {1}".format(hours[__hour], __ampm)
            else:
                __fuzzyTime = "{0} {1} {2}".format(__sRtn, hours[__hour], __ampm)

        return __fuzzyTime

    # Dictionary that holds references to all the time functions.
    __funcs = {"Fuzzy Time": getFuzzyTime, "GMT Time": getGMTTime, "Local Time": getLocalTime, "UTC Time": getUTCTime}


if __name__ == "__main__":
    import tkinter as tk
    import tkinter.ttk as ttk

    def update_timeText():
        # Get the current time
        current = s.timeFuncs(position=timeCombo.get())

        # Update the timeText label box with flexi time.
        timeText.configure(text=current)

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
