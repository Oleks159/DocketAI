# PRIVACY NOTICE: Partial code excerpt only. The full implementation is omitted for privacy.
# Source: backend/services/followup_service.py | Selected source lines: 9-48
# This incomplete excerpt is for portfolio review; it is not a runnable application.

def list_followups(search='',status='',deleted=False):
    with connection() as con:
        rows=[dict(row) for row in con.execute('SELECT f.*,d.invoice_number,d.status AS document_status,d.review_reason AS document_review_reason FROM followups f LEFT JOIN effective_documents d ON d.id=f.document_id WHERE f.dataset=? ORDER BY f.id DESC',(dataset_mode(con),))]
    rows=[row for row in rows if bool(row['deleted_at'])==deleted]
    if status:rows=[row for row in rows if row['status']==status]
    if search:
        value=search.casefold()
        rows=[row for row in rows if any(value in str(row[key] or '').casefold() for key in ('filename','supplier','issue','action','contact','owner'))]
    for row in rows:row['document_url']=f'/document.html?id={row["document_id"]}'
    return rows

def create_followup(request,note='Created by user during document review'):
    with connection() as con:
        con.execute('BEGIN IMMEDIATE')
        doc=con.execute('SELECT * FROM effective_documents WHERE id=?',(request.document_id,)).fetchone()
        if doc is None:raise LookupError('Document not found')
        if doc['status'] not in ('Validated','Needs Review'):raise ValueError('Process this document before creating a follow-up')
        active=dataset_mode(con)
        existing=con.execute("SELECT * FROM followups WHERE document_id=? AND dataset=? AND issue=? AND action=? AND contact=? AND status!='Done' AND deleted_at IS NULL",(request.document_id,active,request.issue,request.action,request.contact)).fetchone()
        if existing:return {'item':dict(existing),'created':False}
        values=request.model_dump(mode='json')
        values.update(dataset=active,filename=doc['filename'],supplier=doc['supplier'],created_at=now(),updated_at=now())
        cursor=con.execute('INSERT INTO followups('+','.join(values)+') VALUES ('+','.join('?' for _ in values)+')',tuple(values.values()))
        item=dict(con.execute('SELECT * FROM followups WHERE id=?',(cursor.lastrowid,)).fetchone())
        con.execute('INSERT INTO followup_events(followup_id,note,after_json,created_at) VALUES (?,?,?,?)',(item['id'],note,json.dumps(item),now()))
        return {'item':item,'created':True}

def update_followup(row_id,request):
    with connection() as con:
        con.execute('BEGIN IMMEDIATE')
        before=con.execute('SELECT * FROM followups WHERE id=? AND dataset=? AND deleted_at IS NULL',(row_id,dataset_mode(con))).fetchone()
        if before is None:raise LookupError('Follow-up not found in the current dataset')
        values=request.model_dump(mode='json',exclude_unset=True)
        note=values.pop('note','') or 'Task updated'
        if any(value is None for key,value in values.items() if key!='due_on'):raise ValueError('Only the due date can be cleared')
        if not values:raise ValueError('Choose a field to update')
        values['updated_at']=now()
        con.execute('UPDATE followups SET '+','.join(key+'=?' for key in values)+' WHERE id=?',(*values.values(),row_id))
        after=dict(con.execute('SELECT * FROM followups WHERE id=?',(row_id,)).fetchone())
        con.execute('INSERT INTO followup_events(followup_id,note,before_json,after_json,created_at) VALUES (?,?,?,?,?)',(row_id,note,json.dumps(dict(before)),json.dumps(after),now()))
# END OF EXCERPT. The remaining code is private.
