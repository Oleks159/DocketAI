# PRIVACY NOTICE: Partial code excerpt only. The full implementation is omitted for privacy.
# Source: scanned_extractor.py | Selected source lines: 57-96
# This incomplete excerpt is for portfolio review; it is not a runnable application.

def clean_text(text: str) -> str:
    if not text:
        return ""
    cleaned = TAG_RE.sub("", text)
    cleaned = BLOCK_CHARS_RE.sub(" ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


# --- Global model cache (load once per process, reuse for every PDF) ------
# IMPORTANT: on CPU, keep OCR_WORKERS=1 in your .env — loading this model
# more than once at the same time just fights over the same CPU cores and
# uses more RAM, with no speed benefit. On GPU, a couple of workers can
# make sense if you have enough VRAM (GPU memory) free.
_predictors = None


def _get_predictors():
    """
    Loads the Surya OCR models one time, onto the correct device (CPU or
    GPU), and reuses them for every PDF after that. Loading a model is
    slow, so we only want to do it once, not per file.
    """
    global _predictors
    if _predictors is None:
        logger.info(f"Loading Surya OCR models onto device: {config.DEVICE} "
                    f"(this happens once per run)")
        foundation_predictor = FoundationPredictor(device=config.DEVICE)
        recognition_predictor = RecognitionPredictor(foundation_predictor)
        detection_predictor = DetectionPredictor(device=config.DEVICE)
        _predictors = (recognition_predictor, detection_predictor)
        logger.info("Surya OCR models loaded successfully.")
    return _predictors


def pdf_to_images(pdf_path: str, dpi: int = None) -> List[Image.Image]:
    """
    Turns each page of the PDF into a picture (image), so OCR can "read"
    it like a photo. Higher dpi = sharper image = better accuracy, but
    slower and uses more memory. Defaults to config.OCR_DPI if not given
# END OF EXCERPT. The remaining code is private.
