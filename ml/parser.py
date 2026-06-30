import fitz  # PyMuPDF
from docx import Document


def extract_text_from_pdf(file):
    """
    Extract text from a PDF file.

    Parameters:
        file: Uploaded PDF file from Streamlit

    Returns:
        str: Extracted text
    """
    text = ""

    pdf = fitz.open(stream=file.read(), filetype="pdf")

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text.strip()


def extract_text_from_docx(file):
    """
    Extract text from a DOCX file.

    Parameters:
        file: Uploaded DOCX file from Streamlit

    Returns:
        str: Extracted text
    """
    doc = Document(file)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text.strip()


def extract_text(file):
    """
    Detect file type and extract text.

    Supported:
    - PDF
    - DOCX

    Parameters:
        file: Uploaded file from Streamlit

    Returns:
        str: Extracted text
    """

    if file is None:
        return ""

    file_name = file.name.lower()

    if file_name.endswith(".pdf"):
        return extract_text_from_pdf(file)

    elif file_name.endswith(".docx"):
        return extract_text_from_docx(file)

    else:
        raise ValueError("Unsupported file format. Please upload PDF or DOCX.")