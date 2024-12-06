import logging
import fitz

logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from the given PDF file.

    :param pdf_path: Path to the input PDF file.
    :return: Extracted text as a string.
    """
    try:
        with fitz.open(pdf_path) as pdf_document:
            text = ""
            for page_num in range(pdf_document.page_count):
                page = pdf_document.load_page(page_num)
                text += page.get_text()
            return text
    except Exception as e:
        logger.error(f"Failed to extract text from PDF {pdf_path}: {e}", exc_info=True)
        raise
