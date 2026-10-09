# PRIVACY NOTICE: Partial code excerpt only. The full implementation is omitted for privacy.
# Source: tests/test_followups.py | Selected source lines: 11-40
# This incomplete excerpt is for portfolio review; it is not a runnable application.

def test_followup_creation_export_audit_and_dataset_scope(dataset,monkeypatch):
    stub(monkeypatch);doc,_=process_document(dataset[0])
    request={'document_id':doc['id'],'issue':'Tax looks incorrect','action':'Contact supplier for a corrected invoice','contact':'Supplier','owner':'Alex'}
    with TestClient(app) as client:
        result=client.post('/api/followups',json=request).json();assert result['created']
        row_id=result['item']['id'];assert not client.post('/api/followups',json=request).json()['created']
        assert client.get('/api/followups').json()['counts']['Open']==1
        assert client.post(f'/api/followups/{row_id}',json={'status':'Waiting','note':'Requested corrected invoice'}).status_code==200
        assert client.get('/api/followups?status=Waiting').json()['items'][0]['document_id']==doc['id']
        assert client.get('/api/followups?search=absent').json()['items']==[]
        assert client.post(f'/api/followups/{row_id}',json={'status':'Done'}).status_code==200
        assert client.post('/api/followups',json=request|{'document_id':999}).status_code==404
        # Formula-like user text remains inert when opened in Excel.
        client.post(f'/api/followups/{row_id}',json={'contact':'=HYPERLINK("bad")','note':'Test literal contact string'})
        exported=client.get('/api/followups/export');assert exported.status_code==200
        rows=list(csv.DictReader(io.StringIO(exported.text.lstrip('\ufeff'))));assert rows[0]['contact'].startswith("'=")
        assert rows[0]['filename']==doc['filename']
        with connection() as con:
            assert con.execute('SELECT count(*) FROM followup_events').fetchone()[0]==4
            assert con.execute('SELECT status FROM documents').fetchone()[0]=='Validated'
            con.execute("UPDATE app_settings SET value='demo' WHERE key='dataset_mode'")
        assert client.get('/api/followups').json()['items']==[]
        assert client.post(f'/api/followups/{row_id}',json={'status':'Done','note':'Other dataset'}).status_code==404
        assert client.post(f'/api/followups/{row_id}/delete').status_code==404

def test_delete_restore_without_notes(dataset,monkeypatch):
    stub(monkeypatch);doc,_=process_document(dataset[0])
    with TestClient(app) as client:
        item=client.post('/api/followups',json={'document_id':doc['id'],'issue':'Incorrect tax','action':'Contact supplier'}).json()['item']
        assert client.post(f'/api/followups/{item["id"]}/delete').status_code==200
# END OF EXCERPT. The remaining code is private.
