import logging
import os
import sys
import yaml
from typing import Dict
from extract import extract_text_from_pdf
from label import label_phrases
from detect_lang import detect_language
from translate import translate_offline
from pdf_gen import create_pdf

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


def load_config(config_path: str = "config/config.yaml") -> Dict:
    """
    Load configuration from a YAML file.
    """
    try:
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        logger.error(f"Failed to load configuration from {config_path}: {e}", exc_info=True)
        sys.exit(1)


def process_pdf(
        input_pdf_path: str,
        output_pdf_path: str,
        labels: Dict[str, str],
        target_lang: str,
        model_name_pattern: str
) -> None:
    """
    Orchestrate the PDF processing:
    - Extract text
    - Detect language
    - Label phrases
    - Translate text
    - Create a new PDF

    :param input_pdf_path: Path to the input PDF file.
    :param output_pdf_path: Path to the output PDF file.
    :param labels: Dictionary of phrases and their corresponding labels.
    :param target_lang: Target language code for translation.
    :param model_name_pattern: Pattern for the MarianMT model name.
    """
    if not os.path.exists(input_pdf_path):
        logger.error(f"Input PDF not found at {input_pdf_path}")
        sys.exit(1)

    logger.info("Starting PDF processing workflow...")

    try:
        # Extract text from the PDF
        logger.info("Extracting text from PDF...")
        extracted_text = extract_text_from_pdf(input_pdf_path)

        # Detect source language
        logger.info("Detecting source language...")
        source_lang = detect_language(extracted_text)

        # Label phrases
        logger.info("Labeling specific phrases...")
        labeled_text = label_phrases(extracted_text, labels)

        # Translate text
        logger.info(f"Translating text from {source_lang} to {target_lang}...")
        translated_text = translate_offline(labeled_text, source_lang, target_lang, model_name_pattern)

        # Create the new PDF
        logger.info("Creating new PDF with translated and labeled text...")
        create_pdf(
            text=translated_text,
            output_path=output_pdf_path,
            input_path=input_pdf_path,
            labels=labels
        )

        logger.info(f"PDF processing complete! Output saved to {output_pdf_path}")

    except Exception as e:
        logger.error("An error occurred during the PDF processing workflow.", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    # Load configuration
    config = load_config()

    input_pdf_path = config.get("input_pdf_path", "input.pdf")
    output_pdf_path = config.get("output_pdf_path", "output.pdf")
    target_lang = config.get("target_lang", "en")
    labels = config.get("labels", {})
    model_name_pattern = config.get("model_name_pattern", "Helsinki-NLP/opus-mt-{source}-{target}")

    process_pdf(input_pdf_path, output_pdf_path, labels, target_lang, model_name_pattern)
