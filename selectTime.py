import datetime
import time

class SelectTime:

    def getGMTTime(self):

        return time.strftime("%H:%M:%S", time.gmtime())



    def getFuzzyTime(self):

        hours = {0: "twelve", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", \
                 7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve"}

        now = datetime.datetime.now()

        hour = now.hour
        mins = now.minute
        nrms = mins - (mins % 5)					#	gets nearest five minutes
        sRtn = ""

        ampm = "in the morning" if hour < 12 else "pm"

        if (mins % 5) > 2:
            nrms += 5								#	closer to next five minutes, go to next

        if nrms == 0:
            sRtn = ""
        elif nrms == 5:
            sRtn = "five past"
        elif nrms == 10:
            sRtn = "ten past"
        elif nrms == 15:
            sRtn = "quarter past"
        elif nrms == 20:
            sRtn = "twenty past"
        elif nrms == 25:
            sRtn = "twenty-five past"
        elif nrms == 30:
            sRtn = "half past"
        elif nrms == 35:
            sRtn = "twenty-five to"
        elif nrms == 40:
            sRtn = "twenty to"
        elif nrms == 45:
            sRtn = "quarter to"
        elif nrms == 50:
            sRtn = "ten to"
        elif nrms == 55:
            sRtn = "five to"
        elif nrms == 60:
            sRtn = ""

        if nrms > 30:
            hour += 1

        #   generate output string according to the hour of the day.
        #   This looks more complicated then it should be, maybe separate if then's would be better.

        #   if the hour is 0 or 24 and no minutes - it must be midnight.
        #   if the hour is 12 and no minutes - it must be noon.

        #   if "pm" then afternoon, subtract 12 - only use 12 hour clock.

        if hour == 12 and sRtn == "":
            fuzzyTime = "about Noon"
        elif hour == 0 and sRtn == "":
            fuzzyTime = "about Midnight"
        elif hour == 24 and sRtn == "":
            fuzzyTime = "about Midnight"
        else:
            if ampm == "pm":
                hour -= 12
                ampm = "in the evening" if hour > 5 else "in the afternoon"
            if sRtn == "":
                fuzzyTime = "about {0} ish {1}".format(hours[hour], ampm)
            else:
                fuzzyTime = "{0} {1} {2}".format(sRtn, hours[hour], ampm)

        return fuzzyTime


if __name__ == "__main__":
    import tkinter as tk
    import tkinter.ttk as ttk

    def update_timeText():
        # Get the current time
        current = s.getGMTTime()

        # Update the timeText label box with flexi time.
        timeText.configure(text=current)

        #  Call the update_timeText() function every 1 second.
        root.after(1000, update_timeText)

    s = SelectTime()
    timeList = ("1", "2")

    root = tk.Tk()
    root.wm_title("SelectTime")

    # create a conbo box
    timevar = tk.StringVar()
    timeCombo = ttk.Combobox(root, textvariable=timevar, values=timeList)
    timeCombo.pack()

    # create a timeText label (a text box)
    timeText = tk.Label(root, text="", font=("Helvetica", 20))
    timeText.pack()

    update_timeText()
    root.mainloop()