import fitz  # PyMuPDF
import logging
from typing import Dict
import re

logger = logging.getLogger(__name__)

def create_pdf(text: str, output_path: str, input_path: str, labels: Dict[str, str]) -> None:
    """
    Create a PDF file maintaining the original format while adding labels.
    """
    try:
        # Open the original PDF
        doc = fitz.open(input_path)
        
        # Create a new PDF for output
        out_doc = fitz.open()
        
        labels_applied = False
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Get full page text for better context
            page_text = page.get_text("text")
            logger.info(f"Page {page_num + 1} text: {page_text[:200]}...")  # Log first 200 chars
            
            # Insert the page into the output document
            out_page = out_doc.new_page(width=page.rect.width, height=page.rect.height)
            out_page.show_pdf_page(out_page.rect, doc, page_num)
            
            # Get text blocks with positions
            blocks = page.get_text("dict")["blocks"]
            
            # Create a shape object for adding labels
            shape = out_page.new_shape()
            
            # Process each text block
            for block in blocks:
                if "lines" not in block:
                    continue
                    
                for line in block["lines"]:
                    line_text = ""
                    line_bbox = None
                    
                    # Combine spans in the line
                    for span in line["spans"]:
                        line_text += span["text"] + " "
                        if line_bbox is None:
                            line_bbox = fitz.Rect(span["bbox"])
                        else:
                            line_bbox |= fitz.Rect(span["bbox"])
                    
                    line_text = line_text.strip().lower()
                    
                    # Check for matches
                    for key, label in labels.items():
                        search_pattern = re.compile(re.escape(key.lower()))
                        if search_pattern.search(line_text):
                            logger.info(f"Found match: '{key}' in '{line_text}'")
                            
                            # Add background rectangle
                            label_rect = fitz.Rect(
                                line_bbox.x0,
                                line_bbox.y0 - 15,
                                line_bbox.x0 + 100,
                                line_bbox.y0 - 2
                            )
                            shape.draw_rect(label_rect)
                            shape.finish(color=(0.9, 0.9, 0.9), fill=(0.9, 0.9, 0.9))
                            
                            # Add label
                            label_point = fitz.Point(line_bbox.x0, line_bbox.y0 - 5)
                            shape.insert_text(
                                label_point,
                                f"{label}",
                                fontsize=8,
                                color=(0.8, 0, 0)
                            )
                            
                            labels_applied = True
            
            # Commit the shapes to the page
            shape.commit()
        
        # Save the modified PDF
        out_doc.save(output_path)
        out_doc.close()
        doc.close()
        
        if labels_applied:
            logger.info("Successfully applied labels to PDF")
        else:
            logger.warning("No labels were applied. Text content:")
            logger.warning(f"Searching for labels: {list(labels.keys())}")
        
    except Exception as e:
        logger.error(f"Failed to create PDF at {output_path}: {e}")
        raise