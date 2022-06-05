About Klock

Klock - a clock with a k.

Written in Python 3.10.4

Klock will consist of a number of views, selected by a row of buttons along the bottom.

The first view is Fuzzy Time.
    The will display the current time in a number of different modes.
        i.e. in Words, in Hex, in Roman Numerals, in Binary etc.
    The font of the time can also be changed.

The second view completed in Stopwatch.
    This consists a clock face to display hours, minutes and seconds and a row of buttons.
    The buttons allow for the timer to be started, stopped, resumed, paused and cleared.

The third view completed is a Countdown Timer.
    This allows a time interval to be set, either via a spin control or pre-set buttons,
    and the time will count down to zero.

The fourth view is a World Klock.
    This displays the time in a given time zone, that is selected from a drop down list.

The fifth view is reminders.
    This allows a reminder to be entered with eiter a due dat or due time {or both].
    A notification is displayed when the reminder is due.


or will be [similar to lazKlock & klock.vb], at the moment a trying ground for ideas.
Stuff that I come across that might be useful.

Contains one sub project, pyDigitalKlock.
    This a simple app that tries to reproduce a LED Digital Klock.
    It allows the user to change the foreground and background colours.
    The background can also be switched to transparent.
    The font can also be selected from from a selection of fonts.
    It save the colours, font and app position between sessions.

One becomes two.
    the first pyDigitalKlock was built using pygubu, the second was built using pySimpleGui.
    The latter look better and more simple to use, maybe the way to go.


