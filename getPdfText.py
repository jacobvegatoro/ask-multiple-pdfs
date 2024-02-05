
""" getPdfText es un módulo de Python que recibe un conjunto de archivos PDF """
""" obtenidos desde Streamlit y extrae el texto """

from PyPDF2 import PdfReader

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text
