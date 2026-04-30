import fitz  # PyMuPDF
import docx
import json

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_pdf(file_path)
    elif file_path.endswith(".docx"):
        return extract_docx(file_path)
    elif file_path.endswith(".txt"):
        return open(file_path, "r").read()
    elif file_path.endswith(".json"):
        with open(file_path, "r") as f:
            data = json.load(f)
            return json.dumps(data)
    else:
        return ""

def extract_pdf(path):
    text = ""
    doc = fitz.open(path)
    for page in doc:
        text += page.get_text()
    return text

def extract_docx(path):
    doc = docx.Document(path)
    return "\n".join([p.text for p in doc.paragraphs])
