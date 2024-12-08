# Updated Dec 6 5:02 PM EST

import notepad
import asyncio
import sys
import os
import ttkbootstrap
import multiprocessing
import flet as ft
from flet_timer.flet_timer import Timer
import tkinter as tk
import time
import tkinter.font as tkFont
from tkinter import *
from ttkbootstrap import Window, Style
from ttkbootstrap.constants import *
from tkinter.messagebox import showinfo, showerror
from tkinter.filedialog import askopenfilename, asksaveasfilename
# import timer since this will be important later on to integrate timer with the document function itself
from threading import Timer # For calling the timer function
# import fpdf so user can save file as a pdf, though this will be done automatically later on
from fpdf import FPDF  # For saving files as PDF

if sys.platform == "darwin":
    from tkinter import _tkinter
    _tkinter.TkVersion = 8.6
    os.environ['TK_SILENCE_DEPRECATION'] = '1'


def start_tkinter(pipe):
    """Tkinter app function (main notepad)"""

    notepad_window = notepad.Notepad(pipe)
    notepad_window.run()

def start_flet(pipe):
    """Flet app function."""
    # Send message to Tkinter
    def send_to_tkinter(message):
        pipe.send(message)

    async def main(page: ft.Page):
        # Add a Timer to periodically check the pipe
        async def check_pipe():
            while True:
                # Check if there's a message
                if pipe.poll():
                    # Receive the message
                    msg = pipe.recv()
                    if msg == "Idle expired":
                        stop_count[0] = False
                        await start_timer()
                    elif msg == "End":
                        page.window.close()
                await asyncio.sleep(0.1)
        asyncio.create_task(check_pipe())

        """Implement timer"""
        # Page formatting
        page.theme_mode = ft.ThemeMode.SYSTEM
        page.window.center()
        page.horizontal_alignment = "center"
        page.vertical_alignment = "center"
        page.padding = 40
        page.window.frameless = True
        page.window.always_on_top = True
        page.window.height = 350
        page.window.width = 425

        minutes = ft.Dropdown(label = "Minutes", hint_text = "0 to 10", width = "125")
        for i in range(11): minutes.options.append(ft.dropdown.Option(i))
        minutes.value = 0
        seconds = ft.Dropdown(label = "Seconds", hint_text = "1 to 59", width = "125")
        for i in range(1, 60): seconds.options.append(ft.dropdown.Option(i))
        dialog = ft.AlertDialog(bgcolor = "#85A27F", title = ft.Text("Please enter a valid number for minutes (0 to 10) and seconds (1 to 59). Click outside the dialog to exit."))

        async def start_writing(e):
            # Update UI
            start_button.visible = False
            pause_button.visible = True

            instruction.value = "Type away! :)"
            hint.value = "The timer will begin after 5 seconds of inactivity. Whether you press done prematurely or the timer expires, there's no turning back."
            page.update()

            # Send message to tkinter
            send_to_tkinter("User started")
            print("User started")

        async def start_timer():
            # Stop the timer
            if stop_count[0] == False:
                try:
                    minutes_value = int(minutes.value)
                    seconds_value = int(seconds.value)
                except:
                    page.open(dialog)
                    return
                
                instruction.value = "Timer started! Write as much as you can before it's all gone..."
                hint.value = "LOCK IN"
                page.update()

                send_to_tkinter("Timer started")
                print("Timer started")
                #stop_count[0] = False
                await update_timer(minutes_value, seconds_value)

        async def update_timer(minutes_value, seconds_value):
            # Calculate seconds remaining and start countdown
            total_seconds = (minutes_value * 60) + seconds_value

            for remaining in range(total_seconds, -1, -1):
                if stop_count[0]:
                    timer.value = "{:02d} min {:02d} sec".format(minutes_value, seconds_value)
                    page.update()
                    return
                else:
                    minutes_update, seconds_update = divmod(remaining, 60)
                    timer.value = "{:02d} min {:02d} sec".format(minutes_update, seconds_update)
                    page.update()
                    await asyncio.sleep(1)

            if stop_count[0] == False:
                send_to_tkinter("Timer expired")
                hint.value = "How did you do?"

        # Pause the timer
        def pause_timer(e):
            start_button.visible = False
            pause_button.visible = False
            stop_count[0] = True

            instruction.value = "Timer paused. You can no longer edit. Make sure to save!"
            hint.value = "Congrats! ...Did you actually finish it?"
            page.update()

            send_to_tkinter("Done")
            print("Done")
        
        # Set up display and stop_count variable to control pausing
        timer = ft.Text("__ min __ sec", size = 30)
        start_button = ft.ElevatedButton("Start", on_click =  start_writing, color = "#85A27F")
        pause_button = ft.ElevatedButton("Done!", on_click = pause_timer, color = "#85A27F", visible = False)
        instruction = ft.Text("Press the start button before you can start typing!", size = 15)
        hint = ft.Text("Set a timer for the time left to work before your session ends. (Max: 10 mins)")
        stop_count = [False]

        # Add controls to page
        page.add(instruction, ft.Container(padding = 2), ft.Row([minutes, seconds, start_button, pause_button], alignment = "center"), ft.Container(padding = 2), timer, ft.Container(padding = 1), hint, ft.Container(padding = 2))
        send_to_tkinter("Not started")
        print("Not started")

    ft.app(target=main)


if __name__ == "__main__":
    # Use a Pipe for inter-process communication
    parent_conn, child_conn = multiprocessing.Pipe()

    # Start Tkinter in a subthread
    tk_process = multiprocessing.Process(target=start_tkinter, args=(parent_conn,))
    tk_process.start()

    try:
        # Run Flet in the main thread
        start_flet(child_conn)
    finally:
        tk_process.terminate()
        tk_process.join()
