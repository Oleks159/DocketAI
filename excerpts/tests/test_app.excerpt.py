# PRIVACY NOTICE: Partial code excerpt only. The full implementation is omitted for privacy.
# Source: tests/test_app.py | Selected source lines: 14-53
# This incomplete excerpt is for portfolio review; it is not a runnable application.

def dataset():
    root = Path(os.getenv('DOCUAI_TEST_PDFS', r'<local-project-path>'))
    files = sorted(root.rglob('*.pdf'))
    if len(files)<3:
        pytest.skip('Set DOCUAI_TEST_PDFS to a folder containing at least three existing PDFs')
    return files

@pytest.fixture(autouse=True)
def isolated_db(tmp_path, monkeypatch):
    monkeypatch.setenv('DOCUAI_DATA_DIR',str(tmp_path))
    monkeypatch.setenv('DOCUAI_EXTRACTION_MODE','local')
    monkeypatch.setenv('DOCUAI_CHAT_MODE','local')
    initialize()

def stub(monkeypatch, **values):
    fields=Fields(supplier='Test supplier',document_type='Invoice',invoice_number='BUS-101',invoice_date='2026-09-05',amount=100,currency='USD',payment_terms='Net 30',payment_details='DE00111111111111111111')
    for name,value in values.items():
        setattr(fields,name,value)
    monkeypatch.setattr(document_service,'extract',lambda path:(fields,[{'page':1,'text':f'{path.name} unique searchable evidence BANK_ACCOUNT 123'}],[],[],{'mode':'local'}))

def test_real_pdf_extraction_and_idempotence(dataset):
    doc,outcome=process_document(dataset[0])
    assert outcome=='processed' and doc['status']!='Failed'
    assert len(doc['extracted_text'])>100
    again,outcome=process_document(dataset[0])
    assert outcome=='skipped' and again['id']==doc['id']
    with connection() as con:
        assert con.execute('SELECT count(*) FROM documents').fetchone()[0]==1
        assert con.execute('SELECT count(*) FROM chunks').fetchone()[0]>0

def test_business_rules_approved_baseline_and_duplicates(dataset,monkeypatch):
    stub(monkeypatch)
    first,_=process_document(dataset[0]);assert first['status']=='Validated' and first['review_reason'] is None
    approve_document(first['id'],Review(note='Confirmed supplier and payment details'))
    second,_=process_document(dataset[1]);assert 'Possible duplicate' in second['review_reason']
    stub(monkeypatch,invoice_number='BUS-102',amount=2000,payment_details='DE00999999999999999999')
    third,_=process_document(dataset[2]);assert 'Payment details changed' in third['review_reason'] and third['approval_reason'] is None
    assert 'New supplier' not in third['review_reason']

def test_changed_details_are_not_trusted_without_approval(dataset,monkeypatch):
# END OF EXCERPT. The remaining code is private.
