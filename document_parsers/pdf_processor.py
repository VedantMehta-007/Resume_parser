import pdfplumber

def parse_pdf(filepath):
    full_text = []
    try:
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                full_text.append(page.extract_text())
        return "\n".join(full_text)
    except Exception as e:
        raise RuntimeError(f"PDF parsing failed: {str(e)}")