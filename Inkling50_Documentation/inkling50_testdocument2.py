import time
import sys
import os
import ttkbootstrap
import tkinter.font as tkFont
from tkinter import *
from ttkbootstrap import Window, Style
from ttkbootstrap.constants import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter import simpledialog  # Import simpledialog for font size input
from fpdf import FPDF  # For saving files as PDF
from threading import Timer

class Notepad:
    __root = Window(themename="journal")
    __thisTextArea = Text(__root, wrap=WORD, undo=True, font=("Calibri", 12))  # Default font
    __thisMenuBar = Menu(__root)
    __thisFileMenu = Menu(__thisMenuBar, tearoff=0)
    __thisEditMenu = Menu(__thisMenuBar, tearoff=0)
    __thisFormatMenu = Menu(__thisMenuBar, tearoff=0)
    __thisHelpMenu = Menu(__thisMenuBar, tearoff=0)

    def __init__(self):
        # Root window with ttkbootstrap
        self.__root.title("Notepad")
        self.__root.geometry("800x600")  # Set a default size

        # Configure root grid layout
        self.__root.grid_rowconfigure(1, weight=1)  # Text area should expand
        self.__root.grid_columnconfigure(1, weight=1)  # Center frame (Text) should expand

        # Create the menu bar
        self.__createMenuBar()
        self.__createStatusBar()
        self.__root.config(menu=self.__thisMenuBar)

        # Adjust window size
        self.__root.bind("<Configure>", self.__adjustSize)

        # Add font tags
        self.style_tags = {"bold", "italic", "underline", "bold italic", "bold italic underline", "bold italic underline", "italic underline", "bold underline"}

        # Margins
        margin_left = Frame(self.__root, width=50, bg="lightgray")
        margin_left.grid(row=1, column=0, sticky=NS)

        text_frame = Frame(self.__root)
        text_frame.grid(row=1, column=1, sticky=NSEW)

        self.__thisTextArea = Text(text_frame, wrap=WORD, undo=True, font=("Calibri", 12))
        self.__thisTextArea.pack(fill=BOTH, expand=True)

        # Toolbar
        toolbar = Frame(self.__root, height=30, bg="lightgray")
        toolbar.grid(row=0, column=0, columnspan=3, sticky=W + E)

        # Toolbar Buttons
        bold_btn = Button(toolbar, text="B", command=self.__makeBold, font=("Calibri", 12, "bold"), width=3)
        bold_btn.pack(side=LEFT, padx=5, pady=5)

        italic_btn = Button(toolbar, text="I", command=self.__makeItalic, font=("Calibri", 12, "italic"), width=3)
        italic_btn.pack(side=LEFT, padx=5, pady=5)

        underline_btn = Button(toolbar, text="U", command=self.__makeUnderline, font=("Calibri", 12, "underline"), width=3)
        underline_btn.pack(side=LEFT, padx=5, pady=5)

        theme_btn = Button(toolbar, text="Toggle Theme", command=self.__toggleDarkMode)
        theme_btn.pack(side=RIGHT, padx=5, pady=5)

        # Bind events
        self.__root.bind("<Key>", self.__onKeyPress)
        self.__root.bind("<Control-b>", lambda event: self.__makeBold())
        self.__root.bind("<Control-i>", lambda event: self.__makeItalic())
        self.__root.bind("<Control-u>", lambda event: self.__makeUnderline())
        self.__root.bind("<Control-c>", lambda event: self.__thisTextArea.event_generate("<<Copy>>"))
        self.__root.bind("<Control-v>", lambda event: self.__thisTextArea.event_generate("<<Paste>>"))

        # Timer for idle time tracking
        self.idle_time_limit = 5  # seconds
        self.timer = None  # Timer will be reset on every key press

        # Start the main loop
        self.__root.mainloop()

    def __onKeyPress(self, event):
        """Triggered on every key press to reset the timer"""
        self.__resetIdleTimer()

    def __resetIdleTimer(self):
        """Reset the idle timer each time a key is pressed"""
        if self.timer:
            self.timer.cancel()  # Cancel the previous timer if it's still running
        
        # Set a new timer that triggers when the idle time limit is reached
        self.timer = Timer(self.idle_time_limit, self.__onIdleTimeout)
        self.timer.start()

    def __onIdleTimeout(self):
        """This method is called when the user is idle for the defined time"""
        print("User is idle for too long!")

    def __createMenuBar(self):
        self.__thisFileMenu.add_command(label="New", command=self.__newFile)
        self.__thisFileMenu.add_command(label="Open", command=self.__openFile)
        self.__thisFileMenu.add_command(label="Save", command=self.__saveFile)
        self.__thisFileMenu.add_separator()
        self.__thisFileMenu.add_command(label="Exit", command=self.__quitApplication)
        self.__thisMenuBar.add_cascade(label="File", menu=self.__thisFileMenu)
        self.__thisEditMenu.add_command(label="Cut", command=lambda: self.__thisTextArea.event_generate("<<Cut>>"))
        self.__thisEditMenu.add_command(label="Copy", command=lambda: self.__thisTextArea.event_generate("<<Copy>>"))
        self.__thisEditMenu.add_command(label="Paste", command=lambda: self.__thisTextArea.event_generate("<<Paste>>"))
        self.__thisMenuBar.add_cascade(label="Edit", menu=self.__thisEditMenu)
        self.__thisFormatMenu.add_command(label="Bold", command=self.__makeBold)
        self.__thisFormatMenu.add_command(label="Italic", command=self.__makeItalic)
        self.__thisFormatMenu.add_command(label="Underline", command=self.__makeUnderline)
        self.__thisFormatMenu.add_command(label="Change Font Size", command=self.__changeFontSize)
        self.__thisMenuBar.add_cascade(label="Format", menu=self.__thisFormatMenu)
        self.__thisHelpMenu.add_command(label="About Notepad", command=self.__showAbout)
        self.__thisMenuBar.add_cascade(label="Help", menu=self.__thisHelpMenu)

    def __createStatusBar(self):
        self.__statusBar = Label(self.__root, text="Words: 0", anchor=W)
        self.__statusBar.grid(row=1, column=0, sticky=W+E, columnspan=2)
        self.__thisTextArea.bind("<KeyRelease>", self.__updateWordCount)

    def __newFile(self):
        self.__root.title("Untitled - Notepad")
        self.__file = None
        self.__thisTextArea.delete(1.0, END)

    def __saveFile(self):
        if not self.__file:
            self.__file = asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
            if self.__file:
                self.__saveAsPDF()
        else:
            self.__saveAsPDF()

    def __openFile(self):
        self.__file = askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if self.__file:
            self.__root.title(os.path.basename(self.__file) + " - Notepad")
            self.__thisTextArea.delete(1.0, END)
        with open(self.__file, "r") as file:
            self.__thisTextArea.insert(1.0, file.read())

    def __updateWordCount(self, event=None):
        text = self.__thisTextArea.get(1.0, END)
        words = len(text.split())
        self.__statusBar.config(text=f"Words: {words}")

    def __changeFontSize(self):
        size = simpledialog.askinteger("Font Size", "Enter font size:", initialvalue=11)
        if size:
            self.__applyTag("font_size", {"font": ("Calibri", size)})

    def __toggleDarkMode(self):
        current_theme = self.__root.style.theme_use()
        new_theme = "darkly" if current_theme == "journal" else "journal"
        self.__root.style.theme_use(new_theme)

    def __adjustSize(self, event=None):
        self.__thisTextArea.config(width=self.__root.winfo_width(), height=self.__root.winfo_height())

    def __quitApplication(self):
        self.__root.destroy()

    def __showAbout(self):
        showinfo("Notepad", "Enhanced Notepad with Advanced Features")

    def __makeBold(self):
        self.__applyTag("bold", {"font": ("Calibri", 12, "bold")})

    def __makeItalic(self):
        self.__applyTag("italic", {"font": ("Calibri", 12, "italic")})

    def __makeUnderline(self):
        self.__applyTag("underline", {"font": ("Calibri", 12, "underline")})

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
    
    def run(self):
        self.__root.mainloop()

# Run the application
notepad = Notepad()
notepad.run()

