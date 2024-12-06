import sys
import os
import ttkbootstrap
import platform
import flet as ft
import tkinter as tk
import tkinter.font as tkFont
import ctypes
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

class Notepad(Tk):
    def __init__(self, pipe):
        super().__init__()
        self.pipe = pipe
        self.running = True

        # Initialize the root window with ttkbootstrap
        self.__root = Window(themename="classic") # start with window, style it journal
        self.__root.title("Notepad") # title the window notepad
        self.__root.geometry("800x600")  # Default size

        # Set up text area with default font
        self.__thisTextArea = Text(self.__root, wrap=WORD, undo=True, font=("Calibri", 12))
        self.__file = None 

        # Create menu bar and status bar
        self.__thisMenuBar = Menu(self.__root) # Create new root to menu function from tkinter library
        self.__createMenuBar() # Create new function later on 
        self.__createStatusBar()

        # Toolbar setup
        self.__createToolbar()

        # Add scrollbars
        self.__thisScrollBar = Scrollbar(self.__root, command=self.__thisTextArea.yview)
        self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)
        self.__thisScrollBar.grid(row=1, column=2, sticky=NS)
        self.__thisTextArea.grid(row=1, column=1, sticky=NSEW)

        # Configure resizing weights
        self.__root.grid_rowconfigure(1, weight=1)
        self.__root.grid_columnconfigure(1, weight=1)

        # Idle timer setup
        self.idle_time_limit = 5000  # milliseconds
        self.idle_timer = None

        self.check_pipe_id = self.after(100, self.check_pipe)

        # Bind events
        self.__bindEvents()
    
    # Send message to Flet
    def send_to_flet(self, message):
        self.pipe.send(message)
    
    def check_pipe(self):
        if not self.running:
            return
        
        if self.pipe.poll():
            msg = self.pipe.recv()
            print("1 {msg}")
            if msg in ["Not started", "Timer paused"]:
                self.__disableTyping()
                pass
            elif msg == "User started":
                self.__enableTyping()
        self.after(100, self.check_pipe)

    def run(self):
        """Run the main application loop."""
        self.__root.mainloop()

    def __bindEvents(self):
        self.__root.bind("<Key>", self.__onKeyPress)
        self.__root.bind("<Configure>", self.__adjustSize)
        self.__root.bind("<Control-b>", lambda event: self.__makeBold())
        self.__root.bind("<Control-i>", lambda event: self.__makeItalic())
        self.__root.bind("<Control-u>", lambda event: self.__makeUnderline())
        self.__thisTextArea.bind("<KeyRelease>", self.__updateWordCount)

        # Disable copy-paste key bindings
        self.__thisTextArea.bind("<Control-c>", self.__disableAction)
        self.__thisTextArea.bind("<Control-v>", self.__disableAction)
        self.__thisTextArea.bind("<Command-c>", self.__disableAction)  # macOS Copy
        self.__thisTextArea.bind("<Command-v>", self.__disableAction)  # macOS Paste

    def __onKeyPress(self, event):
        self.__resetIdleTimer()

    def __resetIdleTimer(self):
        if self.idle_timer is not None:
            self.__root.after_cancel(self.idle_timer)
        self.idle_timer = self.__root.after(self.idle_time_limit, self.__deleteDocument)

    def __deleteDocument(self):

        # Add some comments or message here before it's deleted in Fletch

        self.__thisTextArea.delete(1.0, "end")
        self.__disableTyping()

    def __disableTyping(self):
        self.__thisTextArea.config(state="disabled")
    
    def __enableTyping(self):
        self.__thisTextArea.config(state="normal")

    def __createMenuBar(self):
        file_menu = Menu(self.__thisMenuBar, tearoff=0)
        file_menu.add_command(label="New", command=self.__newFile)
        file_menu.add_command(label="Open", command=self.__openFile)
        file_menu.add_command(label="Save", command=self.__saveFile)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.__quitApplication)
        self.__thisMenuBar.add_cascade(label="File", menu=file_menu)

        format_menu = Menu(self.__thisMenuBar, tearoff=0)
        format_menu.add_command(label="Bold", command=self.__makeBold)
        format_menu.add_command(label="Italic", command=self.__makeItalic)
        format_menu.add_command(label="Underline", command=self.__makeUnderline)
        format_menu.add_command(label="Bold + Underline", command=self.__makeBoldUnderline)
        format_menu.add_command(label="Italic + Underline", command=self.__makeItalicUnderline)
        format_menu.add_command(label="Bold + Italic", command=self.__makeBoldItalic)
        format_menu.add_command(label="Bold + Italic + Underline", command=self.__makeBoldItalicUnderline)
        self.__thisMenuBar.add_cascade(label="Format", menu=format_menu)

        help_menu = Menu(self.__thisMenuBar, tearoff=0)
        help_menu.add_command(label="About Notepad", command=self.__showAbout)
        self.__thisMenuBar.add_cascade(label="Help", menu=help_menu)

        self.__root.config(menu=self.__thisMenuBar)

    def __createToolbar(self):
        # Create a toolbar frame
        toolbar = Frame(self.__root, height=30, bg="lightgray")
        toolbar.grid(row=0, column=0, columnspan=3, sticky=W + E)

        # Buttons for text formatting
        bold_btn = Button(toolbar, text="B", command=self.__makeBold, font=("Calibri", 12, "bold"), width=3)
        bold_btn.grid(row=0, column=0, padx=5, pady=5)

        italic_btn = Button(toolbar, text="I", command=self.__makeItalic, font=("Calibri", 12, "italic"), width=3)
        italic_btn.grid(row=0, column=1, padx=5, pady=5)

        underline_btn = Button(toolbar, text="U", command=self.__makeUnderline, font=("Calibri", 12, "underline"), width=3)
        underline_btn.grid(row=0, column=2, padx=5, pady=5)

        # Buttons for advanced text formatting

        bold_underline_btn = Button(toolbar, text="B+U", command=self.__makeBoldUnderline, font=("Calibri", 12, "bold", "underline"), width=4)
        bold_underline_btn.grid(row=0, column=3, padx=5, pady=5)

        italic_underline_btn = Button(toolbar, text="I+U", command=self.__makeItalicUnderline, font=("Calibri", 12, "italic", "underline"), width=4)
        italic_underline_btn.grid(row=0, column=4, padx=5, pady=5)

        bold_italic_btn = Button(toolbar, text="B+I", command=self.__makeBoldItalic, font=("Calibri", 12, "bold", "italic"), width=4)
        bold_italic_btn.grid(row=0, column=5, padx=5, pady=5)

        bold_italic_underline_btn = Button(toolbar, text="B+I+U", command=self.__makeBoldItalicUnderline, font=("Calibri", 12, "bold", "italic", "underline"), width=5)
        bold_italic_underline_btn.grid(row=0, column=6, padx=5, pady=5)

        # Buttons for center text, highlight, and text color

        centerTextButton = Button(toolbar, text="Center Text", command=self.__centerText)
        centerTextButton.grid(row=0, column=7, padx=5, pady=5)

        highlightBlackButton = Button(toolbar, text="Highlight Black", command=lambda: self.__highlightText("black"))
        highlightBlackButton.grid(row=0, column=8, padx=5, pady=5)

        highlightBlueButton = Button(toolbar, text="Highlight Blue", command=lambda: self.__highlightText("blue"))
        highlightBlueButton.grid(row=0, column=9, padx=5, pady=5)

        highlightRedButton = Button(toolbar, text="Highlight Red", command=lambda: self.__highlightText("red"))
        highlightRedButton.grid(row=0, column=10, padx=5, pady=5)

        highlightGreenButton = Button(toolbar, text="Highlight Green", command=lambda: self.__highlightText("green"))
        highlightGreenButton.grid(row=0, column=11, padx=5, pady=5)

        textColorBlackButton = Button(toolbar, text="Text Black", command=lambda: self.__changeTextColor("black"))
        textColorBlackButton.grid(row=0, column=12, padx=5, pady=5)

        textColorBlueButton = Button(toolbar, text="Text Blue", command=lambda: self.__changeTextColor("blue"))
        textColorBlueButton.grid(row=0, column=13, padx=5, pady=5)

        textColorRedButton = Button(toolbar, text="Text Red", command=lambda: self.__changeTextColor("red"))
        textColorRedButton.grid(row=0, column=14, padx=5, pady=5)

        textColorGreenButton = Button(toolbar, text="Text Green", command=lambda: self.__changeTextColor("green"))
        textColorGreenButton.grid(row=0, column=15, padx=5, pady=5)


    def __createStatusBar(self):
        self.__statusBar = Label(self.__root, text="Words: 0", anchor=E, bg="white", relief=SUNKEN)
        self.__statusBar.grid(row=3, column=0, columnspan=3, sticky=W + E)

    def __updateWordCount(self, event=None):
        text = self.__thisTextArea.get(1.0, END)
        words = len(text.split())
        self.__statusBar.config(text=f"Words: {words}")

    def __disableAction(self, event=None):
        showinfo("Action Blocked", "Copy and Paste are disabled.")
        return "break"

    def __adjustSize(self, event=None):
        pass  # Adjust layout as needed here

    def __quitApplication(self):
        if self.idle_timer is not None:
            self.__root.after_cancel(self.idle_timer)  # Cancel the idle timer thread
        self.__root.after_cancel(self.check_pipe_id)
        self.running = False
        self.__root.destroy()

    def __showAbout(self):
        showinfo("About Notepad", "Enhanced Notepad with advanced features.")

    def __newFile(self):
        self.__thisTextArea.delete(1.0, END)

    def __openFile(self):
        try:
            file = askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
            if file:
                with open(file, "r") as f:
                    self.__thisTextArea.delete(1.0, END)
                    self.__thisTextArea.insert(1.0, f.read())
        except Exception as e:
            showerror("Error", f"Failed to open file: {e}")

    def __saveFile(self):
        try:
            file = asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
            if file:
                self.__saveAsPDF(file)
        except Exception as e:
            showerror("Error", f"Failed to save file: {e}")

    def __saveAsPDF(self, file):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)  # Default font for PDF
        lines = self.__thisTextArea.get(1.0, END).splitlines()
        for line in lines:
            pdf.cell(200, 10, txt=line, ln=True)
        pdf.output(file)

    def __makeBold(self):
        self.__applyTag("bold", {"font": ("Calibri", 12, "bold")})

    def __makeItalic(self):
        self.__applyTag("italic", {"font": ("Calibri", 12, "italic")})

    def __makeUnderline(self):
        self.__applyTag("underline", {"font": ("Calibri", 12, "underline")})
    
    def __makeBoldUnderline(self):
        self.__applyTag("bold_underline", {"font": ("Calibri", 12, "bold", "underline")})

    def __makeItalicUnderline(self):
        self.__applyTag("italic_underline", {"font": ("Calibri", 12, "italic", "underline")})

    def __makeBoldItalic(self):
        self.__applyTag("bold_italic", {"font": ("Calibri", 12, "bold", "italic")})

    def __makeBoldItalicUnderline(self):
        self.__applyTag("bold_italic_underline", {"font": ("Calibri", 12, "bold", "italic", "underline")})

    def __applyTag(self, tag, config):
        self.__thisTextArea.tag_config(tag, **config)  # Apply font and other settings
        try:
            current_tags = self.__thisTextArea.tag_names("sel.first")
            if tag in current_tags:
                self.__thisTextArea.tag_remove(tag, "sel.first", "sel.last")
            else:
                self.__thisTextArea.tag_add(tag, "sel.first", "sel.last")
        except:
            pass

    def __centerText(self):
    # Apply a tag to center-align text
        self.__thisTextArea.tag_configure("center", justify='center')
        self.__thisTextArea.tag_add("center", "sel.first", "sel.last")

    def __highlightText(self, color):
        try:
            # Ensure text is selected
            if not self.__thisTextArea.tag_ranges("sel"):
                raise ValueError("No text selected for highlighting.")
            
            # Add the highlight tag
            self.__thisTextArea.tag_add(f"highlight_{color}", "sel.first", "sel.last")
            self.__thisTextArea.tag_configure(f"highlight_{color}", background=color)
        except ValueError as e:
            print(e)  # Optionally show this message to the user

    def __changeTextColor(self, color):
        try:
            # Ensure text is selected
            if not self.__thisTextArea.tag_ranges("sel"):
                raise ValueError("No text selected for color change.")
            
            # Add the text color tag
            self.__thisTextArea.tag_add(f"text_color_{color}", "sel.first", "sel.last")
            self.__thisTextArea.tag_configure(f"text_color_{color}", foreground=color)
        except ValueError as e:
            print(e)  # Optionally show this message to the user