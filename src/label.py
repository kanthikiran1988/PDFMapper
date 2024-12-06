import logging
from typing import Dict

logger = logging.getLogger(__name__)

def label_phrases(text: str, labels: Dict[str, str]) -> str:
    """
    Label specific phrases in the text by wrapping them with tags.

    :param text: Original text.
    :param labels: Dictionary mapping phrases to label tags.
    :return: Text with labeled phrases.
    """
    for phrase, label in labels.items():
        if phrase in text:
            logger.debug(f"Labeling phrase '{phrase}' with label '{label}'")
            text = text.replace(phrase, f"<{label}>{phrase}</{label}>")
    return text
