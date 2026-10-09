# PRIVACY NOTICE: Partial code excerpt only. The full implementation is omitted for privacy.
# Source: rule_engine.py | Selected source lines: 30-69
# This incomplete excerpt is for portfolio review; it is not a runnable application.

class RuleEngine:
    """Plain-rule checks for invoice fields. No AI involved in this file."""

    # A "labeled" HSN mention near the header, e.g. "HSN Code: 8483" or
    # "HSN: 848360". Must have the word HSN/SAC nearby — this is what makes
    # it safe (unlike the old rule, which grabbed ANY stray number).
    _HSN_LABEL_RE = re.compile(
        r'\b(?:HSN|SAC)(?:\s*(?:CODE|NO\.?))?\s*[:\-]?\s*(\d{4,8})\b',
        re.IGNORECASE,
    )

    @staticmethod
    def validate_hsn(value) -> bool:
        """
        HSN/SAC code must be pure digits, and exactly 4, 6, or 8 digits long.
        Example: "8483" is valid (4 digits). "84831" is NOT valid (5 digits).
        """
        if value is None:
            return False
        cleaned = re.sub(r'\s+', '', str(value))
        return cleaned.isdigit() and len(cleaned) in (4, 6, 8)

    @staticmethod
    def validate_item_code(value) -> bool:
        """
        Item Code must be exactly 7 digits, and must start with 1, 2, 3, or 4.
        Example: "1234567" is valid. "5234567" is NOT valid (starts with 5).
        """
        if value is None:
            return False
        cleaned = str(value)
        return cleaned.isdigit() and len(cleaned) == 7 and cleaned[0] in '1234'

    @staticmethod
    def extract_hsn_from_text(text: str):
        """
        Kept only for reference / possible future use. NOT called
        automatically anymore, because it was too loose (it grabbed any
        4/6/8-digit number from the item description, even if it wasn't
        really an HSN code — e.g. a batch number that happened to be
# END OF EXCERPT. The remaining code is private.
