from pypdf import PdfReader


def extract_text_from_pdf(uploaded_file):
    pdf = PdfReader(uploaded_file)
    text = ""

    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def chunk_text(text, chunk_size=1000):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
    return chunks