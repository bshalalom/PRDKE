import io
from pydantic import BaseModel, Field
from pypdf import PdfReader
from typing import List

# Ein Datenmodell für die Rückgabe, falls die aufrufende Funktion dies erwartet.
class PDFText(BaseModel):
    text: str = Field(..., description="Der extrahierte Text aus dem PDF.")
    page_count: int = Field(..., description="Die Anzahl der Seiten im PDF.")

def extract_text_from_pdf(file_stream: io.BytesIO) -> List[str]:
    """
    Extrahiert Text von jeder Seite eines PDF-Dateistroms.

    Args:
        file_stream: Ein BytesIO-Objekt, das die PDF-Datei enthält.

    Returns:
        Eine Liste von Strings, wobei jeder String den Text einer Seite darstellt.
    """
    try:
        reader = PdfReader(file_stream)
        page_texts = [page.extract_text() for page in reader.pages]
        print(f"Text aus {len(reader.pages)} Seiten extrahiert.")
        return page_texts
    except Exception as e:
        print(f"Fehler beim Extrahieren von Text aus PDF: {e}")
        return []