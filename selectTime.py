# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 15:42:00 2015

@author: scottk2
"""

import datetime
import time
import math

import timeCodes as tc


class SelectTime:
    """   A class which allows the current time to be displays in various formats.
    The formats are held in the enum TimeTypes, these are exported.

    TimeType is set to the desired time format [from TimeTypes]
    getTime is then called and this will return the current time is the desired time format."""

    __types = ("Fuzzy Time", "Time in Words", "GMT Time", "Local Time", "UTC Time", "Swatch Time", "New Earth Time",
               "Julian Time", "Decimal Time", "True Hex Time", "Hex Time", "Oct Time", "Binary Time", "Roman Time",
               "Morse Time", "Mars Sol Date", "Coordinated Mars Time", "Flow Time", "Percent Time", "Metric Time",
               "Unix Time")
#
#  the class is access by the following properties only.
#  getTime can't be made a proper property, this seems to upset the dictionary of functions - they are not callable.

    @property
    def timeTypes(self):
        """ Returns a tuple of available Time types."""
        return self.__types

    def getTime(self, position=0):
        """ Returns a function to return the time as position f in timeTypes."""
        return self.__funcs[position](self)


# -------------------------------------------------------------------------------- time functions ----------------------
#
# The time functions can't be made property's, this seems to upset the dictionary of functions - they are not callable.
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

        __hour, __mins, __secs = self.__getNowTime()
        __nrms = __mins - (__mins % 5)  # gets nearest five minutes
        __sRtn = ""

        __ampm = "in the morning" if __hour < 12 else "pm"

        if (__mins % 5) > 2:
            __nrms += 5  # closer to next five minutes, go to next

        __sRtn = tc.minsText[__nrms]  # look up text for minutes.

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
                __fuzzyTime = "about {0}'ish {1}".format(tc.hours[__hour], __ampm)
            else:
                __fuzzyTime = "{0} {1} {2}".format(__sRtn, tc.hours[__hour], __ampm)

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
            __minsStr = "{0} o'clock {1}".format(tc.hours[__hour], __ampm)
        elif 1 <= __mins <= 9:
            __minsStr = "{0} minutes {1} {2} {3}".format(tc.units[__mins], __pasTo, tc.hours[__hour], __ampm)
        elif 10 <= __mins <= 20:
            __minsStr = "{0} minutes {1} {2} {3}".format(tc.tens[__mins-9], __pasTo, tc.hours[__hour], __ampm)
        elif 21 <= __mins <= 29:
            __minsTens = math.floor(__mins / 10)
            __minsUnit = __mins - (__minsTens * 10)
            __minsStr = "twenty{0} minutes {1} {2} {3}".format(tc.units[__minsUnit], __pasTo, tc.hours[__hour], __ampm)
        else:
            __minsStr = "thirty minutes past {0} {1}".format(tc.hours[__hour], __ampm)

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

        __Rhour = tc.romanNumerals[__hour]
        __Rmins = tc.romanNumerals[__mins]
        __Rsecs = tc.romanNumerals[__secs]

        return "{0}:{1}:{2}".format(__Rhour, __Rmins, __Rsecs)

# ------------------------------------------------------------------------------------- getMorseTime -------------------
    def getMorseTime(self):
        """   Returns the current [local] time with each digit represented bu a Morse code."""

        __hour, __mins, __secs = self.__getNowTime()

        if __hour < 10:
            __Mhour = "{0} {1}".format(tc.morseCode[0], tc.morseCode[__hour])
        else:
            __Mhour = "{0} {1}".format(tc.morseCode[int(__hour/10)], tc.morseCode[__hour % 10])

        if __mins < 10:
            __Mmins = "{0} {1}".format(tc.morseCode[0], tc.morseCode[__mins])
        else:
            __Mmins = "{0} {1}".format(tc.morseCode[int(__mins/10)], tc.morseCode[__mins % 10])

        if __secs < 10:
            __Msecs = "{0} {1}".format(tc.morseCode[0], tc.morseCode[__secs])
        else:
            __Msecs = "{0} {1}".format(tc.morseCode[int(__secs/10)], tc.morseCode[__secs % 10])

        return "{0}:{1}:{2}".format(__Mhour, __Mmins, __Msecs)

# ------------------------------------------------------------------------------------- getMarsSolDate------------------
    def getMarsSolDate(self):
        """   Returns the current [UTC] time as Mars Sol Date.

        see http://jtauber.github.io/mars-clock/"""

        __SolDataEpoch = datetime.datetime(day=6, month=1, year=2000)
        __utcNow = datetime.datetime.utcnow()
        __daysSinceEpoch = (__utcNow - __SolDataEpoch).days + (__utcNow - __SolDataEpoch).seconds / 86400

        return "{0:5.5f}".format((__daysSinceEpoch / 1.027491252) + 44796.0 - 0.00096)

