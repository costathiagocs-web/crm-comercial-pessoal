from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
css='''\n/* CRM 3.4 • filtro mensal do dashboard */\n.dashboard-filter{display:flex;align-items:end;gap:10px;flex-wrap:wrap;margin-bottom:14px}.dashboard-filter>div{min-width:220px}.dashboard-filter label{margin-top:0}.dashboard-filter .muted{margin:0 0 2px}.dashboard-periodo{font-weight:750;color:#fff}\n'''
if 'CRM 3.4 • filtro mensal do dashboard' not in s:
    s=s.replace('</style>',css+'\n</style>',1)
js=r'''

/* CRM 3.4 • Dashboard por mês */
let dashboardMonth=today().slice(0,7);
function dashboardMonths(){
 const set=new Set([today().slice(0,7)]);
 data.orcamentos.forEach(o=>{if(o.data_orcamento)set.add(String(o.data_orcamento).slice(0,7))});
 data.vendas.forEach(v=>{if(v.data_venda)set.add(String(v.data_venda).slice(0,7))});
 return [...set].filter(Boolean).sort().reverse();
}
function dashboardMonthLabel(v){if(v==='todos')return 'Todos os períodos';const [y,m]=String(v).split('-').map(Number);return new Date(y,m-1,1).toLocaleDateString('pt-BR',{month:'long',year:'numeric'})}
function dashboardScope(){
 const allSoldIds=new Set(data.vendas.map(v=>v.orcamento_id).filter(Boolean));
 const q=dashboardMonth==='todos'?data.orcamentos:data.orcamentos.filter(o=>String(o.data_orcamento||'').slice(0,7)===dashboardMonth);
 const v=dashboardMonth==='todos'?data.vendas:data.vendas.filter(x=>String(x.data_venda||'').slice(0,7)===dashboardMonth);
 const open=q.filter(o=>['pendente','negociacao'].includes(o.status)&&!allSoldIds.has(o.id));
 const overdue=open.filter(o=>o.proximo_contato&&o.proximo_contato<today());
 const old=open.filter(o=>days(o.data_orcamento)>=5&&!data.acompanhamentos.some(a=>a.orcamento_id===o.id));
 const approved=q.filter(o=>o.status==='aprovado'||allSoldIds.has(o.id));
 const lost=q.filter(o=>o.status==='perdido'&&!allSoldIds.has(o.id));
 return {q,v,open,overdue,old,approved,lost,allSoldIds};
}
renderDashboard=function(){
 const d=dashboardScope(),q=d.q,v=d.v,sum=v.reduce((s,x)=>s+Number(x.valor||0),0),quoted=q.reduce((s,x)=>s+Number(x.valor||0),0),rate=q.length?100*d.approved.length/q.length:0;
 const ranked=d.open.map(o=>({...o,_p:priorityScore(o)})).sort((a,b)=>b._p.score-a._p.score||Number(b.valor)-Number(a.valor));
 const notes=[];if(d.overdue.length)notes.push('Prioridade alta: '+d.overdue.length+' orçamento(s) com retorno vencido.');if(d.old.length)notes.push(d.old.length+' proposta(s) com pelo menos cinco dias e sem acompanhamento registrado.');if(d.lost.length)notes.push('Analise os motivos de perda em '+d.lost.length+' orçamento(s) no período.');if(!notes.length)notes.push('Nenhum alerta relevante identificado no período selecionado.');
 const months=dashboardMonths(),options='<option value="todos">Todos os períodos</option>'+months.map(m=>'<option value="'+m+'"'+(dashboardMonth===m?' selected':'')+'>'+esc(dashboardMonthLabel(m))+'</option>').join('');
 const high=ranked.filter(o=>o._p.score>=50).length;
 const missing=d.open.filter(o=>!o.proximo_contato&&!o.ultimo_contato&&!quoteContact(o)).length;
 const reasonCounts={};for(const o of d.lost){const k=o.motivo_perda_categoria||'não informado';reasonCounts[k]=(reasonCounts[k]||0)+1}const reasons=Object.entries(reasonCounts).sort((a,b)=>b[1]-a[1]).map(([k,n])=>esc(k)+': '+n).join('; ')||'Nenhuma perda registrada';
 const valid=q.filter(o=>o.custo_estimado!==null&&o.custo_estimado!==undefined&&o.custo_estimado!==''&&Number.isFinite(Number(o.custo_estimado))&&Number(o.valor)>0),issues=valid.filter(o=>Number(o.custo_estimado)>Number(o.valor)),gross=valid.reduce((s,o)=>s+Number(o.valor)-Number(o.custo_estimado),0),sales=valid.reduce((s,o)=>s+Number(o.valor),0),margin=sales?gross/sales*100:null;
 $('dashboard').innerHTML='<div class="card"><div class="dashboard-filter"><div><label for="dashboardMonth">Mês de referência</label><select id="dashboardMonth">'+options+'</select></div><button type="button" id="dashboardCurrent">Mês atual</button><button type="button" class="secondary" id="dashboardAll">Todos os períodos</button><p class="muted">Exibindo: <span class="dashboard-periodo">'+esc(dashboardMonthLabel(dashboardMonth))+'</span></p></div></div>'+
 '<div class="grid">'+kpi('Orçamentos',q.length)+kpi('Valor orçado',money(quoted))+kpi('Pedidos de venda',v.length)+kpi('Valor vendido',money(sum))+kpi('Aproveitamento',rate.toFixed(1).replace('.',',')+'%')+kpi('Ticket médio',money(v.length?sum/v.length:0))+kpi('Em aberto',d.open.length)+kpi('Retornos atrasados',d.overdue.length)+'</div>'+
 '<div class="card"><h2>Diagnóstico comercial 3.4</h2><p class="assistantnote">Indicadores calculados para '+esc(dashboardMonthLabel(dashboardMonth))+'. Vendas vinculadas em qualquer data continuam encerrando o orçamento correspondente.</p><p><b>'+high+'</b> oportunidade(s) com prioridade alta; <b>'+d.lost.length+'</b> orçamento(s) perdido(s).</p><p>'+esc(q.length<10?'Amostra pequena: evite tirar conclusões sobre tendências de conversão.':'Registre os motivos de perda para identificar padrões confiáveis.')+'</p><button type="button" id="goAssistant">Abrir assistente e recomendações</button></div>'+
 '<div class="card"><h2>Assistente comercial • análise automática</h2><p class="muted">Alertas do período selecionado.</p>'+notes.map(n=>'<div class="item">• '+esc(n)+'</div>').join('')+'</div>'+
 '<div class="card"><h2>Oportunidades prioritárias</h2>'+(!ranked.length?'<p>Nenhum orçamento em aberto no período.</p>':ranked.slice(0,8).map(o=>'<div class="item"><b>'+esc(clientName(o.cliente_id))+'</b> — '+money(o.valor)+' • '+esc(o.status)+' • Próximo contato: '+day(o.proximo_contato)+'</div>').join(''))+'</div>'+
 '<div class="card"><h2>Alertas e perdas • CRM 3.4</h2><p><b>'+d.overdue.length+'</b> retorno(s) vencido(s); <b>'+missing+'</b> proposta(s) abertas sem data de retorno ou contato registrado.</p><p><b>Motivos de perda:</b> '+reasons+'.</p><p class="assistantnote">Contagens referentes ao período selecionado.</p></div>'+
 '<div class="card"><h2>Rentabilidade estimada • CRM 3.4</h2><div class="grid">'+kpi('Com custo informado',valid.length)+kpi('Sem custo comparável',q.length-valid.length)+kpi('Diferença preço − custo',money(gross))+kpi('Margem estimada agregada',margin===null?'Sem base':margin.toFixed(1).replace('.',',')+'%')+'</div><p class="assistantnote">Cálculo sobre os orçamentos do período selecionado com preço positivo e custo preenchido. Não representa lucro líquido realizado.</p>'+(issues.length?'<div class="notice"><b>Atenção:</b> '+issues.length+' orçamento(s) com custo maior que preço.</div>':'<p class="good">Nenhum custo superior ao preço entre os registros comparáveis.</p>')+'</div>';
 $('dashboardMonth').value=dashboardMonth;$('dashboardMonth').onchange=e=>{dashboardMonth=e.target.value;renderDashboard()};
 $('dashboardCurrent').onclick=()=>{dashboardMonth=today().slice(0,7);renderDashboard()};$('dashboardAll').onclick=()=>{dashboardMonth='todos';renderDashboard()};$('goAssistant').onclick=()=>show('assistente');
};
'''
if 'CRM 3.4 • Dashboard por mês' not in s:
    s=s.replace('</script>',js+'\n</script>',1)
for x in ['dashboardMonth','dashboardScope','Mês de referência','Todos os períodos']:
    if x not in s: raise SystemExit('falha: '+x)
p.write_text(s,encoding='utf-8')
