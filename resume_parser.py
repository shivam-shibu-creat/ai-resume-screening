import PyPDF2

def extract_text_from_pdf(path):
    with open(path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""

        for page in reader.pages:
            text = text + page.extract_text()

    return text.lower()

