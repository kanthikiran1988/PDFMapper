import logging
from transformers import MarianMTModel, MarianTokenizer
from typing import Optional

logger = logging.getLogger(__name__)

def translate_offline(
    text: str,
    source_lang: str,
    target_lang: str,
    model_name_pattern: str
) -> str:
    """
    Translate text offline using a MarianMT model.
    If source and target languages are the same, returns the original text.

    :param text: Text to translate.
    :param source_lang: Source language code.
    :param target_lang: Target language code.
    :param model_name_pattern: Pattern to form the model name.
    :return: Translated text.
    """
    # If source and target languages are the same, return original text
    if source_lang == target_lang:
        logger.info("Source and target languages are the same. Skipping translation.")
        return text

    model_name = model_name_pattern.format(source=source_lang, target=target_lang)
    logger.info(f"Loading model {model_name} for offline translation.")

    try:
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
    except Exception as e:
        logger.error(f"Failed to load translation model {model_name}: {e}", exc_info=True)
        raise

    try:
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        translated_tokens = model.generate(**inputs)
        translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
        return translated_text
    except Exception as e:
        logger.error(f"Translation failed: {e}", exc_info=True)
        raise
