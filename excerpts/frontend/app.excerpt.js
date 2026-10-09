// PRIVACY NOTICE: Partial code excerpt only. The full implementation is omitted for privacy.
// Source: frontend/app.js | Selected source lines: 89-128
// This incomplete excerpt is for portfolio review; it is not a runnable application.

async function refreshInbox() {
  const params=new URLSearchParams({...state,page_size:12});
  const [response,stats]=await Promise.all([api('/api/documents?'+params),api('/api/stats')]);total=response.total;
  all('.stat-value').forEach((node,index)=>node.textContent=[stats.processed,stats.processing,stats.needs_review,stats.new_today][index]);
  const body=$('.docs tbody');body.replaceChildren();
  if(!response.items.length) body.innerHTML='<tr><td colspan="5">No documents match. Ingest local PDFs using the command in README-DocuAI.md.</td></tr>';
  for(const doc of response.items) {
    const row=document.createElement('tr');const display=['Validated','Needs Review','Processing'].includes(doc.status)?doc.status:'';const badge={'Paid':'pill-ok','Unpaid':'pill-info','Payment unknown':'pill-info','Processing':'pill-info','Needs Review':'pill-warn','Failed':'pill-risk'}[display];
    row.innerHTML=`<td><div class="doc-name"><input type="checkbox" aria-label="Select ${esc(doc.filename)}" ${selected.has(doc.id)?'checked':''} ${['Failed','Processing'].includes(doc.status)?'disabled':''}>${icon('file')}<button type="button" class="btn-link doc-file">${esc(doc.filename)}</button> ... [line shortened for privacy]
    $('input',row).onchange=event=>{if(event.target.checked) selected.set(doc.id,doc.filename);else selected.delete(doc.id);$('#ask-selected').textContent=`Ask selected (${selected.size})`;$('#ask-selected').disabled=!selected.size;};
    const statusCell=row.lastElementChild;
    statusCell.classList.add('invoice-status-cell');

    for(const [label,value] of [['Review reason',doc.review_reason],['Approval reason',doc.approval_reason],['Processing error',doc.processing_error]]){
      if(!value)continue;const reason=document.createElement('p');reason.className='invoice-row-reason';
      reason.textContent=`${label}: ${value.replace(/^Approval required:\s*/i,'')}`;statusCell.append(reason);
    }
    if(doc.due_date){const due=document.createElement('span');due.className='invoice-payment-line';due.textContent=`Due ${doc.due_date}`;statusCell.append(due);}
    $('.doc-file',row).onclick=()=>{location.href=`/document.html?id=${doc.id}`;};body.append(row);
  }
  const start=total ? (state.page-1)*12+1:0,end=Math.min(state.page*12,total);
  $('.table-footer > span').textContent=`Showing ${start}–${end} of ${total} documents${stats.failed ? ` · ${stats.failed} failed (filter to inspect)` : ''}`;
  const pager=$('.pagination');pager.replaceChildren();
  const previous=button('‹',()=>{state.page--;refreshInbox().catch(message);},'btn btn-icon');previous.disabled=state.page===1;previous.setAttribute('aria-label','Previous page');
  const next=button('›',()=>{state.page++;refreshInbox().catch(message);},'btn btn-icon');next.disabled=end>=total;next.setAttribute('aria-label','Next page');
  const current=document.createElement('span');current.textContent=`${state.page} / ${Math.max(1,Math.ceil(total/12))}`;pager.append(previous,current,next);
}
async function inbox() {
  const connectionTitle=$('.connection-title');connectionTitle.innerHTML='Local PDFs <span class="badge-active">Active</span>';
  $('.connection-email').textContent=health.dataset==='demo'?'DEMO DATA · Simulated dates, supplier history and payments · Original PDFs unchanged':`Original PDF data · ${health.extraction_mode === 'local' ? 'Local extraction' : 'AI extraction'}`;
  $('.last-sync').textContent='Live SQLite data';
  const sync=$('.connection-sync button');sync.innerHTML=icon('sync')+'Refresh';sync.onclick=async()=>{sync.disabled=true;try{const arrival=await api('/api/video-arrival/refresh',{});if(arrival.started){state.status='';state.sort='newest';state.page=1;state.search='';$('.search input').value='';cons ... [line shortened for privacy]
  const controls=$('.toolbar-controls'),buttons=all('.toolbar-controls > button');
  const askSelected=button('Ask selected (0)',async()=>{try {const result=await api('/api/documents/select',{document_ids:[...selected.keys()]});sessionStorage.setItem('docuai-selection',JSON.stringify(result.documents));location.href='ask-selected.html';}catch(error){message(error);}},'btn btn-stro ... [line shortened for privacy]
  let timer;$('.search input').oninput=event=>{clearTimeout(timer);timer=setTimeout(()=>{state.search=event.target.value;state.page=1;refreshInbox().catch(message);},250);};
  const filter=document.createElement('label');filter.className='btn status-dropdown';filter.innerHTML=icon('filter')+'Status: ';
  const select=document.createElement('select');select.setAttribute('aria-label','Filter document status');
  for(const [value,label] of [['','All invoices'],['Validated','Validated'],['Needs Review','Needs Review'],['Processing','Processing']]){
    const option=document.createElement('option');option.value=value;option.textContent=label;select.append(option);
  }
// END OF EXCERPT. The remaining code is private.
