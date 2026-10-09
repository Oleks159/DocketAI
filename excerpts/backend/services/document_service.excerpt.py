# PRIVACY NOTICE: Partial code excerpt only. The full implementation is omitted for privacy.
# Source: backend/services/document_service.py | Selected source lines: 15-54
# This incomplete excerpt is for portfolio review; it is not a runnable application.

def review_reasons(con, fields, document_id, conflicts, *, demo=False):
    reasons = list(conflicts)
    key = supplier_key(fields.supplier)
    trusted = con.execute('SELECT * FROM suppliers WHERE supplier_key=?', ('demo:'+key if demo else key,)).fetchone() if key else None
    if trusted and fields.payment_details and trusted['approved_payment_details'] and payment_key(fields.payment_details) != trusted['approved_payment_details']:
        reasons.append('Payment details changed from the approved supplier baseline.')
    import os
    expected='Demo Company' if demo else os.getenv('COMPANY_NAME','').strip()
    if expected and fields.recipient and supplier_key(fields.recipient)!=supplier_key(expected):
        reasons.append(f'Wrong recipient: addressed to {fields.recipient}, expected {expected}.')
    if fields.amount is not None and fields.subtotal is not None and fields.vat is not None and abs(round(fields.subtotal+fields.vat-fields.amount,2))>0.02:
        reasons.append('Financial figures conflict: subtotal plus tax does not match payable total. Check discounts or other adjustments against the source.')
    if key and fields.invoice_number:
        table='effective_documents' if demo else 'documents'
        matches = con.execute(f"SELECT id,filename FROM {table} WHERE supplier_key=? AND lower(invoice_number)=lower(?) AND id<? AND status IN ('Validated','Needs Review') AND source_type!='archived_video_sample'", (key, fields.invoice_number, document_id)).fetchall()
        if matches:
            reasons.append('Possible duplicate invoice: ' + ', '.join(row['filename'] for row in matches))
    return reasons

def approval_reason(fields):
    # Amount alone no longer triggers review.
    return None


def index_pages(con, doc_id, pages):
    con.execute('DELETE FROM chunks WHERE document_id=?', (doc_id,))
    con.execute('DELETE FROM chunk_search WHERE document_id=?', (doc_id,))
    for page in pages:
        # Overlap protects facts at chunk boundaries. SQLite FTS5 persists the
        # retrieval index alongside application data without external services.
        text = page['text']
        for start in range(0, len(text), 1000):
            chunk = text[start:start + 1300].strip()
            if chunk:
                con.execute('INSERT INTO chunks(document_id,page,text) VALUES (?,?,?)', (doc_id, page['page'], chunk))
                con.execute('INSERT INTO chunk_search(text,document_id,page) VALUES (?,?,?)', (chunk, doc_id, page['page']))

def process_document(file_path, *, source_type='local', source_message_id=None, source_attachment_id=None, force=False):
    """Single entry point for local files and future downloaded attachments.

# END OF EXCERPT. The remaining code is private.
