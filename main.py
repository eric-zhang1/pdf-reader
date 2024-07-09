import streamlit as st

import platform
from tempfile import TemporaryDirectory
from pathlib import Path
import os
import fitz

import pytesseract
from pdf2image import convert_from_path
from pypdf import PdfWriter

image_file_list = []

if platform.system() == "Windows":
	# We may need to do some additional downloading and setup...
	# Windows needs a PyTesseract Download
	# https://github.com/UB-Mannheim/tesseract/wiki/Downloading-Tesseract-OCR-Engine

	pytesseract.pytesseract.tesseract_cmd = (
		r"C:\Program Files\Tesseract-OCR\tesseract.exe"
	)

	# Windows also needs poppler_exe
	path_to_poppler_exe = Path(r"C:\Program Files\poppler-24.02.0\Library\bin")

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
            # copy the file to a temp folder
            file_path = os.path.join(tempdir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            # Convert all pages to images
            if platform.system() == "Windows":
                pdf_pages = convert_from_path(
					file_path, 500, poppler_path=path_to_poppler_exe
				)
            else:
                pdf_pages = convert_from_path(file_path, 500)
            
			# Create pdf writer
            merger = PdfWriter()
            
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
            # Write the pdf to the temporary directory for download purposes
            merger.write(f"{tempdir}\{uploaded_file.name}.pdf")
            merger.close()
            # Create download button for file.
            with open(f"{tempdir}\{uploaded_file.name}.pdf", "rb") as file:
                st.sidebar.download_button(
                    label=f"Download {uploaded_file.name}",
                    data=file,
                    file_name=f"{uploaded_file.name}.pdf",
                    mime="application/pdf"
                )
        
    


if __name__ == "__main__":
    main()