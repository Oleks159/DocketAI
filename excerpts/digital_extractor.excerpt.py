# PRIVACY NOTICE: Partial code excerpt only. The full implementation is omitted for privacy.
# Source: digital_extractor.py | Selected source lines: 42-81
# This incomplete excerpt is for portfolio review; it is not a runnable application.

def clean_span_text(text: str) -> str:
    """Remove block characters and collapse whitespace."""
    if not text:
        return ""
    cleaned = BLOCK_CHARS_RE.sub(' ', text)
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()


# --- Lazy page-image rendering for the Gemma vision fallback ---------------
def render_page_images(pdf_path: str, dpi: int = None) -> List[Image.Image]:
    """
    Turns each page of a digital PDF into a picture (image). Only called
    on-demand from llm_extractor.py when a field is still missing after
    the Gemini text pass — most digital PDFs never need this, since the
    text pass usually finds everything.

    dpi (sharpness) defaults to config.OCR_DPI if not given, so digital
    and scanned PDFs use a consistent, device-appropriate resolution
    (lower on CPU to save memory/time, higher on GPU).
    """
    dpi = dpi or config.OCR_DPI
    doc = fitz.open(pdf_path)
    images = []
    try:
        zoom = dpi / 72
        mat = fitz.Matrix(zoom, zoom)
        for page in doc:
            pix = page.get_pixmap(matrix=mat)
            img_bytes = pix.tobytes("png")
            images.append(Image.open(io.BytesIO(img_bytes)))
    finally:
        doc.close()
    logger.info(f"Rendered {len(images)} page image(s) from {pdf_path} at {dpi} DPI "
                f"for the Gemma vision fallback")
    return images


# --- PHASE 1: table detection (math-based, no keywords) --------------------
def _is_valid_data_table(headers, rows):
# END OF EXCERPT. The remaining code is private.
