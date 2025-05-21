import PyPDF2
import pytesseract
from PIL import Image
import os

def extract_text(file_path):
    try:
        if file_path.lower().endswith('.pdf'):
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num, page in enumerate(reader.pages):
                    page_text = page.extract_text() or ""
                    text += f"\n[Page {page_num + 1}]\n{page_text}"
                return text
        elif file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            return text
        else:
            raise ValueError("Unsupported file format")
    except Exception as e:
        raise Exception(f"Error extracting text from {file_path}: {str(e)}")