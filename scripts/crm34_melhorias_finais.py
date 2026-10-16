from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

css='''
/* CRM 3.4 • melhorias finais */
.brand-wrap{display:flex;align-items:center;gap:14px;min-width:0}
.brand-logo{display:none;height:48px;max-width:210px;width:auto;object-fit:contain;border-radius:8px;box-shadow:0 3px 12px #0003}
.brand-copy{min-width:0}
header h1:before{display:none!important}
.sale-badge{display:inline-block;margin-top:6px;padding:4px 7px;border-radius:999px;background:#173f2a;color:#7ee3a5;border:1px solid #2d7047;font-size:11px;font-weight:750}
.sale-actions{display:flex;gap:7px;flex-wrap:wrap}
@media(max-width:720px){.brand-logo{height:38px;max-width:145px}.brand-wrap{gap:9px}}
'''
if 'CRM 3.4 • melhorias finais' not in s:
    s=s.replace('</style>',css+'\n</style>',1)

old_header='<header><div><h1>CRM Comercial</h1><small>Eletro Quadros + Stampo • Gestão comercial multiempresa</small></div><div id="who"></div></header>'
new_header='<header><div class="brand-wrap"><img id="brandLogo" class="brand-logo" alt=""><div class="brand-copy"><h1>CRM Comercial</h1><small>Eletro Quadros + Stampo • Gestão comercial multiempresa</small></div></div><div id="who"></div></header>'
if old_header in s:
    s=s.replace(old_header,new_header,1)
elif 'id="brandLogo"' not in s:
    raise SystemExit('cabecalho alvo nao encontrado')

state="let generatedReportText='',reportNeedsGeneration=true;"
if 'let editingSaleId=null;' not in s:
    s=s.replace(state,state+"\nlet editingSaleId=null;",1)

empresa="function empresaNome(){return empresas.find(e=>e.id===empresaAtual)?.nome||'Selecione uma empresa'}"
marca=empresa+"\nfunction atualizarMarcaEmpresa(){const img=$('brandLogo');if(!img)return;const nome=empresaNome().toLowerCase(),stampo=nome.includes('stampo');img.src=stampo?'assets/logo-stampo.svg':'assets/logo-eletro.svg';img.alt=stampo?'Stampo Metalúrgica':'Eletro Quadros Metalúrgica';img.style.display='block'}"
if 'function atualizarMarcaEmpresa()' not in s:
    s=s.replace(empresa,marca,1)

needle="function cabecalhoEmpresa(){\n const nome=esc(user?.user_metadata?.nome||user?.email?.split('@')[0]||'Administrador');"
repl="function cabecalhoEmpresa(){\n atualizarMarcaEmpresa();\n const nome=esc(user?.user_metadata?.nome||user?.email?.split('@')[0]||'Administrador');"
if needle in s:
    s=s.replace(needle,repl,1)

s=s.replace("empresaAtual=id;editingClientId=null;clientSearch='';editingQuoteId=null;quoteFilters={search:'',status:'todos'};","empresaAtual=id;editingClientId=null;clientSearch='';editingQuoteId=null;editingSaleId=null;quoteFilters={search:'',status:'todos'};",1)

helper_old="function clientName(id){return data.clientes.find(c=>c.id===id)?.empresa||'Cliente não encontrado'}function opts(arr,label){return arr.map(x=>'<option value=\"'+esc(x.id)+'\">'+esc(label(x))+'</option>').join('')}"
helper_new="function clientName(id){return data.clientes.find(c=>c.id===id)?.empresa||'Cliente não encontrado'}function saleByQuote(id){return data.vendas.find(v=>v.orcamento_id===id)}function opts(arr,label){return arr.map(x=>'<option value=\"'+esc(x.id)+'\">'+esc(label(x))+'</option>').join('')}"
if 'function saleByQuote(id)' not in s:
    if helper_old not in s: raise SystemExit('helper alvo nao encontrado')
    s=s.replace(helper_old,helper_new,1)

old_status='<td><span class="pill">'+esc(o.status)+'</span></td>'
new_status='<td><span class="pill">'+esc(o.status)+'</span>'+(saleByQuote(o.id)?'<div class="sale-badge">✓ Venda realizada'+(saleByQuote(o.id).numero_pedido_tiny?' • Pedido '+esc(saleByQuote(o.id).numero_pedido_tiny):'')+'</div>':'')+'</td>'
if old_status in s:
    s=s.replace(old_status,new_status,1)

start=s.find('function renderSales(){')
end=s.find('\nfunction renderFollowups(){',start)
if start<0 or end<0:
    raise SystemExit('renderSales nao encontrado')

