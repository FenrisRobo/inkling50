import flet as ft
import time

def main(page: ft.Page) -> None:
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.padding = 40
    page.window_frameless = True
    page.window_height = 510
    page.window_width = 490

    minutes = ft.Dropdown(label = "Minutes", hint_text = "0 to 10", width = "125")
    for i in range(11): minutes.options.append(ft.dropdown.Option(i))
    seconds = ft.Dropdown(label = "Seconds", hint_text = "1 to 59", width = "125")
    for i in range(1, 60): seconds.options.append(ft.dropdown.Option(i))
    dialog = ft.AlertDialog(bgcolor = "#85A27F", title = ft.Text("Please enter a valid number for minutes (0 to 10) and seconds (1 to 59). Click outside the dialog to exit."))

    def start_timer(e):
        start_button.visible = False
        pause_button.visible = True

        try:
            minutes_value = int(minutes.value)
            seconds_value = int(seconds.value)
        except:
            page.open(dialog)
            return
    
        seconds_remaining = (minutes_value * 60) + seconds_value
        countdown(seconds_remaining, minutes_value, seconds_value, stop_count)
    
    def pause_timer(e):
        global seconds_remaining
        start_button.visible = True
        pause_button.visible = False
        
        if stop_count[0] == True:
            stop_count[0] = False
            seconds_remaining = 0
        else:
            stop_count[0] = True
    
    def countdown(seconds_remaining, minutes_value, seconds_value, stop_count):
        while seconds_remaining and not stop_count[0]:
            minutes_update, seconds_update = divmod(seconds_remaining, 60)
            timer.value = "{:02d} min {:02d} sec".format(minutes_update, seconds_update)
            time.sleep(1)
            seconds_remaining -= 1
            page.update()

        time.sleep(1)
        timer.value = "{:02d} min {:02d} sec".format(minutes_value, seconds_value)
        start_button.visible = True
        pause_button.visible = False
        page.update()
    
    timer = ft.Text(style = "displayLarge", color = "white")
    start_button = ft.ElevatedButton("Start", on_click =  start_timer, color = "#85A27F")
    pause_button = ft.ElevatedButton("Pause", on_click = pause_timer, color = "#85A27F", visible = False)
    stop_count = [False]

    page.add(ft.Container(padding = 20), ft.Row([minutes, seconds, start_button, pause_button], alignment = "center"), ft.Container(padding = 20), timer, ft.Container(padding = 20))

ft.app(main)