import logging
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

class TextbookCalligraphy:
    def __init__(self, output_path: str = "documentation.pdf"):
        self.output_path = output_path
        self.c = canvas.Canvas(self.output_path, pagesize=letter)
        logging.info("TextbookCalligraphy initialized with output path: %s", output_path)

    def add_title(self, title: str, x: int = 100, y: int = 750, font_size: int = 24):
        logging.info("Adding title to documentation: %s", title)
        self.c.setFont("Times-Bold", font_size)
        self.c.drawString(x, y, title)

    def add_paragraph(self, text: str, x: int = 100, y: int = 700, font_size: int = 12):
        logging.info("Adding paragraph to documentation.")
        self.c.setFont("Times-Roman", font_size)
        text_object = self.c.beginText(x, y)
        for line in text.split('\n'):
            text_object.textLine(line)
        self.c.drawText(text_object)

    def save_document(self):
        logging.info("Saving documentation.")
        self.c.save()
        logging.info("Documentation saved as '%s'.", self.output_path)
