from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

state_old = "let editingQuoteId=null;"
state_new = "let editingQuoteId=null;\nlet quoteFilters={search:'',status:'todos',start:'',end:''};"
if state_old not in s:
    raise SystemExit('Estado de orcamentos nao encontrado')
s = s.replace(state_old, state_new, 1)

switch_old = "editingClientId=null;clientSearch='';editingQuoteId=null;history33Records={orcamentos:[],vendas:[]};"
switch_new = "editingClientId=null;clientSearch='';editingQuoteId=null;quoteFilters={search:'',status:'todos',start:'',end:''};history33Records={orcamentos:[],vendas:[]};"
if switch_old not in s:
    raise SystemExit('Trecho de troca de empresa nao encontrado')
s = s.replace(switch_old, switch_new, 1)

start = s.find('function renderQuotes(){')
end = s.find('\nfunction renderSales(){', start)
if start < 0 or end < 0:
    raise SystemExit('Bloco renderQuotes nao encontrado')

new_block = r'''function quoteSearchText(v){return String(v??'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase()}
function filteredQuotes(){const f=quoteFilters,term=quoteSearchText(f.search.trim());return data.orcamentos.filter(o=>{if(f.status!=='todos'&&o.status!==f.status)return false;if(f.start&&String(o.data_orcamento||'')<f.start)return false;if(f.end&&String(o.data_orcamento||'')>f.end)return false;if(term&&!([clientName(o.cliente_id),o.numero_tiny,o.produto,o.status,o.concorrente,o.motivo_perda].some(v=>quoteSearchText(v).includes(term))))return false;return true})}
function renderQuotes(){const current=data.orcamentos.find(o=>o.id===editingQuoteId);if(editingQuoteId&&!current)editingQuoteId=null;const filtered=filteredQuotes(),f=quoteFilters;
$('orcamentos').innerHTML='<div class="card" id="quoteEditor"><h2>'+(current?'Editar orçamento':'Novo orçamento')+'</h2>'+(!data.clientes.length?'<div class="notice">Cadastre um cliente primeiro.</div>':'')+'<form id="fq">'+quoteFormFields(current)+'<div class="formactions"><button '+(!data.clientes.length?'disabled':'')+'>'+(current?'Salvar alterações':'Salvar orçamento')+'</button>'+(current?'<button type="button" class="secondary" id="cancelQuote">Cancelar edição</button>':'')+'</div></form></div><div class="card"><div class="row"><div><h2 style="margin-bottom:4px">Orçamentos ('+data.orcamentos.length+')</h2><p class="muted" style="margin:0">Exibindo '+filtered.length+' registro(s) da empresa ativa.</p></div></div><div class="formgrid"><div><label for="quoteSearch">Pesquisar</label><input id="quoteSearch" value="'+esc(f.search)+'" placeholder="Cliente, número Tiny, produto..."></div><div><label for="quoteStatus">Situação</label><select id="quoteStatus"><option value="todos">Todas</option><option value="pendente">Pendente</option><option value="negociacao">Em negociação</option><option value="aprovado">Aprovado</option><option value="perdido">Perdido</option></select></div><div><label for="quoteStart">Data inicial</label><input id="quoteStart" type="date" value="'+esc(f.start)+'"></div><div><label for="quoteEnd">Data final</label><input id="quoteEnd" type="date" value="'+esc(f.end)+'"></div></div><div class="formactions"><button type="button" class="secondary" id="clearQuoteFilters">Limpar filtros</button></div><div class="tablewrap"><table><thead><tr><th>Tiny</th><th>Cliente</th><th>Data</th><th>Valor</th><th>Status</th><th>Retorno</th><th>Ações</th></tr></thead><tbody>'+(!filtered.length?'<tr><td colspan="7" class="muted">Nenhum orçamento encontrado com os filtros atuais.</td></tr>':filtered.map(o=>'<tr><td>'+esc(o.numero_tiny)+'</td><td>'+esc(clientName(o.cliente_id))+'</td><td>'+day(o.data_orcamento)+'</td><td>'+money(o.valor)+'</td><td><span class="pill">'+esc(o.status)+'</span></td><td>'+day(o.proximo_contato)+'</td><td><div class="formactions"><button type="button" class="secondary" data-edit-quote="'+esc(o.id)+'">Editar</button><button type="button" class="secondary" data-delete-quote="'+esc(o.id)+'">Excluir</button></div></td></tr>').join(''))+'</tbody></table></div></div>';
formHandler('fq',async p=>{if(!Number.isFinite(Number(p.valor))||Number(p.valor)<0){message('Informe um valor válido.',true);return}const id=editingQuoteId;let result=id?await sb.from('orcamentos').update(p).eq('id',id).eq('usuario_id',user.id).eq('empresa_id',empresaAtual):await sb.from('orcamentos').insert({...p,usuario_id:user.id,empresa_id:empresaAtual});if(result.error){message('Erro ao salvar orçamento: '+result.error.message,true);return}editingQuoteId=null;message(id?'Orçamento atualizado':'Orçamento cadastrado');await refresh()});
if(current)$('cancelQuote').onclick=()=>{editingQuoteId=null;renderQuotes()};
$('quoteStatus').value=f.status;
$('quoteSearch').oninput=ev=>{quoteFilters.search=ev.target.value;renderQuotes();const campo=$('quoteSearch');campo.focus();campo.setSelectionRange(campo.value.length,campo.value.length)};
$('quoteStatus').onchange=ev=>{quoteFilters.status=ev.target.value;renderQuotes()};
$('quoteStart').onchange=ev=>{quoteFilters.start=ev.target.value;renderQuotes()};
$('quoteEnd').onchange=ev=>{quoteFilters.end=ev.target.value;renderQuotes()};
$('clearQuoteFilters').onclick=()=>{quoteFilters={search:'',status:'todos',start:'',end:''};renderQuotes()};
document.querySelectorAll('[data-edit-quote]').forEach(el=>el.onclick=()=>{editingQuoteId=el.dataset.editQuote;renderQuotes();document.getElementById('quoteEditor').scrollIntoView({behavior:'smooth',block:'start'})});
document.querySelectorAll('[data-delete-quote]').forEach(el=>el.onclick=async()=>{const id=el.dataset.deleteQuote,o=data.orcamentos.find(x=>x.id===id);if(!o)return;const nv=data.vendas.filter(x=>x.orcamento_id===id).length,na=data.acompanhamentos.filter(x=>x.orcamento_id===id).length;if(nv||na){message('Não é possível excluir: orçamento vinculado a '+nv+' venda(s) e '+na+' acompanhamento(s). Preserve o histórico ou resolva os vínculos primeiro.',true);return}if(!confirm('Excluir definitivamente o orçamento '+(o.numero_tiny||'sem número')+' de '+clientName(o.cliente_id)+' no valor de '+money(o.valor)+'? Esta ação não pode ser desfeita.'))return;el.disabled=true;const {error}=await sb.from('orcamentos').delete().eq('id',id).eq('usuario_id',user.id).eq('empresa_id',empresaAtual);if(error){message('Não foi possível excluir: '+error.message,true);el.disabled=false;return}if(editingQuoteId===id)editingQuoteId=null;message('Orçamento excluído');await refresh()})}'''

s = s[:start] + new_block + s[end:]

for required in ['quoteFilters','filteredQuotes','quoteSearch','quoteStatus','quoteStart','quoteEnd','clearQuoteFilters']:
    if required not in s:
        raise SystemExit('Validacao falhou: '+required)

p.write_text(s, encoding='utf-8')

# Trigger controlado do workflow temporario.
