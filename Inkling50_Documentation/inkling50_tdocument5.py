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
    __root = Window(themename="journal")
    __thisTextArea = Text(__root, wrap=WORD, undo=True, font=("Calibri", 12))  # Default font
    __thisMenuBar = Menu(__root)
    __thisFileMenu = Menu(__thisMenuBar, tearoff=0)
    __thisEditMenu = Menu(__thisMenuBar, tearoff=0)
    __thisFormatMenu = Menu(__thisMenuBar, tearoff=0)
    __thisHelpMenu = Menu(__thisMenuBar, tearoff=0)
    __thisScrollBar = Scrollbar(__thisTextArea)
    __file = None

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
        self.__root.bind("<Control-c>", lambda event: self.__thisTextArea.event_generate("<<Copy>>"))
        self.__root.bind("<Control-v>", lambda event: self.__thisTextArea.event_generate("<<Paste>>"))

        # Margins
        margin_left = Frame(self.__root, width=50, bg="lightgray")
        margin_left.grid(row=1, column=0, sticky=NS)

        text_frame = Frame(self.__root)
        text_frame.grid(row=1, column=1, sticky=NSEW)

        self.__thisTextArea = Text(text_frame, wrap=WORD, undo=True, font=("Calibri", 12))
        self.__thisTextArea.pack(fill=BOTH, expand=True)

        # Set the scrollbar
        self.__thisScrollBar = Scrollbar(self.__thisTextArea)
        self.__thisScrollBar.pack(side=RIGHT, fill=Y)
        self.__thisScrollBar.config(command=self.__thisTextArea.yview)
        self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)

        margin_right = Frame(self.__root, width=50, bg="lightgray")
        margin_right.grid(row=1, column=2, sticky=NS)

        # Word Count
        self.__statusBar = Label(self.__root, text="Words: 0", anchor=E, bg="white", relief=SUNKEN)
        self.__statusBar.grid(row=3, column=0, columnspan=3, sticky=W+E)

        # Configure resizing weights
        self.__root.grid_rowconfigure(1, weight=1)  # Allow text frame to expand vertically
        self.__root.grid_columnconfigure(1, weight=1)  # Allow text frame to expand horizontally

        # Bind events
        self.__thisTextArea.bind("<KeyRelease>", self.__updateWordCount)

        self.__root.mainloop()


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

    def __updateWordCount(self, event=None):
        text = self.__thisTextArea.get(1.0, END)
        words = len(text.split())
        self.__statusBar.config(text=f"Words: {words}")

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


    def __saveAsPDF(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Calibri", size=12)
        lines = self.__thisTextArea.get(1.0, END).splitlines()
        for line in lines:
            pdf.cell(200, 10, txt=line, ln=True)
        pdf.output(self.__file)

    def __changeFontSize(self):
        size = simpledialog.askinteger("Font Size", "Enter font size:", initialvalue=12)
        if size:
            self.__applyTag("font_size", {"font": ("Calibri", size)})

    def __applyTag(self, tag, options):
        try:
            # Get the current selection (if any)
            current_tags = self.__thisTextArea.tag_names(SEL_FIRST)
            
            # Determine if any combination of bold, italic, or underline is already applied
            current_font = self.__thisTextArea.tag_cget(tag, "font") if tag in current_tags else ("Calibri", 12)
            
            # Apply the font styles based on the current state
            if tag == "bold":
                current_font = ("Calibri", 12, "bold")
            elif tag == "italic":
                current_font = ("Calibri", 12, "italic")
            elif tag == "underline":
                current_font = ("Calibri", 12, "underline")
            
            # Configure the tag with the updated font settings
            self.__thisTextArea.tag_configure(tag, font=current_font)
            
            # Add the tag to the selected text
            if tag not in current_tags:
                self.__thisTextArea.tag_add(tag, SEL_FIRST, SEL_LAST)
        except TclError:
            showerror("Error", "Please select text to apply formatting.")


    def __makeBold(self):
        self.__applyTag("bold", {"font": ("Calibri", 12, "bold")})

    def __makeItalic(self):
        self.__applyTag("italic", {"font": ("Calibri", 12, "italic")})

    def __makeUnderline(self):
        self.__applyTag("underline", {"font": ("Calibri", 12, "underline")})

    def run(self):
        self.__root.mainloop()

# Run the application
notepad = Notepad()
notepad.run()
