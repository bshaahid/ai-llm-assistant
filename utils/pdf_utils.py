from pypdf import PdfReader


def extract_text_from_pdf(uploaded_file):
    pdf = PdfReader(uploaded_file)
    text = ""

    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def chunk_text(text, chunk_size=1000, overlap=200):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks