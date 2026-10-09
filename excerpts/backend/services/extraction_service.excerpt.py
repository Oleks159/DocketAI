# PRIVACY NOTICE: Partial code excerpt only. The full implementation is omitted for privacy.
# Source: backend/services/extraction_service.py | Selected source lines: 12-51
# This incomplete excerpt is for portfolio review; it is not a runnable application.

def money(value):
    if value is None:
        return None
    cleaned = re.sub(r'[^\d.,-]', '', str(value))
    if not cleaned:
        return None
    if ',' in cleaned and '.' in cleaned:
        cleaned = cleaned.replace(',', '') if cleaned.rfind('.') > cleaned.rfind(',') else cleaned.replace('.', '').replace(',', '.')
    elif ',' in cleaned:
        cleaned = cleaned.replace(',', '.') if len(cleaned.split(',')[-1]) == 2 else cleaned.replace(',', '')
    try:
        return float(Decimal(cleaned))
    except InvalidOperation:
        return None

def normalize_date(value):
    if not value:
        return None
    # Clipped years (e.g. 03/22/2) are never guessed.
    for fmt in ('%Y-%m-%d', '%m/%d/%Y', '%d.%m.%Y', '%d %b %Y', '%B %d, %Y'):
        try:
            return datetime.strptime(value.strip(), fmt).date().isoformat()
        except ValueError:
            pass
    return None

def capture(text, pattern):
    match = re.search(pattern, text, re.I)
    return match.group(1).strip() if match else None

def local_fields(text, sorted_text):
    result = Fields(document_type='Invoice' if re.search(r'\binvoice\b', text, re.I) else ('Receipt' if re.search(r'\breceipt\b', text, re.I) else 'Document'))
    result.invoice_number = capture(text, r'\binvoice\s*(?:number|no\.?|#)\s*[:#]?\s*([A-Z0-9][A-Z0-9/-]*)')
    result.invoice_date_raw = capture(text, r'\binvoice\s*date\s*:\s*([\d./-]+)')
    result.due_date_raw = capture(text, r'\b(?:due\s*date|pay\s*by)\s*:\s*([\d./-]+)')
    if not result.due_date_raw:
        result.due_date_raw = capture(text, r'([\d]{1,2}/[\d]{1,2}/[\d]{1,4})\s*\n\s*BY\s*:')
    result.invoice_date = normalize_date(result.invoice_date_raw)
    result.due_date = normalize_date(result.due_date_raw)
    # A table column "Net" followed by a number on another line is an
# END OF EXCERPT. The remaining code is private.
