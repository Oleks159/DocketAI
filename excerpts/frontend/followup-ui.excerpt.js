// PRIVACY NOTICE: Partial code excerpt only. The full implementation is omitted for privacy.
// Source: frontend/followup-ui.js | Selected source lines: 1-32
// This incomplete excerpt is for portfolio review; it is not a runnable application.

(()=>{

  const labelInput=(form,key,title,value,type='text')=>{

    const label=document.createElement('label');label.style.cssText='display:block;margin:12px 0';label.textContent=title;

    const input=document.createElement(type==='textarea'?'textarea':'input');input.name=key;input.value=value||'';

    if(type!=='textarea')input.type=type;input.style.cssText='display:block;width:100%;padding:8px';

    if(['issue','action','contact','note'].includes(key)){input.required=key!=='note';input.maxLength=key==='action'?4000:key==='contact'?300:2000;}

    label.append(input);form.append(label);return input;

  };

  window.openFollowup=async(doc,item=null,onSave=null)=>{

    const node=document.createElement('dialog');node.className='card followup-dialog';node.style.cssText='width:min(700px,94vw);max-height:85vh;overflow:auto;padding:24px;border:1px solid #ddd';

    const heading=document.createElement('h2');heading.textContent=item?'Edit follow-up':'Add follow-up';

    const file=document.createElement('p');file.className='task-context';file.textContent=[doc.supplier,doc.invoice_number].filter(Boolean).join('  /  ')||doc.filename;

    const info=document.createElement('p');info.textContent='Record what needs to happen next. This does not contact anyone or approve the invoice.';

    const reason=doc.review_reason||'';let suggestion='Contact supplier to clarify this invoice.';if(/payment details changed/i.test(reason))suggestion='Confirm the new bank details with the supplier using a contact already on file before paying.';else if(/duplicate/i.test(reason))suggestion='Ask th ... [line shortened for privacy]

    labelInput(form,'action','What should happen next?',item?.action||suggestion,'textarea');

    labelInput(form,'contact','Who to contact (name or role)',item?.contact||'Supplier');

// END OF EXCERPT. The remaining code is private.
