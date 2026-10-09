# PRIVACY NOTICE: Partial code excerpt only. The full implementation is omitted for privacy.
# Source: backend/services/ai_answer_service.py | Selected source lines: 45-84
# This incomplete excerpt is for portfolio review; it is not a runnable application.

def answer_with_model(question,docs,hits,session_id=None,scope_ids=None):
    from backend.services.rag_service import summary,source
    lookup={doc['id']:doc for doc in docs}
    represented=sorted(docs,key=lambda doc:doc['status']!='Needs Review')[:500]
    evidence=list(hits)
    # Small selected scopes and labelled sample invoices include their complete
    # text, so explanations can cite services and line items without keyword hits.
    for doc in represented:
        if doc.get('extracted_text') and (len(docs)<=5 or doc.get('source_type')=='video_sample'):
            evidence.append({'document_id':doc['id'],'filename':doc['filename'],'page':1,'origin':'Fictional sample PDF' if doc.get('source_type')=='video_sample' else 'Extracted PDF text','text':doc['extracted_text'][:12000]})
    for doc in represented:
        payment=payment_summary(doc)
        text=summary(doc)+'\n'+f"Recipient: {doc.get('recipient') or 'unknown'}\nApproval: {doc.get('approval_reason') or 'none'}\nPayment status: {payment['payment_status']}; recorded paid amount: {doc['currency'] or 'unknown'} {payment['paid_amount']:.2f}; outstanding amount: {payment['outstanding ... [line shortened for privacy]
        evidence.append({'document_id':doc['id'],'filename':doc['filename'],'page':0,'origin':'Stored extracted fields, review flags and recorded payment ledger','text':text})
    coverage={'selected_documents':len(docs),'represented_documents':len(represented),'complete_record_catalog':len(represented)==len(docs)}
    conversation=[]
    if session_id:
        from backend.database import connection,dataset_mode
        with connection() as con:
            previous=con.execute('SELECT question,answer,scope FROM chats WHERE session_id=? AND dataset=? ORDER BY id DESC LIMIT 20',(session_id,dataset_mode(con))).fetchall()
        eligible=[row for row in previous if ((json.loads(row['scope']) is None and scope_ids is None) or (json.loads(row['scope']) is not None and scope_ids is not None and set(json.loads(row['scope']))==set(scope_ids)))]
        conversation=[{'question':row['question'],'answer':row['answer'][:3000]} for row in reversed(eligible[:6])]
    parsed=invoke(question,evidence,coverage,conversation=conversation)
    calculated=None;calc_sources=[]
    if parsed.requested_calculation:
        spec=parsed.requested_calculation
        if (spec.start is None)!=(spec.end is None) or (spec.start and spec.start>spec.end):raise ValueError('AI requested an invalid date window')
        ids=spec.document_ids
        if ids is not None and (not ids or any(doc_id not in lookup for doc_id in ids)):raise ValueError('AI requested calculation outside the document scope')
        selected=[lookup[doc_id] for doc_id in dict.fromkeys(ids)] if ids is not None else docs
        calculated,calc_sources=finance_result(spec.kind,selected,spec.start,spec.end)
        calculation={'document_id':0,'origin':'Verified backend calculation','text':calculated,'source_document_ids':[item['document_id'] for item in calc_sources]}
        parsed=invoke(question,evidence,coverage,calculation,conversation)
        if parsed.requested_calculation:raise ValueError('AI requested a repeated calculation')
    if isinstance(parsed,NaturalAnswer):
        import re
        if not parsed.answer.strip():raise ValueError('AI returned an empty answer')
        cited={};used=[]
        for citation in parsed.citations:
            quote=citation.quote.strip();doc_id=citation.document_id
# END OF EXCERPT. The remaining code is private.
