import os
from docx2pdf import convert
import PyPDF2
from pdf2docx import Converter
from docx import Document

def doc2pdfconverter(dir_path):
    for doc_file in os.listdir(dir_path):
        pdf_name = os.path.splitext(doc_file)[0]
        convert(f"{dir_path}\\{doc_file}", f"{dir_path}\\{pdf_name}.pdf")
        os.remove(f"{dir_path}\\{doc_file}")
    

def mergePDFs(helper_dir_path, result_dir_path, conv_pdf_name):
    pdf_files = []
    
    for pdf in os.listdir(helper_dir_path):
        pdf_files.append(pdf)
    
    pdf_merger = PyPDF2.PdfMerger()
    
    for pdf in pdf_files:
        pdf_merger.append(f"{helper_dir_path}\\{pdf}")
        
    pdf_merger.write(f"{result_dir_path}\\{conv_pdf_name}")
    pdf_merger.close()
        
def pdf2wordconverter(dir_path, result_pdf_name, result_docx_name):
    pdf = f"{dir_path}\\{result_pdf_name}"
    docx = f"{dir_path}\\{result_docx_name}"
    
    cv = Converter(pdf)
    cv.convert(docx, start=0, end=None)
    cv.close()
    
def mergewords(helper_dir_path, result_dir_path, conv_pdf_name, result_docx_name):
    doc2pdfconverter(dir_path=helper_dir_path)
    mergePDFs(helper_dir_path, result_dir_path, conv_pdf_name)
    pdf2wordconverter(dir_path=result_dir_path, result_pdf_name=conv_pdf_name, result_docx_name=result_docx_name)
    
    