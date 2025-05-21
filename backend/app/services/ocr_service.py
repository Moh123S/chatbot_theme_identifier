import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from unstructured.partition.auto import partition
import os

def extract_text(file_path):
    try:
        if file_path.lower().endswith('.pdf'):
            # Use PyMuPDF for PDF text extraction
            doc = fitz.open(file_path)
            text = ""
            for page_num in range(doc.page_count):
                page = doc[page_num]
                page_text = page.get_text("text")
                text += f"\n[Page {page_num + 1}]\n{page_text}"
            doc.close()
            if not text.strip():  # Fallback to OCR if no text extracted
                images = convert_from_path(file_path)
                text = ""
                for i, image in enumerate(images):
                    text += f"\n[Page {i + 1}]\n{pytesseract.image_to_string(image)}"
            return text
        elif file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Use unstructured for image processing
            elements = partition(filename=file_path)
            text = "\n".join([str(el) for el in elements])
            if not text.strip():  # Fallback to pytesseract
                image = Image.open(file_path)
                text = pytesseract.image_to_string(image)
            return text
        else:
            raise ValueError("Unsupported file format")
    except Exception as e:
        raise Exception(f"Error extracting text from {file_path}: {str(e)}")