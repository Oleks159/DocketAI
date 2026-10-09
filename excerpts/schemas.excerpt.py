# PRIVACY NOTICE: Partial code excerpt only. The full implementation is omitted for privacy.
# Source: schemas.py | Selected source lines: 36-75
# This incomplete excerpt is for portfolio review; it is not a runnable application.

class SourceRef:
    filename: str
    page: int
    sheet: Optional[str] = None
    slide: Optional[str] = None
    bbox: Optional[List[float]] = None


@dataclass
class NormalizedBlock:
    block_id: str
    document_id: str
    type: str          # "text", "heading", "table", "image"
    text: str = ""
    table_data: Optional[Dict] = None
    source_ref: Optional[SourceRef] = None
    confidence: float = 1.0
    language: str = "en"
    metadata: Dict = field(default_factory=dict)


# ─────────────────────────────────────────────────────────
# NEW — Pydantic models matching the ACTUAL invoice output shape that
# flows through llm_extractor.py / rule_engine.py / run.py.
#
# Every field is written as "Optional" (allowed to be empty/null) because
# the whole point of this pipeline is that some fields are genuinely
# missing on some invoices — that's expected, not an error. What we DO
# want to catch is the WRONG TYPE of data (e.g. text where a number
# should be), which usually means something went wrong upstream.
# ─────────────────────────────────────────────────────────

class InvoiceItem(BaseModel):
    """One row from the invoice's item table (e.g. one product line)."""

    item_name: Optional[str] = None
    item_code: Optional[str] = None
    hsn_sac: Optional[str] = None
    quantity: Optional[float] = None
    rate: Optional[float] = None
# END OF EXCERPT. The remaining code is private.
