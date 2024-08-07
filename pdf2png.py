import fitz
import os

def ConvertPDF2Image(filepath):
    pdf_document = fitz.open(filepath)
    os.makedirs('./pages', exist_ok=True)
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap()
        image_path = f'./pages/page_{page_number + 1}.png'
        pix.save(image_path)
