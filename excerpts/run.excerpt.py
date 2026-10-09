# PRIVACY NOTICE: Partial code excerpt only. The full implementation is omitted for privacy.
# Source: run.py | Selected source lines: 79-118
# This incomplete excerpt is for portfolio review; it is not a runnable application.

def _get_db_connection():
    """Opens a connection to the tracking database, creating the table
    if it doesn't exist yet."""
    conn = sqlite3.connect(config.DB_PATH, timeout=30)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS file_status (
            doc_id TEXT PRIMARY KEY,
            filename TEXT,
            status TEXT,
            attempts INTEGER DEFAULT 0,
            error TEXT,
            tokens_used INTEGER DEFAULT 0,
            cost REAL DEFAULT 0.0,
            started_at TEXT,
            finished_at TEXT
        )
    """)
    conn.commit()
    return conn


def _is_already_done(doc_id: str) -> bool:
    """Checks if this file was already successfully processed before."""
    with _db_lock:
        conn = _get_db_connection()
        try:
            row = conn.execute(
                "SELECT status FROM file_status WHERE doc_id = ?", (doc_id,)
            ).fetchone()
            return row is not None and row[0] == "success"
        finally:
            conn.close()


def _mark_started(doc_id: str, filename: str) -> None:
    with _db_lock:
        conn = _get_db_connection()
        try:
            now = datetime.now(timezone.utc).isoformat()
            conn.execute("""
# END OF EXCERPT. The remaining code is private.
