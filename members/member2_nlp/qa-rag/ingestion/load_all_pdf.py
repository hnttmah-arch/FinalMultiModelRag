from pathlib import Path
from pypdf import PdfReader

DATA_DIR = "data"

pdfs = Path(DATA_DIR).glob("*.pdf")

for pdf in pdfs:
    try:
        reader = PdfReader(str(pdf))

        print("\n================")
        print(pdf.name)
        print("Pages:", len(reader.pages))

        text = reader.pages[0].extract_text()

        print(text[:500])

    except Exception as e:
        print(pdf.name, e)