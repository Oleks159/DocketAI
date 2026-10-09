# PRIVACY NOTICE: Partial code excerpt only. The full implementation is omitted for privacy.
# Source: backend/services/demo_service.py | Selected source lines: 12-51
# This incomplete excerpt is for portfolio review; it is not a runnable application.

def scenario_text(doc,payload):
    return NOTE+'\nSource filename: '+doc['filename']+'\n'+'\n'.join(f'{key}: {value}' for key,value in payload.items() if key not in ('extracted_text','extraction_warnings'))

def seed_demo():
    initialize()
    with connection() as con:
        if con.execute('SELECT count(*) FROM demo_overrides').fetchone()[0]:
            return {'created':0,'note':'Existing demo scenario preserved; user payment/review changes were not reset.'}
        docs=[dict(row) for row in con.execute("SELECT * FROM documents WHERE status IN ('Validated','Needs Review') ORDER BY filename LIMIT 100")]
        if len(docs)<8:raise ValueError('Load at least eight real dataset PDFs before creating the scenario')
        current=today()
        for index,name in enumerate(SUPPLIERS):
            con.execute('INSERT OR IGNORE INTO suppliers VALUES (?,?,?,?)',('demo:'+supplier_key(name),name,payment_key('DEMO-BANK-'+str(index+1)),now()))
        first_payload=None
        for index,doc in enumerate(docs):
            supplier_index=index%8;cycle=index//8
            issued=month_start(current,-(cycle//2))
            issued=issued+timedelta(days=min(3 if cycle%2 else 0,max(0,current.day-1)) if cycle<2 else (3 if cycle%2 else 0))
            terms=[14,30,45][supplier_index%3]
            subtotal=[125,240,360,450,680,920,1350,2100][supplier_index]+(6-cycle//2)*5+(20 if cycle%2 else 0)
            amount=round(subtotal*1.2,2)
            payload=Fields(supplier=SUPPLIERS[supplier_index],document_type='Invoice',invoice_number=f'DEMO-{issued:%Y%m}-{index+1:04}',invoice_date=issued.isoformat(),due_date=(issued+timedelta(days=terms)).isoformat(),invoice_date_raw=issued.isoformat(),due_date_raw=(issued+timedelta(days=terms)). ... [line shortened for privacy]
            if index==0:first_payload=dict(payload)
            if index==1:
                payload=dict(first_payload)
            if index==2:payload['payment_details']='DEMO-CHANGED-BANK'
            if index==3:payload['subtotal']+=50
            if index==4:payload['recipient']='Another Demo Business'
            payload.update(supplier_key=supplier_key(payload['supplier']),status='Validated',review_reason=None,approval_reason=None,payment_tracking='Unpaid',extraction_warnings=json.dumps([NOTE]))
            payload['extracted_text']=scenario_text(doc,payload)
            con.execute('INSERT INTO demo_overrides VALUES (?,?)',(doc['id'],json.dumps(payload)))
            # Old invoices include both full and partial payments; current bills
            # remain unpaid to make upcoming due-date queries useful.
            if cycle>=2 and index%5!=0:
                paid_on=min(issued+timedelta(days=terms-3),current)
                paid_cents=cents(amount)//2 if index%7==0 else cents(amount)
                con.execute('INSERT INTO payments(document_id,dataset,amount_cents,currency,paid_on,reference,note,created_at) VALUES (?,?,?,?,?,?,?,?)',(doc['id'],'demo',paid_cents,'USD',paid_on.isoformat(),f'DEMO-PAYMENT-{doc["id"]}','Simulated payment for demo only',now()))
        con.execute("UPDATE app_settings SET value='demo' WHERE key='dataset_mode'")
        recheck_demo(con)
        return {'created':len(docs),'dataset':'demo','note':NOTE}
# END OF EXCERPT. The remaining code is private.
