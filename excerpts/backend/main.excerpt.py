# PRIVACY NOTICE: Partial code excerpt only. The full implementation is omitted for privacy.
# Source: backend/main.py | Selected source lines: 61-100
# This incomplete excerpt is for portfolio review; it is not a runnable application.

@app.get('/api/documents')
def documents(search: str = Query(default='', max_length=500), status: str = '', sort: str = 'newest', page: int = Query(default=1,ge=1), page_size: int = Query(default=12,ge=1,le=200)):
    ordering = {'newest':'received_at DESC,id DESC','oldest':'received_at ASC,id ASC','amount':'currency ASC,amount DESC,id DESC','filename':'filename ASC,id ASC'}
    if sort not in ordering:
        raise HTTPException(422,'Invalid sort')
    clauses, params = [], []
    if status:
        if status not in ('Validated','Processing','Needs Review','Failed','Approval Required','Paid','Unpaid','Payment unknown'):
            raise HTTPException(422,'Invalid status')
        if status=='Approval Required':status='Needs Review'
        if status in ('Paid','Unpaid','Payment unknown'):
            paid="(SELECT coalesce(sum(p.amount_cents),0) FROM payments p WHERE p.document_id=effective_documents.id AND p.dataset=CASE WHEN effective_documents.is_demo=1 THEN 'demo' ELSE 'original' END AND p.voided_at IS NULL)"
            fully_paid=f"({paid}>0 AND amount IS NOT NULL AND {paid}>=round(amount*100))"
            known=f"({paid}>0 OR payment_tracking='Unpaid')"
            clauses.append("status='Validated'")
            clauses.append(fully_paid if status=='Paid' else f"({known} AND NOT {fully_paid})" if status=='Unpaid' else f"NOT {known}")
        else:
            clauses.append('status=?')
            params.append(status)
    if search:
        clauses.append("(filename LIKE ? ESCAPE '\\' OR supplier LIKE ? ESCAPE '\\' OR invoice_number LIKE ? ESCAPE '\\')")
        search=search.strip().strip('*`').strip().replace('–','-').replace('—','-').replace('‑','-')
        pattern = '%' + search.replace('\\','\\\\').replace('%','\\%').replace('_','\\_') + '%'
        params.extend([pattern]*3)
    where = ' WHERE ' + ' AND '.join(clauses) if clauses else ''
    with connection() as con:
        total = con.execute('SELECT count(*) FROM effective_documents'+where, params).fetchone()[0]
        rows = con.execute('SELECT * FROM effective_documents'+where+' ORDER BY '+ordering[sort]+' LIMIT ? OFFSET ?', (*params,page_size,(page-1)*page_size)).fetchall()
    return {'items':[serialize(row) for row in rows],'total':total,'page':page,'page_size':page_size}

@app.post('/api/documents/select')
def select(request: Selection):
    try:
        rows = scoped_documents(request.document_ids)
        return {'documents':[{'id':row['id'],'filename':row['filename']} for row in rows]}
    except LookupError as exc:
        raise HTTPException(404,str(exc))
    except ValueError as exc:
        raise HTTPException(422,str(exc))

# END OF EXCERPT. The remaining code is private.
