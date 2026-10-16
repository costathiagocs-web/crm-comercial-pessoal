from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

state_old = "let empresas=[],empresaAtual=null,carregamentoEmpresa=0;"
state_new = "let empresas=[],empresaAtual=null,carregamentoEmpresa=0;\nlet editingClientId=null,clientSearch='';"
if state_old not in s:
    raise SystemExit('Estado multiempresa nao encontrado')
s = s.replace(state_old, state_new, 1)

switch_old = "$('empresaSelecionada').onchange=async ev=>{const id=ev.target.value;if(!empresas.some(e=>e.id===id))return;empresaAtual=id;editingQuoteId=null;history33Records={orcamentos:[],vendas:[]};history33Request++;chatHistory=[];data={clientes:[],orcamentos:[],vendas:[],acompanhamentos:[]};cabecalhoEmpresa();render();renderHistory33();await refresh()};"
switch_new = "$('empresaSelecionada').onchange=async ev=>{const id=ev.target.value;if(!empresas.some(e=>e.id===id))return;empresaAtual=id;editingClientId=null;clientSearch='';editingQuoteId=null;history33Records={orcamentos:[],vendas:[]};history33Request++;chatHistory=[];data={clientes:[],orcamentos:[],vendas:[],acompanhamentos:[]};cabecalhoEmpresa();render();renderHistory33();await refresh()};"
if switch_old not in s:
    raise SystemExit('Handler de troca de empresa nao encontrado')
s = s.replace(switch_old, switch_new, 1)

start = s.find('function renderClients(){')
end = s.find('\nlet editingQuoteId=null;', start)
if start < 0 or end < 0:
    raise SystemExit('Bloco renderClients nao encontrado')

new_block = r'''function clientSearchText(v){return String(v??'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase()}
function clientFormFields(c){const val=k=>esc(c?.[k]??'');return '<div class="formgrid">'+[['empresa','Empresa *'],['cnpj','CNPJ'],['contato','Pessoa de contato'],['telefone','WhatsApp / telefone'],['email','E-mail'],['cidade','Cidade'],['estado','Estado'],['origem','Origem do cliente']].map(([n,l])=>'<div><label>'+l+'</label><input name="'+n+'" value="'+val(n)+'" '+(n==='empresa'?'required':'')+'></div>').join('')+'</div><label>Observações</label><textarea name="observacoes">'+esc(c?.observacoes??'')+'</textarea>'}
function renderClients(){const current=data.clientes.find(c=>c.id===editingClientId);if(editingClientId&&!current)editingClientId=null;const termo=clientSearchText(clientSearch.trim()),filtered=!termo?data.clientes:data.clientes.filter(c=>[c.empresa,c.cnpj,c.contato,c.telefone,c.email,c.cidade,c.estado,c.origem].some(v=>clientSearchText(v).includes(termo)));$('clientes').innerHTML='<div class="card" id="clientEditor"><h2>'+(current?'Editar cliente':'Novo cliente')+'</h2><form id="fc">'+clientFormFields(current)+'<div class="formactions"><button>'+(current?'Salvar alterações':'Salvar cliente')+'</button>'+(current?'<button type="button" class="secondary" id="cancelClient">Cancelar edição</button>':'')+'</div></form></div><div class="card"><div class="row"><div><h2 style="margin-bottom:4px">Clientes cadastrados ('+data.clientes.length+')</h2><p class="muted" style="margin:0">Exibindo '+filtered.length+' registro(s) da empresa ativa.</p></div><div style="min-width:min(100%,340px);flex:0 1 340px"><label for="clientSearch" style="margin-top:0">Pesquisar clientes</label><input id="clientSearch" value="'+esc(clientSearch)+'" placeholder="Empresa, CNPJ, contato, cidade..."></div></div><div class="tablewrap"><table><thead><tr><th>Empresa</th><th>Contato</th><th>Telefone</th><th>Cidade / UF</th><th>CNPJ</th><th>Ações</th></tr></thead><tbody>'+(!filtered.length?'<tr><td colspan="6" class="muted">Nenhum cliente encontrado.</td></tr>':filtered.map(c=>'<tr><td>'+esc(c.empresa)+'</td><td>'+esc(c.contato)+'</td><td>'+esc(c.telefone)+'</td><td>'+esc([c.cidade,c.estado].filter(Boolean).join(' / '))+'</td><td>'+esc(c.cnpj)+'</td><td><div class="formactions"><button type="button" class="secondary" data-edit-client="'+esc(c.id)+'">Editar</button><button type="button" class="secondary" data-delete-client="'+esc(c.id)+'">Excluir</button></div></td></tr>').join(''))+'</tbody></table></div></div>';
formHandler('fc',async p=>{const id=editingClientId;let result=id?await sb.from('clientes').update(p).eq('id',id).eq('usuario_id',user.id).eq('empresa_id',empresaAtual):await sb.from('clientes').insert({...p,usuario_id:user.id,empresa_id:empresaAtual});if(result.error){message('Erro ao salvar cliente: '+result.error.message,true);return}editingClientId=null;message(id?'Cliente atualizado':'Cliente cadastrado');await refresh()});
if(current)$('cancelClient').onclick=()=>{editingClientId=null;renderClients()};
$('clientSearch').oninput=ev=>{clientSearch=ev.target.value;renderClients();const campo=$('clientSearch');campo.focus();campo.setSelectionRange(campo.value.length,campo.value.length)};
document.querySelectorAll('[data-edit-client]').forEach(el=>el.onclick=()=>{editingClientId=el.dataset.editClient;renderClients();document.getElementById('clientEditor').scrollIntoView({behavior:'smooth',block:'start'})});
document.querySelectorAll('[data-delete-client]').forEach(el=>el.onclick=async()=>{const id=el.dataset.deleteClient,c=data.clientes.find(x=>x.id===id);if(!c)return;const nq=data.orcamentos.filter(o=>o.cliente_id===id).length;if(nq){message('Não é possível excluir: este cliente possui '+nq+' orçamento(s) vinculado(s). Preserve o histórico comercial.',true);return}if(!confirm('Excluir definitivamente o cliente '+c.empresa+'? Esta ação não pode ser desfeita.'))return;el.disabled=true;const {error}=await sb.from('clientes').delete().eq('id',id).eq('usuario_id',user.id).eq('empresa_id',empresaAtual);if(error){message('Não foi possível excluir o cliente: '+error.message,true);el.disabled=false;return}if(editingClientId===id)editingClientId=null;message('Cliente excluído');await refresh()})}'''

s = s[:start] + new_block + s[end:]

for required in ['editingClientId','clientSearchText','data-edit-client','data-delete-client','Preserve o histórico comercial']:
    if required not in s:
        raise SystemExit('Validacao falhou: '+required)

p.write_text(s, encoding='utf-8')
