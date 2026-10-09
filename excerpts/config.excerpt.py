# PRIVACY NOTICE: Partial code excerpt only. The full implementation is omitted for privacy.
# Source: config.py | Selected source lines: 46-85
# This incomplete excerpt is for portfolio review; it is not a runnable application.

def setup_logging() -> logging.Logger:
    """Turns on logging. Safe to call more than once — it only sets up once."""
    global _logging_configured
    root_logger = logging.getLogger()
    if _logging_configured:
        return root_logger

    os.makedirs(LOG_DIR, exist_ok=True)
    level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    root_logger.setLevel(level)

    log_format = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    file_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, "pipeline.log"),
        maxBytes=50 * 1024 * 1024,
        backupCount=10,
        encoding="utf-8",
    )
    file_handler.setFormatter(log_format)

    screen_handler = logging.StreamHandler()
    screen_handler.setFormatter(log_format)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(screen_handler)
    _logging_configured = True
    return root_logger


setup_logging()
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────
# STEP 2: DEVICE DETECTION (CPU or GPU) — unchanged.
# This is about OCR hardware, completely separate from which LLM
# provider you use for text extraction.
# ─────────────────────────────────────────────────────────

# END OF EXCERPT. The remaining code is private.
