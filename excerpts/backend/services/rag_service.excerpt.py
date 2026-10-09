# PRIVACY NOTICE: Partial code excerpt only. The full implementation is omitted for privacy.
# Source: backend/services/rag_service.py | Selected source lines: 31-70
# This incomplete excerpt is for portfolio review; it is not a runnable application.

def retrieve(question, ids, limit=8):
    words = [word for word in re.findall(r'\w+', question.lower()) if word not in STOPWORDS][:30]
    if not words or not ids:
        return []
    expression = ' OR '.join('"' + word.replace('"','') + '"' for word in words)
    with connection() as con:
        if dataset_mode(con)=='demo':
            docs=con.execute('SELECT * FROM effective_documents WHERE id IN ('+','.join('?' for _ in ids)+') AND is_demo=1',ids).fetchall()
            ranked=[]
            for row in docs:
                score=sum(word in row['extracted_text'].casefold() for word in words)
                if score:ranked.append({'text':row['extracted_text'],'document_id':row['id'],'page':1,'filename':row['filename'],'rank':-score})
            return sorted(ranked,key=lambda item:item['rank'])[:limit]
        # Scope filtering occurs inside the retrieval SQL, before ranking/limit.
        rows = con.execute('SELECT s.text,s.document_id,s.page,d.filename,bm25(chunk_search) AS rank FROM chunk_search s JOIN documents d ON d.id=s.document_id WHERE chunk_search MATCH ? AND s.document_id IN (' + ','.join('?' for _ in ids) + ') ORDER BY rank LIMIT ?', (expression, *ids, limit)).fetchall()
        return [dict(row) for row in rows]

def source(doc,ledger=False):
    target='record' if doc.get('is_demo') or ledger else 'file'
    return {'document_id': doc['id'], 'filename': doc['filename'], 'url': f"/api/documents/{doc['id']}/{target}", 'supplier':doc.get('supplier'),'invoice_number':doc.get('invoice_number'),'status':doc.get('status'),'data_origin':'demo scenario' if doc.get('is_demo') else ('recorded payment data' if ledger else 'source PDF')}

def summary(doc):
    amount = f"{doc['currency'] or 'currency unknown'} {doc['amount']:.2f}" if doc['amount'] is not None else 'amount unknown'
    return f"[{doc['filename']}] Supplier: {doc['supplier'] or 'unknown'}; invoice: {doc['invoice_number'] or 'unknown'}; amount: {amount}; invoice date: {doc['invoice_date'] or doc['invoice_date_raw'] or 'unknown'}; due: {doc['due_date'] or doc['due_date_raw'] or 'unknown'}; terms: {doc['payment_te ... [line shortened for privacy]

def structured_answer(question, docs):
    from backend.services.finance_service import finance_answer
    financial=finance_answer(question,docs)
    if financial:return financial
    q = question.casefold()
    picked = None
    intro = ''
    if 'duplicate' in q:
        picked = [doc for doc in docs if 'duplicate' in (doc['review_reason'] or '').lower()]
        intro = f'{len(picked)} possible duplicate documents in this scope.'
    elif 'approval' in q:
        picked=[doc for doc in docs if doc.get('approval_reason')]
        intro=f'{len(picked)} invoices require amount-based approval, separately from discrepancy review.'
    elif any(term in q for term in ('payment change', 'payment detail', 'bank change')):
        picked = [doc for doc in docs if 'payment details changed' in (doc['review_reason'] or '').lower()]
# END OF EXCERPT. The remaining code is private.
