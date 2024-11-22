import sys
import tkinter # standard Python interface to the Tk GUI toolkit
import os # Python library to create methods to interact with OSs
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *

class Notepad:

    __root = Tk() # set _root as the window of the GUI application

    # default window width and height

    __thisWidth = 300 # default window width for notepad
    __thisHeight = 300 # default window length for notepad
    __thisTextArea = Text(__root) # this is the area to input text
    __thisMenuBar = Menu(__root) # this is the area to hold menu options
    __thisFileMenu = Menu(__thisMenuBar, tearoff=0) # creates a file option
    __thisEditMenu = Menu(__thisMenuBar, tearoff=0) # creates an edit option
    __thisHelpMenu = Menu(__thisMenuBar, tearoff=0) # creates a help option

    # to add scrollbar

    __thisScrollBar = Scrollbar(__thisTextArea) # this is the area to hold a scrollbar
    __file = None # currently there is no file

    def __init__(self, **kwargs):

        # __init__ refers to constructor method of a class to give values to the class

        # self refers to creation of a class to give access to variables and methods

        # **kwargs refers to "keyword arguments" to allow method to accept additional named arguments when class is instantiated
        
        # Set icon of the Notepad
        try:
            self.__root.wm_iconbitmap("Notepad.ico") 
            # a tkinter method to use to set the window manager's icon for the application
        except:
            pass
            # otherwise, pass through the try exception

        # Set window size (said above default was 300 x 300)

        try:
            self.__thisWidth = kwargs['width']
        except KeyError:
            pass

        try:
            self.__thisHeight = kwargs['height']
        except KeyError:
            pass

        # Set the window text

        self.__root.title("Untitled - Notepad")

        # Center the window

        screenWidth = self.__root.winfo_screenwidth()
        screenHeight = self.__root.winfo_screenheight()

        # For left-alligning
        left = (screenWidth / 2) - (self.__thisWidth / 2)

        # For right-alligning
        top = (screenHeight / 2) - (self.__thisHeight / 2)

        # For top and bottom (%d is a placeholder)
        self.__root.geometry('%dx%d+%d+%d' % (self.__thisWidth,self.__thisHeight, left, top))

        # To make the text area auto-resizable
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)

        # Add controls (widget)
        self.__thisTextArea.grid(sticky = N + E + S + W)

        # To open new file
        self.__thisFileMenu.add_command(label="New", command=self.__newFile)
        
        # To open an already existing file
        self.__thisFileMenu.add_command(label="Open", command=self.__openFile)

        # To save current file
        self.__thisFileMenu.add_command(label="Save", command=self.__saveFile)

        # To create a line in the dialog
        self.__thisFileMenu.add_separator()
        self.__thisFileMenu.add_command(label="Exit", command=self.__quitApplication)
        self.__thisMenuBar.add_cascade(label="File", menu=self.__thisFileMenu)

        # To give a feature of cut
        self.__thisEditMenu.add_command(label="Cut", command=self.__cut)

        # To give a feature to copy
        self.__thisEditMenu.add_command(label="Copy",command=self.__copy)

        # To give a feature of paste
        self.__thisEditMenu.add_command(label="Paste",command=self.__paste)
        
        # To give a feature of editing
        self.__thisMenuBar.add_cascade(label="Edit", menu=self.__thisEditMenu)

        # To create a feature of description of the notepad
        self.__thisHelpMenu.add_command(label="About Notepad", command=self.__showAbout)
        self.__thisMenuBar.add_cascade(label="Help", menu=self.__thisHelpMenu)

        self.__root.config(menu=self.__thisMenuBar)

        self.__thisScrollBar.pack(side=RIGHT, fill=Y)

        # Scrollbar will adjust automatically accordng to the content
        self.__thisScrollBar.config(command=self.__thisTextArea.yview)
        self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.config)

    def __quitApplication(self):
        self.__root.destroy()
        # exit ()

    def __showAbout(self):
        showinfo("Notepad", "Mrinal Verma")
    
    def __openFile(self):
        self.__file = askopenfilename(defaultextension=".txt",
            filetypes=[("All Files", "*.*"),("Text Documents", "*.txt")])

        if self.__file == "":
            self.__file = None
        
        else:
        
            try:
            
                self.__root.title(os.path.basename(self.__file) + " - Notepad")
                self.__thisTextArea.delete(1.0, END)

                with open(self.__file, "r") as file:
                
                    self.__thisTextArea.insert(1.0, file.read())
                
            except Exception as e:
            
                showerror("Error", f"Could not open file: {e}")
            
    def __newFile(self):
        self.__root.title("Untitled - Notepad")
        self.__file = None
        self.__thisTextArea.delete(1.0,END)

    def __saveFile(self):
        if self.__file == None:
            # Save as new file
            self.__file = asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt", filetypes=[("All Files","*.*"),("Text Document","*.txt")])

            if self.__file == "":
                self.__file = None

            else:

            # Try to save the file
                file = open(self.__file,"w")
                file.write(self.__thisTextArea.get(1.0,END))
                file.close()

            # Change the window title
                self.__root.title(os.path.basename(self.__file) + " - Notepad")
        else:
            file = open(self.__file,"w")
            file.write(self.__thisTextArea.get(1.0,END))
            file.close()

    def __cut(self):
        self.__thisTextArea.event_generate("<<Cut>>")
    
    def __copy(self):
        self.__thisTextArea.event_generate("<<Copy>>")

    def __paste(self):
        self.__thisTextArea.event_generate("<<Paste>>")
    
    def run(self):

         # Run main application

        self.__root.mainloop()

# Run main application

notepad = Notepad(width=600, height=400)
notepad.run()