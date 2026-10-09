# PRIVACY NOTICE: Partial code excerpt only. The full implementation is omitted for privacy.
# Source: backend/services/finance_service.py | Selected source lines: 10-49
# This incomplete excerpt is for portfolio review; it is not a runnable application.

def today():
    return datetime.now(ZoneInfo('Europe/Berlin')).date()

def cents(amount):
    value=Decimal(str(amount))*100
    if value!=value.to_integral_value():
        raise ValueError('Payment amounts must have at most two decimal places')
    return int(value)

def payment_summary(doc,con=None):
    if con is None:
        with connection() as con:
            return payment_summary(doc,con)
    active='demo' if doc.get('is_demo') else 'original'
    paid=con.execute('SELECT coalesce(sum(amount_cents),0) FROM payments WHERE document_id=? AND dataset=? AND voided_at IS NULL',(doc['id'],active)).fetchone()[0]
    total=cents(doc['amount']) if doc.get('amount') is not None else None
    tracking=doc.get('payment_tracking','Unknown')
    status=('Paid' if total is not None and paid>=total else 'Partially Paid') if paid else ('Unpaid' if tracking=='Unpaid' else 'Unknown')
    balance=(total-paid)/100 if total is not None and (paid or tracking=='Unpaid') else None
    return {'paid_amount':paid/100,'payment_status':status,'outstanding_amount':balance,'payment_dataset':active}

def record_payment(doc_id,payment):
    if payment.paid_on>today():
        raise ValueError('A recorded payment cannot have a future payment date')
    with connection() as con:
        con.execute('BEGIN IMMEDIATE')
        row=con.execute('SELECT * FROM effective_documents WHERE id=?',(doc_id,)).fetchone()
        if row is None:raise LookupError('Document not found')
        doc=dict(row)
        if doc['status'] not in ('Validated','Needs Review'):raise ValueError('Process the invoice successfully first')
        if not doc['currency'] or doc['amount'] is None:raise ValueError('Confirm invoice currency and amount before recording payment')
        if payment.currency!=doc['currency']:raise ValueError('Payment currency must match the invoice currency')
        value=cents(payment.amount)
        remaining=cents(doc['amount'])-cents(payment_summary(doc,con)['paid_amount'])
        if value>remaining:raise ValueError('Recorded payment exceeds the remaining invoice amount')
        active='demo' if doc['is_demo'] else 'original'
        if con.execute('SELECT 1 FROM payments WHERE document_id=? AND dataset=? AND reference=? AND voided_at IS NULL',(doc_id,active,payment.reference)).fetchone():raise ValueError('This payment reference is already recorded for this invoice')
        cursor=con.execute('INSERT INTO payments(document_id,dataset,amount_cents,currency,paid_on,reference,note,created_at) VALUES (?,?,?,?,?,?,?,?)',(doc_id,active,value,payment.currency,payment.paid_on.isoformat(),payment.reference,payment.note,now()))
        return {'id':cursor.lastrowid,**payment_summary(doc,con)}

# END OF EXCERPT. The remaining code is private.
