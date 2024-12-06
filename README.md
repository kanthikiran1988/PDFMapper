# PDFMapper

PDFMapper is a Python tool that processes PDF documents by identifying specific text patterns, adding labels, and maintaining the original PDF formatting.

## Features

- Preserves original PDF formatting and layout
- Adds labels to specified text patterns
- Supports multiple languages
- Configurable label mappings
- Language detection and translation support

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/PDFMapper.git
cd PDFMapper
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Configure the tool by editing `config/config.yaml`:

```yaml
input_pdf_path: "input.pdf"
output_pdf_path: "output.pdf"
target_lang: "en"
labels:
  "invoice no": "Invoice Number"
  "purchase order no": "PO Number"
```

## Usage

1. Place your input PDF in the project directory (or update the path in config.yaml)
2. Run the script:

```bash
python src/main.py
```

## Project Structure

```
PDFMapper/
├── src/
│   ├── main.py          # Main application entry point
│   ├── pdf_gen.py       # PDF generation and labeling
│   ├── extract.py       # PDF text extraction
│   ├── label.py         # Text labeling functionality
│   ├── detect_lang.py   # Language detection
│   └── translate.py     # Translation functionality
├── config/
│   └── config.yaml      # Configuration file
└── requirements.txt     # Project dependencies
```

## Dependencies

- PyMuPDF (fitz)
- transformers
- torch
- fpdf2
- PyYAML
- langdetect
- sentencepiece
- sacremoses

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- PyMuPDF for PDF processing
- Hugging Face Transformers for translation capabilities