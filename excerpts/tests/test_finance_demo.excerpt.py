# PRIVACY NOTICE: Partial code excerpt only. The full implementation is omitted for privacy.
# Source: tests/test_finance_demo.py | Selected source lines: 14-53
# This incomplete excerpt is for portfolio review; it is not a runnable application.

def test_calendar_windows(monkeypatch):
    monkeypatch.setattr(finance_service,'today',lambda:date(2026,10,6))
    assert finance_service.period('due next week','due')==(date(2026,10,12),date(2026,10,18))
    assert finance_service.period('last 3 months','paid')==(date(2026,7,1),date(2026,9,30))
    monkeypatch.setattr(finance_service,'today',lambda:date(2026,12,28))
    assert finance_service.period('next month','due')==(date(2027,1,1),date(2027,1,31))

def test_payment_ledger_scope_validation_and_void(dataset,monkeypatch):
    monkeypatch.setattr(finance_service,'today',lambda:date(2026,10,6))
    stub(monkeypatch,amount=100,due_date='2026-10-15')
    first,_=process_document(dataset[0])
    stub(monkeypatch,invoice_number='SECOND',amount=200,due_date='2026-10-15')
    second,_=process_document(dataset[1])
    assert first['payment_status']=='Unknown'
    assert not ask(Question(question='Invoices due next week'))['sources']
    payment=Payment(amount=40,currency='USD',paid_on='2026-10-02',reference='TRANSFER-1')
    recorded=finance_service.record_payment(first['id'],payment)
    assert recorded['payment_status']=='Partially Paid' and recorded['outstanding_amount']==60
    answer=ask(Question(question='How much did I pay this month?',document_ids=[first['id']]))
    assert 'USD 40.00' in answer['answer'] and len(answer['sources'])==1
    assert answer['sources'][0]['url'].endswith('/record')
    assert not ask(Question(question='How much did I pay this month?',document_ids=[second['id']]))['sources']
    assert 'USD 60.00' in ask(Question(question='Which invoices are due next week?'))['answer']
    for values in [dict(currency='EUR'),dict(amount=61,reference='TOO-MUCH'),dict(paid_on='2026-10-07'),dict(reference='TRANSFER-1')]:
        with pytest.raises(ValueError):finance_service.record_payment(first['id'],Payment(**(payment.model_dump()|values)))
    with pytest.raises(ValueError,match='Void'):approve_document(first['id'],Review(note='Change total',fields=Fields(supplier='Test supplier',amount=500,currency='USD')))
    finance_service.void_payment(recorded['id'],'Correct mistaken record')
    assert not ask(Question(question='How much did I pay this month?'))['sources']
    with connection() as con:assert con.execute('SELECT voided_at FROM payments').fetchone()[0]

def test_demo_provenance_review_policy_and_mode_isolation(dataset,monkeypatch):
    for index,path in enumerate(dataset[:16]):
        stub(monkeypatch,invoice_number=f'ORIGINAL-{index}')
        process_document(path)
    with connection() as con:before=[tuple(row) for row in con.execute('SELECT filename,supplier,invoice_date,amount,extracted_text FROM documents ORDER BY id')]
    result=seed_demo();assert result['created']==16
    with TestClient(app) as client:
        stats=client.get('/api/stats').json();assert stats['needs_review']==4
        docs=client.get('/api/documents?page_size=200').json()['items']
        assert all(doc['is_demo'] for doc in docs)
# END OF EXCERPT. The remaining code is private.
