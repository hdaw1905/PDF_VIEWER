import math
import fitz
from tkinter import PhotoImage

class PDFMiner:
    def __init__(self, filepath):
        self.filepath = filepath
        self.pdf = fitz.open(self.filepath)
        self.first_page = self.pdf.load_page(0)
        self.width, self.height = self.first_page.rect.width, self.first_page.rect.height
        self.zoom = self.calculate_zoom()

    def calculate_zoom(self):
        zoom_dict = {800: 0.8, 700: 0.6, 600: 1.0, 500: 1.0}
        width = int(math.floor(self.width / 100.0) * 100)
        return zoom_dict.get(width, 1.0)

    def get_metadata(self):
        metadata = self.pdf.metadata
        num_pages = self.pdf.page_count
        return metadata, num_pages
    
    def get_page(self, page_num):
        page = self.pdf.load_page(page_num)
        mat = fitz.Matrix(self.zoom, self.zoom)
        pix = page.get_pixmap(matrix=mat) if self.zoom else page.get_pixmap()
        imgdata = pix.tobytes("ppm") if pix.alpha else pix.tobytes()
        return PhotoImage(data=imgdata)
    
    def get_text(self, page_num):
        page = self.pdf.load_page(page_num)
        return page.get_text('text')
