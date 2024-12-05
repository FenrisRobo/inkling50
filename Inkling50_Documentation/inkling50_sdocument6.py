import sys
import os
import ttkbootstrap
from ttkbootstrap import Window, Style
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter import simpledialog
from fpdf import FPDF

class Notepad:
    __thisWidth = 600
    __thisHeight = 400
    __file = None

    def __init__(self):
        # Initialize the ttkbootstrap window
        self.__root = Window(themename="journal")
        self.__root.title("Untitled - Notepad")

        # Set window geometry
        screenWidth = self.__root.winfo_screenwidth()
        screenHeight = self.__root.winfo_screenheight()
        left = (screenWidth / 2) - (self.__thisWidth / 2)
        top = (screenHeight / 2) - (self.__thisHeight / 2)
        self.__root.geometry(f'{self.__thisWidth}x{self.__thisHeight}+{int(left)}+{int(top)}')

        # Configure grid layout
        self.__root.grid_rowconfigure(0, weight=1)  # Text area
        self.__root.grid_rowconfigure(1, weight=0)  # Status bar
        self.__root.grid_columnconfigure(0, weight=1)

        # Text area
        self.__thisTextArea = Text(self.__root, wrap=WORD, undo=True, font=("Calibri", 12))
        self.__thisTextArea.grid(row=0, column=0, sticky=NSEW)

        # Scrollbar
        self.__thisScrollBar = Scrollbar(self.__thisTextArea)
        self.__thisScrollBar.pack(side=RIGHT, fill=Y)
        self.__thisScrollBar.config(command=self.__thisTextArea.yview)
        self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)

        # Create menu bar
        self.__createMenuBar()

        # Create status bar
        self.__statusBar = Label(self.__root, text="Words: 0", anchor=E, bg="white", relief=SUNKEN)
        self.__statusBar.grid(row=1, column=0, sticky=W+E)

        # Bind events
        self.__thisTextArea.bind("<KeyRelease>", self.__updateWordCount)
        self.__root.bind("<Control-c>", lambda event: self.__thisTextArea.event_generate("<<Copy>>"))
        self.__root.bind("<Control-v>", lambda event: self.__thisTextArea.event_generate("<<Paste>>"))

        self.__root.mainloop()

    def __createMenuBar(self):
        menuBar = Menu(self.__root)

        # File menu
        fileMenu = Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="New", command=self.__newFile)
        fileMenu.add_command(label="Open", command=self.__openFile)
        fileMenu.add_command(label="Save", command=self.__saveFile)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.__quitApplication)
        menuBar.add_cascade(label="File", menu=fileMenu)

        # Edit menu
        editMenu = Menu(menuBar, tearoff=0)
        editMenu.add_command(label="Cut", command=lambda: self.__thisTextArea.event_generate("<<Cut>>"))
        editMenu.add_command(label="Copy", command=lambda: self.__thisTextArea.event_generate("<<Copy>>"))
        editMenu.add_command(label="Paste", command=lambda: self.__thisTextArea.event_generate("<<Paste>>"))
        menuBar.add_cascade(label="Edit", menu=editMenu)

        # Help menu
        helpMenu = Menu(menuBar, tearoff=0)
        helpMenu.add_command(label="About", command=self.__showAbout)
        menuBar.add_cascade(label="Help", menu=helpMenu)

        self.__root.config(menu=menuBar)

    def __newFile(self):
        self.__root.title("Untitled - Notepad")
        self.__file = None
        self.__thisTextArea.delete(1.0, END)

    def __openFile(self):
        self.__file = askopenfilename(filetypes=[("Text Documents", "*.txt")])
        if self.__file:
            self.__root.title(f"{self.__file} - Notepad")
            with open(self.__file, "r") as f:
                self.__thisTextArea.delete(1.0, END)
                self.__thisTextArea.insert(1.0, f.read())

    def __saveFile(self):
        if not self.__file:
            self.__file = asksaveasfilename(defaultextension=".txt", filetypes=[("Text Documents", "*.txt")])
        if self.__file:
            with open(self.__file, "w") as f:
                f.write(self.__thisTextArea.get(1.0, END))
            self.__root.title(f"{self.__file} - Notepad")

    def __quitApplication(self):
        self.__root.destroy()

    def __showAbout(self):
        showinfo("Notepad", "Enhanced Notepad with ttkbootstrap UI")

    def __updateWordCount(self, event=None):
        text = self.__thisTextArea.get(1.0, END).strip()
        words = len(text.split())
        self.__statusBar.config(text=f"Words: {words}")

# Run the application
notepad = Notepad()
