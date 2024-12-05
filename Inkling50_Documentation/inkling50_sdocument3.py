import sys
import os
from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter import simpledialog
from fpdf import FPDF  # For saving files as PDF

class Notepad:
    __root = Tk()
    __thisWidth = 600
    __thisHeight = 400
    __thisTextArea = Text(__root, wrap=WORD, undo=True)
    __thisMenuBar = Menu(__root)
    __thisFileMenu = Menu(__thisMenuBar, tearoff=0)
    __thisEditMenu = Menu(__thisMenuBar, tearoff=0)
    __thisFormatMenu = Menu(__thisMenuBar, tearoff=0)
    __thisHelpMenu = Menu(__thisMenuBar, tearoff=0)
    __thisScrollBar = Scrollbar(__thisTextArea)
    __file = None

    def __init__(self):
        self.__root.title("Untitled - Notepad")
        screenWidth = self.__root.winfo_screenwidth()
        screenHeight = self.__root.winfo_screenheight()
        left = (screenWidth / 2) - (self.__thisWidth / 2)
        top = (screenHeight / 2) - (self.__thisHeight / 2)
        self.__root.geometry(f'{self.__thisWidth}x{self.__thisHeight}+{int(left)}+{int(top)}')
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)
        self.__thisTextArea.grid(sticky=N + E + S + W)
        self.__thisScrollBar.pack(side=RIGHT, fill=Y)
        self.__thisScrollBar.config(command=self.__thisTextArea.yview)
        self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)
        self.__createMenuBar()
        self.__createStatusBar()
        self.__root.config(menu=self.__thisMenuBar)

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
        self.__statusBar.pack(side=BOTTOM, fill=X)
        self.__thisTextArea.bind("<KeyRelease>", self.__updateWordCount)

    def __updateWordCount(self, event=None):
        text = self.__thisTextArea.get(1.0, END)
        words = len(text.split())
        self.__statusBar.config(text=f"Words: {words}")

    def __quitApplication(self):
        self.__root.destroy()

    def __showAbout(self):
        showinfo("Notepad", "Enhanced Notepad with Advanced Features")

    def __openFile(self):
        self.__file = askopenfilename(filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if self.__file:
            self.__root.title(os.path.basename(self.__file) + " - Notepad")
            self.__thisTextArea.delete(1.0, END)
            with open(self.__file, "r") as file:
                self.__thisTextArea.insert(1.0, file.read())

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

    def __saveAsPDF(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        lines = self.__thisTextArea.get(1.0, END).splitlines()
        for line in lines:
            pdf.cell(200, 10, txt=line, ln=True)
        pdf.output(self.__file)

    def __makeBold(self):
        self.__applyTag("bold", {"font": ("Arial", 12, "bold")})

    def __makeItalic(self):
        self.__applyTag("italic", {"font": ("Arial", 12, "italic")})

    def __makeUnderline(self):
        self.__applyTag("underline", {"font": ("Arial", 12, "underline")})

    def __changeFontSize(self):
        size = simpledialog.askinteger("Font Size", "Enter font size:", initialvalue=12)
        if size:
            self.__applyTag("font_size", {"font": ("Arial", size)})

    def __applyTag(self, tag, options):
        try:
            self.__thisTextArea.tag_configure(tag, **options)
            current_tags = self.__thisTextArea.tag_names(SEL_FIRST)
            if tag in current_tags:
                self.__thisTextArea.tag_remove(tag, SEL_FIRST, SEL_LAST)
            else:
                self.__thisTextArea.tag_add(tag, SEL_FIRST, SEL_LAST)
        except TclError:
            showerror("Error", "Please select text to apply formatting.")

    def run(self):
        self.__root.mainloop()

# Run the application
notepad = Notepad()
notepad.run()
