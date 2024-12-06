import logging
from langdetect import detect, DetectorFactory

logger = logging.getLogger(__name__)

# Set seed for deterministic language detection
DetectorFactory.seed = 0

def detect_language(text: str) -> str:
    """
    Detect the language of the given text.

    :param text: Text to detect language from.
    :return: Detected language code (ISO 639-1).
    """
    try:
        language_code = detect(text)
        logger.info(f"Detected language: {language_code}")
        return language_code
    except Exception as e:
        logger.error("Language detection failed.", exc_info=True)
        raise
