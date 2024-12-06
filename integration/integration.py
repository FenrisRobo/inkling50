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



##########################################################

def start_tkinter(pipe):
    """Tkinter app function (main notepad)"""

    # Send message to Flet
    def send_to_flet():
        pipe.send("Hello from Tkinter!")

    #root = tk.Tk()
    Notepad().run()
    #root.title("Main notepad")
    #root.mainloop()

def start_flet(pipe):
    """Flet app function."""
    # Send message to Tkinter
    def send_to_tkinter(message, e):
        pipe.send(message)

    def main(page: ft.Page):
        def check_pipe():
            # Check if there's a message
            if pipe.poll():
                # Receive the message
                msg = pipe.recv()

        # Add a Timer to periodically check the pipe
        page.add(Timer(name = "timer", interval_s = 0.5, callback = check_pipe))  # Check every 0.5 seconds

        """Implement timer"""
        # Page formatting
        page.theme_mode = ft.ThemeMode.SYSTEM
        page.window.center()
        page.horizontal_alignment = "center"
        page.vertical_alignment = "center"
        page.padding = 40
        page.window.frameless = True
        page.window.always_on_top = True
        page.window.height = 300
        page.window.width = 425

        minutes = ft.Dropdown(label = "Minutes", hint_text = "0 to 10", width = "125")
        for i in range(11): minutes.options.append(ft.dropdown.Option(i))
        seconds = ft.Dropdown(label = "Seconds", hint_text = "1 to 59", width = "125")
        for i in range(1, 60): seconds.options.append(ft.dropdown.Option(i))
        dialog = ft.AlertDialog(bgcolor = "#85A27F", title = ft.Text("Please enter a valid number for minutes (0 to 10) and seconds (1 to 59). Click outside the dialog to exit."))

        def start_timer(e):
            # Buttons for testing
            start_button.visible = False
            pause_button.visible = True

            # Convert user input to int
            try:
                minutes_value = int(minutes.value)
                seconds_value = int(seconds.value)
            except:
                page.open(dialog)
                return

            # Calculate seconds remaining and start countdown
            seconds_remaining = (minutes_value * 60) + seconds_value
            send_to_tkinter("Timer started")

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
        
        # Pause the timer
        def pause_timer(e):
            send_to_tkinter("Timer paused")

            if stop_count[0] == True:
                stop_count[0] = False
            else:
                stop_count[0] = True
                start_button.visible = True
                start_button.disabled = False
                pause_button.visible = False

        # Set up display and stop_count variable to control pausing
        timer = ft.Text(size = 30)
        start_button = ft.ElevatedButton("Start", on_click =  start_timer, color = "#85A27F")
        pause_button = ft.ElevatedButton("Done!", on_click = pause_timer, color = "#85A27F", visible = False)
        stop_count = [False]

        # Add controls to page
        page.add(ft.Text("Select the duration of idle activity before your document deletes. (Max: 10 mins)"), ft.Container(padding = 5), ft.Row([minutes, seconds, start_button, pause_button], alignment = "center"), ft.Container(padding = 5), timer, ft.Container(padding = 5)) 

    ft.app(target=main)

if __name__ == "__main__":
    # Use a Pipe for inter-process communication
    parent_conn, child_conn = multiprocessing.Pipe()

    # Start Tkinter in a subthread
    tk_process = multiprocessing.Process(target=start_tkinter, args=(child_conn,))
    tk_process.start()

    # Run Flet in the main thread
    start_flet(parent_conn)