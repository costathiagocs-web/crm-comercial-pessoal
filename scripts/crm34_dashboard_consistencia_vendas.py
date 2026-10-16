from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="function analysis(){let pending=data.orcamentos.filter(o=>['pendente','negociacao'].includes(o.status));let overdue=pending.filter(o=>o.proximo_contato&&o.proximo_contato<today());let old=pending.filter(o=>days(o.data_orcamento)>=5&&!data.acompanhamentos.some(a=>a.orcamento_id===o.id));let win=data.orcamentos.filter(o=>o.status==='aprovado').length;let lost=data.orcamentos.filter(o=>o.status==='perdido');let notes=[];"
new="function analysis(){let soldQuoteIds=new Set(data.vendas.map(v=>v.orcamento_id).filter(Boolean));let pending=data.orcamentos.filter(o=>['pendente','negociacao'].includes(o.status)&&!soldQuoteIds.has(o.id));let overdue=pending.filter(o=>o.proximo_contato&&o.proximo_contato<today());let old=pending.filter(o=>days(o.data_orcamento)>=5&&!data.acompanhamentos.some(a=>a.orcamento_id===o.id));let win=data.orcamentos.filter(o=>o.status==='aprovado'||soldQuoteIds.has(o.id)).length;let lost=data.orcamentos.filter(o=>o.status==='perdido'&&!soldQuoteIds.has(o.id));let notes=[];"
if old not in s: raise SystemExit('analysis alvo nao encontrado')
s=s.replace(old,new,1)
old2="function priorityList(){return data.orcamentos.filter(o=>['pendente','negociacao'].includes(o.status)).map(o=>({...o,_p:priorityScore(o)})).sort((a,b)=>b._p.score-a._p.score||Number(b.valor)-Number(a.valor))}"
new2="function priorityList(){const soldQuoteIds=new Set(data.vendas.map(v=>v.orcamento_id).filter(Boolean));return data.orcamentos.filter(o=>['pendente','negociacao'].includes(o.status)&&!soldQuoteIds.has(o.id)).map(o=>({...o,_p:priorityScore(o)})).sort((a,b)=>b._p.score-a._p.score||Number(b.valor)-Number(a.valor))}"
if old2 in s: s=s.replace(old2,new2,1)
old3="function statsSummary(){const q=data.orcamentos,v=data.vendas,approved=q.filter(o=>o.status==='aprovado'),lost=q.filter(o=>o.status==='perdido'),pending=priorityList(),value=q.reduce((s,o)=>s+Number(o.valor||0),0),sold=v.reduce((s,o)=>s+Number(o.valor||0),0);return {q,v,approved,lost,pending,value,sold,rate:q.length?approved.length/q.length*100:null}}"
new3="function statsSummary(){const q=data.orcamentos,v=data.vendas,soldQuoteIds=new Set(v.map(x=>x.orcamento_id).filter(Boolean)),approved=q.filter(o=>o.status==='aprovado'||soldQuoteIds.has(o.id)),lost=q.filter(o=>o.status==='perdido'&&!soldQuoteIds.has(o.id)),pending=priorityList(),value=q.reduce((s,o)=>s+Number(o.valor||0),0),sold=v.reduce((s,o)=>s+Number(o.valor||0),0);return {q,v,approved,lost,pending,value,sold,rate:q.length?approved.length/q.length*100:null}}"
if old3 in s: s=s.replace(old3,new3,1)
p.write_text(s,encoding='utf-8')
