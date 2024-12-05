import tkinter as tk
import tkinter.font as tkFont

window = tk.Tk()

# Create a custom font
custom_font = tkFont.Font(family="Arial", size=12, weight="bold", slant="italic")

label = tk.Label(window, text="Hello, World!", font=custom_font)
label.pack()

window.mainloop()