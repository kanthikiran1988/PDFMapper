import os
import logging
from transformers import MarianMTModel, MarianTokenizer

logger = logging.getLogger(__name__)


def translate_offline(
        text: str,
        source_lang: str,
        target_lang: str,
        model_name_pattern: str,
        local_model_dir: str = None
) -> str:
    """
    Translate text offline using a MarianMT model. If the model isn't found locally,
    it will be downloaded once (assuming internet availability), and all subsequent runs
    can use the local model without downloading again.

    :param text: Text to translate.
    :param source_lang: Source language code.
    :param target_lang: Target language code.
    :param model_name_pattern: Pattern to form the model name (e.g., 'Helsinki-NLP/opus-mt-{source}-{target}').
    :param local_model_dir: Optional path to a local directory containing the model files.
    :return: Translated text.
    """
    model_name = model_name_pattern.format(source=source_lang, target=target_lang)

    # If local directory is specified and exists, load from there
    if local_model_dir and os.path.exists(local_model_dir):
        logger.info(f"Loading model from local directory: {local_model_dir}")
        tokenizer = MarianTokenizer.from_pretrained(local_model_dir)
        model = MarianMTModel.from_pretrained(local_model_dir)
    else:
        # If local directory isn't provided or doesn't exist, download the model once
        # You can choose a dedicated cache directory to store models.
        cache_dir = "./models"
        model_cache_path = os.path.join(cache_dir, model_name.replace("/", "__"))

        if not os.path.exists(model_cache_path):
            logger.info(f"Model {model_name} not found locally. Downloading...")
            tokenizer = MarianTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
            model = MarianMTModel.from_pretrained(model_name, cache_dir=cache_dir)
            logger.info(f"Model downloaded and cached at {model_cache_path}")
        else:
            logger.info(f"Loading cached model from {model_cache_path}")
            tokenizer = MarianTokenizer.from_pretrained(model_cache_path)
            model = MarianMTModel.from_pretrained(model_cache_path)

    # Perform the translation
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    translated_tokens = model.generate(**inputs)
    translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
    return translated_text
