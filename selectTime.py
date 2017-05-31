import datetime
import time

class SelectTime:

    @property
    def timeTypes(self):
        """ Retruns a list(tuple) of available Time types."""
        return ("GMT", "Fuzzy Time")
        
    @property      
    def getGMTTime(self):
        """ returns curent time as GMT."""
        return time.strftime("%H:%M:%S", time.gmtime())

    @property 
    def getFuzzyTime(self):
        """ Returns current time as Fuzzy Time."""
        
        hours = {0: "twelve", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", \
                 7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve"}

        minsText = {0: "", 5: "five past", 10: "ten past", 15: "quarter past",   \
                    20: "twenty past", 25: "twenty-five past", 30: "half past",  \
                    35: "twenty-five to", 35: "twenty-five to", 40: "twenty to", \
                    45: "quarter to", 50: "ten to", 55: "five to", 60: ""}
        
        now = datetime.datetime.now()

        __hour = now.hour
        __mins = now.minute
        __nrms = __mins - (__mins % 5)          # gets nearest five minutes
        __sRtn = ""

        __ampm = "in the morning" if __hour < 12 else "pm"

        if (__mins % 5) > 2:
            __nrms += 5               # closer to next five minutes, go to next
            
        __sRtn = minsText[__nrms]     #  look up text for minutes.

        if __nrms > 30:
            __hour += 1

        #   generate output string according to the hour of the day.
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




if __name__ == "__main__":
    import tkinter as tk
    import tkinter.ttk as ttk

    def update_timeText():
        # Get the current time
        current = s.getFuzzyTime

        # Update the timeText label box with flexi time.
        timeText.configure(text=current)

        #  Call the update_timeText() function every 1 second.
        root.after(1000, update_timeText)

    s = SelectTime()

    root = tk.Tk()
    root.wm_title("SelectTime Test")

    # create a conbo box
    timevar = tk.StringVar()
    timeCombo = ttk.Combobox(root, textvariable=timevar, values=s.timeTypes)
    timeCombo.current(0)
    timeCombo.pack()

    # create a timeText label (a text box)
    timeText = ttk.Label(root, text="", font=("Helvetica", 20))
    timeText.pack()

    update_timeText()
    root.mainloop()
