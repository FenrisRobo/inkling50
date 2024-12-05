import sys
import os
import ttkbootstrap
from tkinter import *
from ttkbootstrap import Window
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter import simpledialog  # Import simpledialog for font size input
from fpdf import FPDF  # For saving files as PDF

class Notepad:
    __root = Tk()
    __thisWidth = 600
    __thisHeight = 400
    __thisTextArea = Text(__root, wrap=WORD, undo=True, font=("Calibri", 12))  # Default font
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
        
        # Configure grid layout
        self.__root.grid_rowconfigure(0, weight=1)  # Text area
        self.__root.grid_rowconfigure(1, weight=0)  # Status bar
        self.__root.grid_columnconfigure(0, weight=1)
        
        # Add the text area
        self.__thisTextArea.grid(row=0, column=0, sticky=N + E + S + W)
        self.__thisScrollBar.pack(side=RIGHT, fill=Y)
        self.__thisScrollBar.config(command=self.__thisTextArea.yview)
        self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)
        
        self.__createMenuBar()
        self.__createStatusBar()
        self.__root.config(menu=self.__thisMenuBar)

        # Root window with ttkbootstrap
        self.__root = Window(themename="journal")
        self.__root.title("Notepad")
        
        # Toolbar
        toolbar = Frame(self.__root, height=30, bg="lightgray")
        toolbar.grid(row=0, column=0, columnspan=3, sticky=W+E)

        # Toolbar Buttons
        bold_btn = Button(toolbar, text="B", command=self.__makeBold, font=("Calibri", 12, "bold"), width=3)
        bold_btn.pack(side=LEFT, padx=5, pady=5)

        italic_btn = Button(toolbar, text="I", command=self.__makeItalic, font=("Calibri", 12, "italic"), width=3)
        italic_btn.pack(side=LEFT, padx=5, pady=5)

        underline_btn = Button(toolbar, text="U", command=self.__makeUnderline, font=("Calibri", 12, "underline"), width=3)
        underline_btn.pack(side=LEFT, padx=5, pady=5)

        theme_btn = Button(toolbar, text="Toggle Theme", command=self.__toggleDarkMode)
        theme_btn.pack(side=RIGHT, padx=5, pady=5)

        # Toolbar Button Shortcut
        self.__root.bind("<Control-b>", lambda event: self.__makeBold())
        self.__root.bind("<Control-i>", lambda event: self.__makeItalic())
        self.__root.bind("<Control-u>", lambda event: self.__makeUnderline())

        # Margins
        margin_left = Frame(self.__root, width=50, bg="lightgray")
        margin_left.grid(row=1, column=0, sticky=NS)

        text_frame = Frame(self.__root)
        text_frame.grid(row=1, column=1, sticky=NSEW)

        self.__thisTextArea = Text(text_frame, wrap=WORD, undo=True, font=("Calibri", 12))
        self.__thisTextArea.pack(fill=BOTH, expand=True)

        margin_right = Frame(self.__root, width=50, bg="lightgray")
        margin_right.grid(row=1, column=2, sticky=NS)

        # Word Count
        self.__statusBar = Label(self.__root, text="Words: 0", anchor=E, bg="white", relief=SUNKEN)
        self.__statusBar.grid(row=3, column=0, columnspan=3, sticky=W+E)

        # Bind events
        self.__thisTextArea.bind("<KeyRelease>", self.__updateWordCount)

        self.__root.mainloop()


    def __createMenuBar(self):
        self.__thisFileMenu.add_command(label="New", command=self.__newFile)
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

    def __updateWordCount(self, event=None):
        text = self.__thisTextArea.get(1.0, END)
        words = len(text.split())
        self.__statusBar.config(text=f"Words: {words}")

    def __toggleDarkMode(self):
        current_theme = self.__root.style.theme_use()
        new_theme = "darkly" if current_theme == "journal" else "journal"
        self.__root.style.theme_use(new_theme)
    
    def __quitApplication(self):
        self.__root.destroy()

    def __showAbout(self):
        showinfo("Notepad", "Enhanced Notepad with Advanced Features")

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
        pdf.set_font("Calibri", size=12)
        lines = self.__thisTextArea.get(1.0, END).splitlines()
        for line in lines:
            pdf.cell(200, 10, txt=line, ln=True)
        pdf.output(self.__file)

    def __makeBold(self):
        self.__applyTag("bold", {"font": ("Calibri", 12, "bold")})

    def __makeItalic(self):
        self.__applyTag("italic", {"font": ("Calibri", 12, "italic")})

    def __makeUnderline(self):
        self.__applyTag("underline", {"font": ("Calibri", 12, "underline")})

    def __changeFontSize(self):
        size = simpledialog.askinteger("Font Size", "Enter font size:", initialvalue=12)
        if size:
            self.__applyTag("font_size", {"font": ("Calibri", size)})

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