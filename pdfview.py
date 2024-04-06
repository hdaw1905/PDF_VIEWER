from tkinter import *
from tkinter import ttk, filedialog
import os
from miner import PDFMiner

class PDFViewer:
    def __init__(self, master):
        # Initialize variables
        self.path = None
        self.fileisopen = False
        self.author = None
        self.name = None
        self.current_page = 0
        self.numPages = None

        # Create main window
        self.master = master
        self.master.title('PDF Viewer')
        self.master.geometry('580x520+440+180')
        self.master.resizable(width=0, height=0)
        self.master.iconbitmap('pdf_file_icon.ico')

        # Create menu
        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)
        self.filemenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Open File", command=self.open_file)
        self.filemenu.add_command(label="Exit", command=self.master.destroy)

        # Create frames
        self.top_frame = ttk.Frame(self.master, width=580, height=460)
        self.top_frame.grid(row=0, column=0)
        self.top_frame.grid_propagate(False)

        self.bottom_frame = ttk.Frame(self.master, width=580, height=50)
        self.bottom_frame.grid(row=1, column=0)
        self.bottom_frame.grid_propagate(False)

        # Create scrollbars and canvas
        self.scrolly = Scrollbar(self.top_frame, orient=VERTICAL)
        self.scrolly.grid(row=0, column=1, sticky=(N, S))
        self.scrollx = Scrollbar(self.top_frame, orient=HORIZONTAL)
        self.scrollx.grid(row=1, column=0, sticky=(W, E))

        self.output = Canvas(self.top_frame, bg='#ECE8F3', width=560, height=435)
        self.output.configure(yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set)
        self.output.grid(row=0, column=0)
        self.scrolly.config(command=self.output.yview)
        self.scrollx.config(command=self.output.xview)

        # Load button icons
        self.uparrow_icon = PhotoImage(file='uparrow.png').subsample(3, 3)
        self.downarrow_icon = PhotoImage(file='downarrow.png').subsample(3, 3)

        # Create buttons and page label
        self.upbutton = ttk.Button(self.bottom_frame, image=self.uparrow_icon, command=self.previous_page)
        self.upbutton.grid(row=0, column=1, padx=(270, 5), pady=8)
        self.downbutton = ttk.Button(self.bottom_frame, image=self.downarrow_icon, command=self.next_page)
        self.downbutton.grid(row=0, column=3, pady=8)
        self.page_label = ttk.Label(self.bottom_frame, text='page')
        self.page_label.grid(row=0, column=4, padx=5)

    def open_file(self):
        # Open file dialog and select PDF file
        filepath = filedialog.askopenfilename(title='Select a PDF file', initialdir=os.getcwd(), filetypes=(('PDF', '*.pdf'),))
        if filepath:
            # If file selected, set path and extract file name
            self.path = filepath
            self.name = os.path.basename(self.path)[:-4]
            # Initialize PDFMiner with selected file
            self.miner = PDFMiner(self.path)
            # Get metadata and number of pages
            data, self.numPages = self.miner.get_metadata()
            self.current_page = 0
            if self.numPages:
                # If pages found, update variables and display first page
                self.author = data.get('author')
                self.fileisopen = True
                self.display_page()
                self.master.title(self.name)

    def display_page(self):
        if 0 <= self.current_page < self.numPages:
            # Display current page
            self.img_file = self.miner.get_page(self.current_page)
            self.output.delete("all")
            self.output.create_image(0, 0, anchor='nw', image=self.img_file)
            self.page_label.config(text=f'{self.current_page + 1} of {self.numPages}')
            self.output.config(scrollregion=self.output.bbox("all"))

    def next_page(self):
        if self.fileisopen and self.current_page < self.numPages - 1:
            # Display next page if available
            self.current_page += 1
            self.display_page()

    def previous_page(self):
        if self.fileisopen and self.current_page > 0:
            # Display previous page if available
            self.current_page -= 1
            self.display_page()

root = Tk()
app = PDFViewer(root)
root.mainloop()
