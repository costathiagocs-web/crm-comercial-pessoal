from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="const quoteOptions='<option value=\"\">Sem orçamento relacionado</option>'+data.orcamentos.map(o=>'<option value=\"'+esc(o.id)+'\"'+(selectedQuote===o.id?' selected':'')+'>'+esc((o.numero_tiny||'Sem número')+' — '+clientName(o.cliente_id))+'</option>').join('');"
new="const usados=new Set(data.vendas.filter(v=>!editingSaleId||v.id!==editingSaleId).map(v=>v.orcamento_id).filter(Boolean));const disponiveis=data.orcamentos.filter(o=>!usados.has(o.id)||o.id===selectedQuote);const quoteOptions='<option value=\"\">Sem orçamento relacionado</option>'+disponiveis.map(o=>'<option value=\"'+esc(o.id)+'\"'+(selectedQuote===o.id?' selected':'')+'>'+esc((o.numero_tiny||'Sem número')+' — '+clientName(o.cliente_id))+(saleByQuote(o.id)&&o.id===selectedQuote?' — venda atual':'')+'</option>').join('');"
if old not in s: raise SystemExit('quoteOptions alvo nao encontrado')
s=s.replace(old,new,1)
old2="formHandler('fv',async p=>{\n   if(!Number.isFinite(Number(p.valor))||Number(p.valor)<0){message('Informe um valor válido.',true);return}\n   const id=editingSaleId;"
new2="formHandler('fv',async p=>{\n   if(!Number.isFinite(Number(p.valor))||Number(p.valor)<0){message('Informe um valor válido.',true);return}\n   if(p.orcamento_id&&data.vendas.some(v=>v.orcamento_id===p.orcamento_id&&v.id!==editingSaleId)){message('Este orçamento já foi convertido em venda e não pode ser utilizado novamente.',true);return}\n   const id=editingSaleId;"
if old2 not in s: raise SystemExit('formHandler venda alvo nao encontrado')
s=s.replace(old2,new2,1)
p.write_text(s,encoding='utf-8')
