import PySimpleGUI as sg

"""
    Allows you to "browse" through the Theme settings.  Click on one and you"ll see a
    Popup window using the color scheme you chose.  It"s a simple little program that also demonstrates
    how snappy a GUI can feel if you enable an element"s events rather than waiting on a button click.
    In this program, as soon as a listbox entry is clicked, the read returns.
"""

def run_theme():
    theme = None
    sg.theme("Dark Brown")


    layout = [[sg.Text("Theme Browser")],
              [sg.Text("Click a Theme color to see demo window")],
              [sg.Listbox(values=sg.theme_list(), size=(20, 12), key="-LIST-", enable_events=True)],
              [sg.OK(), sg.Cancel()]
             ]

    window = sg.Window("Theme Browser", layout)

    while True:  # Event Loop
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Cancel"):
            break
        elif event == "OK":
            theme = values["-LIST-"][0]
            break

        theme = values["-LIST-"][0]
        sg.theme(theme)
        sg.popup_get_text(f"This is {theme}")


    window.close(); del window

    return theme
