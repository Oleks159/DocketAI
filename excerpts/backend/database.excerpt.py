# PRIVACY NOTICE: Partial code excerpt only. The full implementation is omitted for privacy.
# Source: backend/database.py | Selected source lines: 12-51
# This incomplete excerpt is for portfolio review; it is not a runnable application.

def connection():
    path = db_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path, timeout=30)
    con.row_factory = sqlite3.Row
    con.execute('PRAGMA foreign_keys=ON')
    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()

def initialize():
    with connection() as con:
        con.execute('PRAGMA journal_mode=WAL')
        con.executescript('''
        CREATE TABLE IF NOT EXISTS documents (
          id INTEGER PRIMARY KEY, content_hash TEXT NOT NULL UNIQUE,
          filename TEXT NOT NULL, file_path TEXT NOT NULL,
          supplier TEXT, supplier_key TEXT, document_type TEXT,
          invoice_number TEXT, invoice_date TEXT, due_date TEXT,
          invoice_date_raw TEXT, due_date_raw TEXT,
          amount REAL, currency TEXT, subtotal REAL, vat REAL,
          payment_terms TEXT, payment_details TEXT,
          status TEXT NOT NULL CHECK(status IN ('Processing','Validated','Needs Review','Failed')),
          review_reason TEXT, extracted_text TEXT NOT NULL DEFAULT '',
          extraction_mode TEXT, extraction_warnings TEXT NOT NULL DEFAULT '[]',
          raw_extraction TEXT NOT NULL DEFAULT '{}', processing_error TEXT,
          source_type TEXT NOT NULL DEFAULT 'local', source_message_id TEXT, source_attachment_id TEXT,
          received_at TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_documents_supplier ON documents(supplier_key, invoice_number);
        CREATE INDEX IF NOT EXISTS idx_documents_status ON documents(status, received_at);
        CREATE TABLE IF NOT EXISTS suppliers (
          supplier_key TEXT PRIMARY KEY, name TEXT NOT NULL,
          approved_payment_details TEXT, approved_at TEXT NOT NULL
        );
# END OF EXCERPT. The remaining code is private.
