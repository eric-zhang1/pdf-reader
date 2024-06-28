import streamlit as st

import platform
from tempfile import TemporaryDirectory
from pathlib import Path

import pytesseract
from pdf2image import convert_from_path
from pypdf import PdfMerger

image_file_list = []

# TODO: Replace PdfMerger with PDFReader + PDFWriter. Might need to look into pypdf

if platform.system() == "Windows":
	# We may need to do some additional downloading and setup...
	# Windows needs a PyTesseract Download
	# https://github.com/UB-Mannheim/tesseract/wiki/Downloading-Tesseract-OCR-Engine

	pytesseract.pytesseract.tesseract_cmd = (
		r"C:\Program Files\Tesseract-OCR\tesseract.exe"
	)

	# Windows also needs poppler_exe
	path_to_poppler_exe = Path(r"C:\.....")

def main():
    st.title("Pdf Reader")
    st.write("""
	# Pdf-Reader
    Created by Eric L. Zhang
	""")
    st.sidebar.header("File input")
    uploaded_file = st.sidebar.file_uploader("Choose a pdf file to ocr")
    if uploaded_file is not None:
        with TemporaryDirectory() as tempdir:
            # Convert all pages to images
            if platform.system() == "Windows":
                pdf_pages = convert_from_path(
					uploaded_file, 500, poppler_path=path_to_poppler_exe
				)
            else:
                pdf_pages = convert_from_path(uploaded_file, 500)
            
			# Create pdf merger
            merger = PdfMerger()
            
			# Loop through each page of the pdf
            for page_enumeration, page in enumerate(pdf_pages, start=1):
                filenameJPG = f"{tempdir}\page_{page_enumeration:03}.jpg"
                filenamePDF = f"{tempdir}\page_{page_enumeration:03}.pdf"
                
				# Convert each page to an image
                page.save(filenameJPG, "JPEG")
                
            	# Convert each image to searchable pdf
                current_page = pytesseract.image_to_pdf_or_hocr(filenameJPG, extension="pdf")
                with open(filenamePDF, "w+b") as f:
                    f.write(current_page)
                
				# Append current page to the end of pdf
                merger.append(filenamePDF)
            merger.write(f"{uploaded_file.name}.pdf")
        # Output converted pdf file
    



if __name__ == "__main__":
    main()