# ------------------------------------------------------------------------------------- getCoordinatedMarsTime ---------
    def getCoordinatedMarsTime(self):
        """   Returns the current [UTC] time as Coordinated Mars Time.

        see http://jtauber.github.io/mars-clock/"""

        __SolDataEpoch = datetime.datetime(day=6, month=1, year=2000)
        __utcNow = datetime.datetime.utcnow()
        __daysSinceEpoch = (__utcNow - __SolDataEpoch).days + (__utcNow - __SolDataEpoch).seconds / 86400

        __marsSolDate = (__daysSinceEpoch / 1.027491252) + 44796.0 - 0.00096

        __mtc = (24 * __marsSolDate) % 24

        __hour = int(__mtc)
        __mins = (__mtc - __hour) * 60
        __secs = (__mins - int(__mins)) * 60

        return "{0:0>2.0f}:{1:0>2.0f}:{2:0>2.0f}".format(__hour, __mins, __secs)

# ------------------------------------------------------------------------------------- getFlowTime -------------------
    def getFlowTime(self):
        """   Returns the current [local] time as Flow Time.
        Flow Time still divides the day into 24 hours, but each hour is divided into 100 minutes of 100 seconds.
        A Quick conversion is takes 2/3 of the minute [or second] and add it to it's self."""

        __hour, __mins, __secs = self.__getNowTime()
        __mins *= (5/3)
        __secs *= (5/3)

        return "{0:0>2}h {1:0>2.0f}m {2:0>2.0f}s".format(__hour, __mins, __secs)

# ------------------------------------------------------------------------------------- getPercentTime -----------------
    def getPercentTime(self):
        """   Returns the current [local] time as a percent of the day.
        See http://raywinstead.com/metricclock.shtml """

        __hour, __mins, __secs = self.__getNowTime()

        __noOfSeconds = (__hour * 3600) + (__mins * 60) + __secs
        __percentSeconds = __noOfSeconds / 86400 * 100

        return "{0:2.4f} PMH".format(__percentSeconds)

# ------------------------------------------------------------------------------------- getMetricTime ------------------
    def getMetricTime(self):
        """   Returns the current [local] time in Metric time.
        Metric time is the measure of time interval using the metric system, which defines the second as the base unit of time,
        and multiple and submultiple units formed with metric prefixes, such as kiloseconds and milliseconds.
        Only Kiloseconds are used here."""

        __hour, __mins, __secs = self.__getNowTime()

        __noOfSeconds = ((__hour * 3600) + (__mins * 60) + __secs) / 1000

        return "{0} Kiloseconds".format(__noOfSeconds)

# ------------------------------------------------------------------------------------- getUnixTime --------------------
    def getUnixTime(self):
        """   Returns UTC in Unix time.
        Unix time, or POSIX time, is a system for describing instants in time, defined as the number of seconds
        elapsed since midnight Coordinated Universal Time (UTC) of Thursday, January 1, 1970  """

        __tday = datetime.datetime.utcnow()
        __epoch = datetime.datetime(1970, 1, 1)
        __secs = (__tday - __epoch).total_seconds()

        return "{0:.0f}".format(__secs)

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
               "Morse Time": getMorseTime,
               "Mars Sol Date": getMarsSolDate,
               "Coordinated Mars Time": getCoordinatedMarsTime,
               "Flow Time": getFlowTime,
               "Percent Time": getPercentTime,
               "Metric Time": getMetricTime,
               "Unix Time": getUnixTime}


#
# ----------------------------------------------------- called to test, if run as main (not imported) ------------------
#
if __name__ == "__main__":
    import tkinter as tk
    import tkinter.ttk as ttk

    def update_timeText():
        # Get the current time
        current = s.getTime(position=timeCombo.get())

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
