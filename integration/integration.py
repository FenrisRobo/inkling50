import threading
import queue
import flet as ft
import tkinter as tk

# Shared queue for communication between threads
message_queue = queue.Queue()

# tkinter app function (main notepad)
def start_tkinter():
    # Send message to flet
    def send_to_flet():
        message_queue.put("Hello from Tkinter!")

    root = tk.Tk()
    root.title("Main Notepad")

    btn = tk.Button(root, text="Send to Flet", command=send_to_flet)
    btn.pack(pady=20)

    label = tk.Label(root, text="Tkinter Running...")
    label.pack(pady=20)

    root.mainloop()

# Flet app function
def start_flet(page: ft.Page):
    def check_queue():
        while not message_queue.empty():
            msg = message_queue.get()
            messages_list.controls.append(ft.Text(msg))
            page.update()
    
    # Send message to tkinter
    def send_to_tkinter(e):
        message_queue.put("Hello from Flet!")
    
    messages_list = ft.Column()
    page.add(
        ft.Text("Flet Running..."),
        ft.ElevatedButton("Send to Tkinter", on_click=send_to_tkinter),
        messages_list,
    )
    
    # Check for messages from tkinter
    page.add(ft.Timer(0.5. check_queue))

# Start tkinter in a side thread
tkinter_thread = threading.Thread(target = start_tkinter, daemon = True)
tkinter_thread.start()

# Start Flet in the main thread
ft.app(target = start_flet)