new_sales=r'''function renderSales(){
 const current=data.vendas.find(v=>v.id===editingSaleId);if(editingSaleId&&!current)editingSaleId=null;
 const selectedQuote=current?.orcamento_id||'';
 const val=k=>esc(current?.[k]??'');
 const quoteOptions='<option value="">Sem orçamento relacionado</option>'+data.orcamentos.map(o=>'<option value="'+esc(o.id)+'"'+(selectedQuote===o.id?' selected':'')+'>'+esc((o.numero_tiny||'Sem número')+' — '+clientName(o.cliente_id))+'</option>').join('');
 $('vendas').innerHTML='<div class="card" id="saleEditor"><h2>'+(current?'Editar pedido de venda':'Novo pedido de venda')+'</h2><p class="muted">Ao selecionar um orçamento, o valor é preenchido automaticamente. Ao salvar uma venda vinculada, o orçamento é marcado como aprovado.</p><form id="fv"><div class="formgrid"><div><label>Orçamento relacionado (opcional)</label><select name="orcamento_id" id="saleQuote">'+quoteOptions+'</select></div><div><label>Número do pedido Tiny</label><input name="numero_pedido_tiny" value="'+val('numero_pedido_tiny')+'"></div><div><label>Data da venda</label><input name="data_venda" type="date" value="'+(current?val('data_venda'):today())+'" required></div><div><label>Valor em R$</label><input name="valor" id="saleValue" type="number" min="0" step="0.01" value="'+val('valor')+'" required></div></div><label>Observações</label><textarea name="observacoes">'+esc(current?.observacoes??'')+'</textarea><div class="formactions"><button>'+(current?'Salvar alterações':'Salvar venda')+'</button>'+(current?'<button type="button" class="secondary" id="cancelSale">Cancelar edição</button>':'')+'</div></form></div><div class="card"><h2>Pedidos realizados</h2><div class="tablewrap"><table><thead><tr><th>Pedido Tiny</th><th>Data</th><th>Cliente</th><th>Valor</th><th>Orçamento</th><th>Ações</th></tr></thead><tbody>'+(!data.vendas.length?'<tr><td colspan="6" class="muted">Nenhuma venda registrada.</td></tr>':data.vendas.map(v=>{const o=data.orcamentos.find(x=>x.id===v.orcamento_id);return '<tr><td>'+esc(v.numero_pedido_tiny)+'</td><td>'+day(v.data_venda)+'</td><td>'+esc(o?clientName(o.cliente_id):'—')+'</td><td>'+money(v.valor)+'</td><td>'+esc(o?.numero_tiny||'—')+'</td><td><div class="sale-actions"><button type="button" class="secondary" data-edit-sale="'+esc(v.id)+'">Editar</button><button type="button" class="danger" data-delete-sale="'+esc(v.id)+'">Excluir</button></div></td></tr>'}).join(''))+'</tbody></table></div></div>';
 const preencherValor=()=>{const id=$('saleQuote').value;if(!id){if(!current)$('saleValue').value='';return}const o=data.orcamentos.find(x=>x.id===id);if(o&&o.valor!==null&&o.valor!==undefined)$('saleValue').value=Number(o.valor).toFixed(2)};
 $('saleQuote').onchange=preencherValor;
 if(!current&&$('saleQuote').value)preencherValor();
 formHandler('fv',async p=>{
   if(!Number.isFinite(Number(p.valor))||Number(p.valor)<0){message('Informe um valor válido.',true);return}
   const id=editingSaleId;
   const result=id?await sb.from('vendas').update(p).eq('id',id).eq('usuario_id',user.id).eq('empresa_id',empresaAtual):await sb.from('vendas').insert({...p,usuario_id:user.id,empresa_id:empresaAtual});
   if(result.error){message('Erro ao salvar venda: '+result.error.message,true);return}
   if(p.orcamento_id){
     const up=await sb.from('orcamentos').update({status:'aprovado'}).eq('id',p.orcamento_id).eq('usuario_id',user.id).eq('empresa_id',empresaAtual);
     if(up.error){message('Venda salva, mas não foi possível marcar o orçamento como aprovado: '+up.error.message,true);editingSaleId=null;reportNeedsGeneration=true;await refresh();return}
   }
   editingSaleId=null;reportNeedsGeneration=true;message(id?'Venda atualizada e orçamento sincronizado':'Venda cadastrada e orçamento aprovado');await refresh()
 });
 if(current)$('cancelSale').onclick=()=>{editingSaleId=null;renderSales()};
 document.querySelectorAll('[data-edit-sale]').forEach(el=>el.onclick=()=>{editingSaleId=el.dataset.editSale;renderSales();document.getElementById('saleEditor').scrollIntoView({behavior:'smooth',block:'start'})});
 document.querySelectorAll('[data-delete-sale]').forEach(el=>el.onclick=async()=>{const id=el.dataset.deleteSale,v=data.vendas.find(x=>x.id===id);if(!v)return;if(!confirm('Excluir a venda '+(v.numero_pedido_tiny||'sem número')+' no valor de '+money(v.valor)+'? O orçamento relacionado permanecerá aprovado e poderá ser ajustado manualmente, se necessário.'))return;el.disabled=true;const {error}=await sb.from('vendas').delete().eq('id',id).eq('usuario_id',user.id).eq('empresa_id',empresaAtual);if(error){message('Não foi possível excluir a venda: '+error.message,true);el.disabled=false;return}if(editingSaleId===id)editingSaleId=null;reportNeedsGeneration=true;message('Venda excluída');await refresh()});
}'''

s=s[:start]+new_sales+s[end:]

for required in ['function atualizarMarcaEmpresa()','let editingSaleId=null','data-edit-sale','data-delete-sale',"status:'aprovado'",'Venda realizada','assets/logo-stampo.svg']:
    if required not in s:
        raise SystemExit('validacao falhou: '+required)

p.write_text(s,encoding='utf-8')
