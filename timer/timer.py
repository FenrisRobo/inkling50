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

    seconds = ft.TextField(hint_text = "Seconds", border_radius = 30, width = 120, text_align = "center")

    def start_timer(e):
        button.visible = False
        seconds_value = int(eval(seconds.value))

        while seconds_value:
            mins, secs = divmod(seconds_value, 60)
            timer.value = "{:02d} min {:02d} sec".format(mins, secs)
            time.sleep(1)
            seconds_value = seconds_value - 1
            page.update()

        time.sleep(1)
        timer.value = "{:02d} min {:02d} sec".format(mins, seconds_value)
        button.visible = True
        page.update()
    
    timer = ft.Text(style = "displayLarge", color = "white")
    button = ft.ElevatedButton("Set Timer", on_click =  start_timer, color = "#85A27F")

    page.add(ft.Container(padding = 20), ft.Row([seconds, button], alignment = "center"), ft.Container(padding = 20), timer, ft.Container(padding = 20))

ft.app(main)