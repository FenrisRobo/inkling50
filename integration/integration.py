import multiprocessing
import flet as ft
from flet_timer.flet_timer import Timer
import tkinter as tk

def start_tkinter(pipe):
    """Tkinter app function (main notepad)"""

    # Send message to Flet
    def send_to_flet():
        pipe.send("Hello from Tkinter!")

    root = tk.Tk()
    root.title("Main notepad")

    btn = tk.Button(root, text="Send to Flet", command=send_to_flet)
    btn.pack(pady=20)

    label = tk.Label(root, text="Tkinter Running...")
    label.pack(pady=20)

    root.mainloop()

def start_flet(pipe):
    """Flet app function."""

    # Send message to Tkinter
    def send_to_tkinter(e):
        pipe.send("Hello from Flet!")

    def main(page: ft.Page):
        messages_list = ft.Column()

        # Add UI elements
        page.add(
            ft.Text("Flet Running..."),
            ft.ElevatedButton("Send to Tkinter", on_click=send_to_tkinter),
            messages_list,
        )

        def check_pipe():
            # Check if there's a message
            if pipe.poll():
                # Receive the message
                msg = pipe.recv()
                # Display message in Flet
                messages_list.controls.append(ft.Text(msg))
                page.update()

        # Add a Timer to periodically check the pipe
        page.add(Timer(name = "timer", interval_s = 0.5, callback = check_pipe))  # Check every 0.5 seconds

    ft.app(target=main)

if __name__ == "__main__":
    # Use a Pipe for inter-process communication
    parent_conn, child_conn = multiprocessing.Pipe()

    # Start Tkinter in a subthread
    tk_process = multiprocessing.Process(target=start_tkinter, args=(child_conn,))
    tk_process.start()

    # Run Flet in the main thread
    start_flet(parent_conn)