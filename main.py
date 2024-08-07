import sys
from pdf2png import ConvertPDF2Image
from ocr import *
import os
from png2word import AddTextBoxToWordDocument
from wordmerger import mergewords
import shutil

def prepare(pdf_path, result_dir):
    current_directory = os.getcwd()
    
    new_directory = f"{os.path.splitext(os.path.basename(pdf_path))[0]}_helper"

    new_directory_path = os.path.join(current_directory, new_directory)
    if not os.path.exists(new_directory_path):
        os.makedirs(new_directory_path)
        
    new_directory_result = f"{os.path.splitext(os.path.basename(pdf_path))[0]}_result"

    result_dir_path = os.path.join(result_dir, new_directory_result)
    if not os.path.exists(result_dir_path):
        os.makedirs(result_dir_path)
    
    original_name, extension = os.path.splitext(os.path.basename(pdf_path))
    new_pdf_name = f"{original_name}_converted{extension}"
    new_pdf_path = os.path.join(result_dir_path, new_pdf_name)
    
    shutil.copy(pdf_path, new_pdf_path)
    
    return new_pdf_name, new_directory
    
    
if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python script_name.py /path/to/your/pdf/file.pdf [result_dir]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    
    result_dir = sys.argv[2] if len(sys.argv) == 3 else os.getcwd()

    if not os.path.isfile(pdf_path):
        print(f"Error: The file {pdf_path} does not exist.")
        sys.exit(1)

    if not os.path.isdir(result_dir):
        print(f"Error: The directory {result_dir} does not exist.")
        sys.exit(1)
        
    
    conv_pdf_name, helper_dir = prepare(pdf_path, result_dir)
    
    ConvertPDF2Image(pdf_path)

    helper_dir_path = os.path.join(os.getcwd(), helper_dir)

    for page_image in os.listdir('pages'):
        image_path = f"pages\\{page_image}"
        page_name = os.path.splitext(page_image)[0]
        
        ocr_results, img_width, img_height = runOCR(image_path)
        
        AddTextBoxToWordDocument(outputs=ocr_results,
                                 page_width=8.5 * 72, page_height=11 * 72,  
                                 image_width=img_width, image_height=img_height, 
                                 dir_path=helper_dir_path, file_name=page_name)
        
        os.remove(f"pages\\{page_image}")
        
    
    mergewords(helper_dir_path="bovitett_absztrakt_helper", 
               result_dir_path="bovitett_absztrakt_result", 
               conv_pdf_name="bovitett_absztrakt_converted.pdf", 
               result_docx_name="bovitett_absztrakt_converted.docx")
    
    if(os.path.exists(helper_dir)):
        shutil.rmtree(helper_dir)
    
        
        
