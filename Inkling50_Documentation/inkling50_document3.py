import tkinter as tk
from tkinter import *
from tkinter.messagebox import showinfo, showerror
from tkinter.filedialog import askopenfilename, asksaveasfilename


class Notepad:

    def __init__(self, **kwargs):
        self.__root = Tk()

        # Window settings
        self.__thisWidth = kwargs.get('width', 600)
        self.__thisHeight = kwargs.get('height', 400)
        self.__file = None

        # Set window title
        self.__root.title("Untitled - Notepad")

        # Center window on screen
        screen_width = self.__root.winfo_screenwidth()
        screen_height = self.__root.winfo_screenheight()
        left = (screen_width // 2) - (self.__thisWidth // 2)
        top = (screen_height // 2) - (self.__thisHeight // 2)
        self.__root.geometry(f"{self.__thisWidth}x{self.__thisHeight}+{left}+{top}")

        # Create widgets
        self.__thisTextArea = Text(self.__root, undo=True)
        self.__thisScrollBar = Scrollbar(self.__thisTextArea)
        self.__thisMenuBar = Menu(self.__root)

        # Configure text area and scrollbar
        self.__thisTextArea.grid(row=0, column=0, sticky=N + E + S + W)
        self.__thisScrollBar.config(command=self.__thisTextArea.yview)
        self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set)
        self.__thisScrollBar.pack(side=RIGHT, fill=Y)

        # Configure menu bar
        self.__fileMenu = Menu(self.__thisMenuBar, tearoff=0)
        self.__fileMenu.add_command(label="New", command=self.__newFile)
        self.__fileMenu.add_command(label="Open", command=self.__openFile)
        self.__fileMenu.add_command(label="Save", command=self.__saveFile)
        self.__fileMenu.add_separator()
        self.__fileMenu.add_command(label="Exit", command=self.__quitApplication)
        self.__thisMenuBar.add_cascade(label="File", menu=self.__fileMenu)

        self.__editMenu = Menu(self.__thisMenuBar, tearoff=0)
        self.__editMenu.add_command(label="Cut", command=self.__cut)
        self.__editMenu.add_command(label="Copy", command=self.__copy)
        self.__editMenu.add_command(label="Paste", command=self.__paste)
        self.__thisMenuBar.add_cascade(label="Edit", menu=self.__editMenu)

        self.__helpMenu = Menu(self.__thisMenuBar, tearoff=0)
        self.__helpMenu.add_command(label="About Notepad", command=self.__showAbout)
        self.__thisMenuBar.add_cascade(label="Help", menu=self.__helpMenu)

        # Attach menu bar to the root
        self.__root.config(menu=self.__thisMenuBar)

    def __newFile(self):
        self.__root.title("Untitled - Notepad")
        self.__file = None
        self.__thisTextArea.delete(1.0, END)

    def __openFile(self):
        self.__file = askopenfilename(defaultextension=".txt",
                                      filetypes=[("All Files", "*.*"),
                                                 ("Text Documents", "*.txt")])

        if self.__file:
            self.__root.title(f"{self.__file} - Notepad")
            try:
                with open(self.__file, "r") as file:
                    content = file.read()
                self.__thisTextArea.delete(1.0, END)
                self.__thisTextArea.insert(1.0, content)
            except Exception as e:
                showerror("Error", f"Cannot open file: {e}")

    def __saveFile(self):
        if self.__file is None:
            self.__file = asksaveasfilename(initialfile="Untitled.txt",
                                            defaultextension=".txt",
                                            filetypes=[("All Files", "*.*"),
                                                       ("Text Documents", "*.txt")])
            if not self.__file:
                return

        try:
            with open(self.__file, "w") as file:
                file.write(self.__thisTextArea.get(1.0, END))
            self.__root.title(f"{self.__file} - Notepad")
        except Exception as e:
            showerror("Error", f"Cannot save file: {e}")

    def __quitApplication(self):
        self.__root.destroy()

    def __showAbout(self):
        showinfo("About Notepad", "Simple Notepad App\nCreated for Demo Purposes")

    def __cut(self):
        self.__thisTextArea.event_generate("<<Cut>>")

    def __copy(self):
        self.__thisTextArea.event_generate("<<Copy>>")

    def __paste(self):
        self.__thisTextArea.event_generate("<<Paste>>")

    def run(self):
        self.__root.mainloop()


# Run the application
notepad = Notepad(width=600, height=400)
notepad.run()
