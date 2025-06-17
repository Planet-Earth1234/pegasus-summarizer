
import fitz  # PyMuPDF

def extract_pdf(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return ' '.join(text.split())  # Removes extra whitespace

# Example usage
pdf_path = r"C:\Users\Yash\Downloads\My_Resume.pdf"  # Replace with your actual PDF file path
extracted_text = extract_pdf(pdf_path)
print(extracted_text)