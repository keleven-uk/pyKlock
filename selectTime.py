import datetime
import time
import math

import timeCodes


class SelectTime:

    #  GLOBAL variables used in several fimction
    __types = ("Fuzzy Time", "Time in Words", "GMT Time", "Local Time", "UTC Time", "Swatch Time", "New Earth Time",
               "Julian Time", "Decimal Time", "True Hex Time", "Hex Time", "Oct Time", "Binary Time", "Roman Time",
               "Morse Time")

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
    def __getNowTime(self):
        """  returns now as hour, munutes and seconds"""
        now = datetime.datetime.now()

        return now.hour, now.minute, now.second
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

        __hour, __mins, __secs = self.__getNowTime()
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

        __hour, __mins, __secs = self.__getNowTime()
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

        return "@ {0::.2f} BMT".format(__noOfBeats)

# ------------------------------------------------------------------------------------- getNETTime ---------------------
    def getNETTime(self):
        """    Returns UTC time as New Earth Time.
        New Earth Time [or NET] splits the day into 360 degrees. each degree is
        further split into 60 minutes and further into 60 seconds.

        Only shows degrees and minutes - at the moment.

        see http://en.wikipedia.org/wiki/New_Earth_Time"""

        __utcNow = datetime.datetime.utcnow()

        __hour = __utcNow.hour
        __mins = __utcNow.minute
        __secs = __utcNow.second

        __deg = __hour * 15 + (__mins // 4)
        __min = __mins - ((__mins // 4) * 4)
        __sec = math.floor((__secs + (__min * 60)) / 4)

        return "{0} deg {1:0>2} mins".format(__deg, __sec)

# ------------------------------------------------------------------------------------- getJulianTime ------------------
    def getJulianTime(self):
        """   returns UTC time as a Julian Date Time.
        Formulae pinched from http://en.wikipedia.org/wiki/Julian_day"""

        now = datetime.datetime.utcnow()

        a = (14 - now.month) / 12
        y = now.year + 4800 - a
        m = now.month + (12 * a) - 3

        jt = now.day + ((153 * m + 2) / 5) + (365 * y) + (y / 4) + (y / 100) - 32045
        jt = jt + ((now.hour - 12) / 24) + (now.minute / 1440) + (now.second / 86400)

        return "{0:.5f}".format(jt)

# ------------------------------------------------------------------------------------- getDecimalTime -----------------
    def getDecimalTime(self):
        """   Returns the current [local] time in decimal notation.
        The day is divided into 10 hours, each hour is then split into 100 minutes of 100 seconds.

        see http://en.wikipedia.org/wiki/Decimal_time"""

        __hour, __mins, __secs = self.__getNowTime()

        __noOfSeconds = (__hour * 3600) + (__mins * 60) + __secs
        __noOfDecimalSeconds = __noOfSeconds / 0.864

        __hour = math.floor(__noOfDecimalSeconds / 10000)
        __mins = math.floor((__noOfDecimalSeconds - (__hour * 10000)) / 100)
        __secs = math.floor(__noOfDecimalSeconds - (__hour * 10000) - (__mins * 100))
        return "{0:0>2}h {1:0>2}m {2:0>2}s".format(__hour, __mins, __secs)

# ------------------------------------------------------------------------------------- getTrueHexTime -----------------
    def getTrueHexTime(self):
        """   Returns the current [local] time in Hexadecimal time.
        The day is divided in 10 (sixteen) hexadecimal hours, each hour in 100 (two hundred and fifty-six)
        hexadecimal minutes and each minute in 10 (sixteen) hexadecimal seconds.

        see http://en.wikipedia.org/wiki/Hexadecimal_time"""

        __hour, __mins, __secs = self.__getNowTime()

        __noOfSeconds = (__hour * 3600) + (__mins * 60) + __secs
        __noOfHexSeconds = math.floor(__noOfSeconds * (65536 / 84600))

        __hour = math.floor(__noOfHexSeconds / 4096)
        __mins = math.floor((__noOfHexSeconds - (__hour * 4096)) / 16)
        __secs = __noOfHexSeconds % 16
        return "{0:0>2X}_{1:0>2X}_{2:0>2X}".format(__hour, __mins, __secs)

#   0> - pads a string with 0's from the left.
# ------------------------------------------------------------------------------------- getHexTime ---------------------
    def getHexTime(self):
        """   Returns current [local] time in hex [base 16] format.
        This is only a hex representation of the current time"""

        __hour, __mins, __secs = self.__getNowTime()
        return "{0:0>2X}:{1:0>2X}:{2:0>2X}".format(__hour, __mins, __secs)

# ------------------------------------------------------------------------------------- getOctTime ---------------------
    def getOctTime(self):
        """   Returns current [local] time in oct [base 8] format.
        This is only a hex representation of the current time"""

        __hour, __mins, __secs = self.__getNowTime()
        return "{0:0>2o}:{1:0>2o}:{2:0>2o}".format(__hour, __mins, __secs)

# ------------------------------------------------------------------------------------- getBinTime ---------------------
    def getBinTime(self):
        """   Returns current [local] time in Binary [base 2] format.
        This is only a hex representation of the current time"""

        __hour, __mins, __secs = self.__getNowTime()
        return "{0:0>6b}:{1:0>6b}:{2:0>6b}".format(__hour, __mins, __secs)

# ------------------------------------------------------------------------------------- getRomanTime -------------------
    def getRomanTime(self):
        """   Returns the current [local] time in Roman numerals."""

        __hour, __mins, __secs = self.__getNowTime()
        
        __Rhour = timeCodes.romanNumerals[__hour]
        __Rmins = timeCodes.romanNumerals[__mins]
        __Rsecs = timeCodes.romanNumerals[__secs]
        
        return "{0}:{1}:{2}".format(__Rhour, __Rmins, __Rsecs)

# ------------------------------------------------------------------------------------- getMorseTime -------------------
    def getMorseTime(self):
        """   Returns the current [local] time with each digit represented bu a Morse code."""

        __hour, __mins, __secs = self.__getNowTime()

        if __hour < 10:
            __Mhour = "{0} {1}".format(timeCodes.morseCode[0], timeCodes.morseCode[__hour])
        else:
            __Mhour = "{0} {1}".format(timeCodes.morseCode[int(__hour/10)], timeCodes.morseCode[__hour % 10])

        if __mins < 10:
            __Mmins = "{0} {1}".format(timeCodes.morseCode[0], timeCodes.morseCode[__mins])
        else:
            __Mmins = "{0} {1}".format(timeCodes.morseCode[int(__mins/10)], timeCodes.morseCode[__mins % 10])

        if __secs < 10:
            __Msecs = "{0} {1}".format(timeCodes.morseCode[0], timeCodes.morseCode[__secs])
        else:
            __Msecs = "{0} {1}".format(timeCodes.morseCode[int(__secs/10)], timeCodes.morseCode[__secs % 10])

        return "{0}:{1}:{2}".format(__Mhour, __Mmins, __Msecs)

    #
    # GLOBAL Dictionary that holds references to all the time functions.
    __funcs = {"Fuzzy Time": getFuzzyTime,
               "Time in Words": getWordsTime,
               "GMT Time": getGMTTime,
               "Local Time": getLocalTime,
               "UTC Time": getUTCTime,
               "Swatch Time": getSwatchTime,
               "New Earth Time": getNETTime,
               "Julian Time": getJulianTime,
               "Decimal Time": getDecimalTime,
               "True Hex Time": getTrueHexTime,
               "Hex Time": getHexTime,
               "Oct Time": getOctTime,
               "Binary Time": getBinTime,
               "Roman Time": getRomanTime,
               "Morse Time": getMorseTime}


#
# ----------------------------------------------------- called to test, if run as main (nit imported) ------------------
#
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
