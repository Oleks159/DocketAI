# PRIVACY NOTICE: Partial code excerpt only. The full implementation is omitted for privacy.
# Source: tests/test_model_answers.py | Selected source lines: 11-50
# This incomplete excerpt is for portfolio review; it is not a runnable application.

def test_typo_with_no_text_hits_still_calls_model_on_scoped_flags(dataset,monkeypatch):
    stub(monkeypatch);first,_=process_document(dataset[0]);second,_=process_document(dataset[1])
    reason='Financial figures conflict: subtotal plus tax does not match payable total.'
    with connection() as con:con.execute("UPDATE documents SET status='Needs Review',review_reason=? WHERE id=?",(reason,first['id']))
    question='is there anz document that contains descrepancies?'
    assert retrieve(question,[first['id']])==[]
    monkeypatch.setenv('DOCUAI_CHAT_MODE','gemini');calls=[]
    def respond(prompt,model):
        calls.append(prompt);assert question in prompt and reason in prompt and second['filename'] not in prompt
        return GroundedAnswer(claims=[Claim(statement='This invoice has a possible total mismatch.',document_id=first['id'],quote=reason)],missing_information='')
    monkeypatch.setattr(provider_service,'gemini_structured',respond)
    result=ask(Question(question=question,document_ids=[first['id']]))
    assert len(calls)==1 and result['mode']=='gemini' and result['sources'][0]['document_id']==first['id']

def test_model_requests_verified_calculation_and_cannot_broaden_scope(dataset,monkeypatch):
    stub(monkeypatch);first,_=process_document(dataset[0]);second,_=process_document(dataset[1])
    monkeypatch.setenv('DOCUAI_CHAT_MODE','gemini');calls=[]
    plan=CalculationSpec(kind='invoiced',start=date(2026,9,1),end=date(2026,9,30))
    def respond(prompt,model):
        calls.append(prompt)
        if len(calls)==1:return GroundedAnswer(claims=[],missing_information='',requested_calculation=plan)
        quote='Invoiced amounts for 2026-09-01 through 2026-09-30: USD 100.00.'
        assert quote in prompt
        return GroundedAnswer(claims=[Claim(statement='You were invoiced USD 100.00 in September.',document_id=0,quote=quote)],missing_information='')
    monkeypatch.setattr(provider_service,'gemini_structured',respond)
    result=ask(Question(question='What did these bills cost last September?',document_ids=[first['id']]))
    assert len(calls)==2 and result['mode']=='gemini' and len(result['sources'])==1
    calls.clear();plan.document_ids=[second['id']]
    with pytest.raises(ValueError,match='scope'):ask(Question(question='What did these bills cost?',document_ids=[first['id']]))


def test_model_selects_presentation_and_history_preserves_it(dataset,monkeypatch):
    from fastapi.testclient import TestClient
    from backend.main import app
    stub(monkeypatch);doc,_=process_document(dataset[0])
    monkeypatch.setenv('DOCUAI_CHAT_MODE','gemini')
    for presentation in ('narrative','invoice_list'):
        monkeypatch.setattr(provider_service,'gemini_structured',lambda prompt,model:GroundedAnswer(presentation=presentation,claims=[Claim(statement='The record names Test supplier.',document_id=doc['id'],quote='Test supplier')],missing_information=''))
        result=ask(Question(question='Explain this record',document_ids=[doc['id']],session_id='adaptive'))
        assert result['presentation']==presentation
# END OF EXCERPT. The remaining code is private.
