from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
start=s.find('function reportText(){')
end=s.find('\nfunction renderReport(){', start)
if start < 0 or end < 0:
    raise SystemExit('reportText nao encontrado')

new_report=r'''function reportText(){
 const end=new Date(today()+'T12:00:00'),start=new Date(end);start.setDate(end.getDate()-6);const future=new Date(end);future.setDate(end.getDate()+6);
 const d0=start.toLocaleDateString('en-CA'),d1=today(),d2=future.toLocaleDateString('en-CA');
 const q=data.orcamentos.filter(o=>o.data_orcamento>=d0&&o.data_orcamento<=d1),v=data.vendas.filter(o=>o.data_venda>=d0&&o.data_venda<=d1);
 const open=data.orcamentos.filter(o=>['pendente','negociacao'].includes(o.status));
 const approved=q.filter(o=>o.status==='aprovado'),lost=q.filter(o=>o.status==='perdido');
 const overdue=open.filter(o=>o.proximo_contato&&o.proximo_contato<d1);
 const todayContacts=open.filter(o=>o.proximo_contato===d1);
 const next=open.filter(o=>o.proximo_contato&&o.proximo_contato>d1&&o.proximo_contato<=d2).sort((a,b)=>String(a.proximo_contato).localeCompare(String(b.proximo_contato)));
 const without=open.filter(o=>!o.proximo_contato);
 const openValue=open.reduce((s,o)=>s+Number(o.valor||0),0),overdueValue=overdue.reduce((s,o)=>s+Number(o.valor||0),0);
 const weekQuoted=q.reduce((s,o)=>s+Number(o.valor||0),0),weekSold=v.reduce((s,o)=>s+Number(o.valor||0),0);
 const win=q.length?approved.length/q.length*100:0,a=analysis();
 const priority=[...open].sort((x,y)=>Number(!!y.proximo_contato&&y.proximo_contato<d1)-Number(!!x.proximo_contato&&x.proximo_contato<d1)||Number(y.valor||0)-Number(x.valor||0)).slice(0,8);
 const agenda=next.slice(0,8).map(o=>'• '+day(o.proximo_contato)+' — '+clientName(o.cliente_id)+' — '+(o.numero_tiny||'sem número')+' — '+money(o.valor)).join('\n');
 const priorities=priority.map(o=>'• '+clientName(o.cliente_id)+' — '+(o.numero_tiny||'sem número')+' — '+money(o.valor)+' — '+(o.proximo_contato?'próximo contato '+day(o.proximo_contato):'sem próximo contato')).join('\n');

 const clientMap=new Map();
 const touch=id=>{if(!clientMap.has(id))clientMap.set(id,{id,nome:clientName(id),orcamentos:0,valorOrcado:0,vendas:0,valorVendido:0,aprovados:0});return clientMap.get(id)};
 q.forEach(o=>{const c=touch(o.cliente_id);c.orcamentos++;c.valorOrcado+=Number(o.valor||0);if(o.status==='aprovado')c.aprovados++});
 const quoteById=new Map(data.orcamentos.map(o=>[o.id,o]));
 let vendasSemOrcamento=0,valorVendasSemOrcamento=0;
 v.forEach(x=>{const o=quoteById.get(x.orcamento_id);if(o?.cliente_id){const c=touch(o.cliente_id);c.vendas++;c.valorVendido+=Number(x.valor||0)}else{vendasSemOrcamento++;valorVendasSemOrcamento+=Number(x.valor||0)}});
 const clientes=[...clientMap.values()].sort((a,b)=>b.valorOrcado-a.valorOrcado||b.valorVendido-a.valorVendido||a.nome.localeCompare(b.nome,'pt-BR'));
 const clientesTexto=clientes.length?clientes.map(c=>'• '+c.nome+' — '+c.orcamentos+' orçamento(s), total '+money(c.valorOrcado)+' | '+c.vendas+' venda(s), total '+money(c.valorVendido)+' | '+c.aprovados+' orçamento(s) aprovado(s)').join('\n'):'Nenhum orçamento ou venda no período.';
 const semVinculo=vendasSemOrcamento?'\n• Pedidos sem orçamento vinculado: '+vendasSemOrcamento+' | '+money(valorVendasSemOrcamento):'';

 return 'RELATÓRIO SEMANAL — '+empresaNome()+' — '+day(d0)+' a '+day(d1)+'\n\n'+
 'RESUMO DA SEMANA\n'+
 'Orçamentos incluídos: '+q.length+' | Valor orçado: '+money(weekQuoted)+'\n'+
 'Pedidos fechados: '+v.length+' | Valor vendido: '+money(weekSold)+'\n'+
 'Aprovados entre os orçamentos da semana: '+approved.length+'\n'+
 'Perdidos entre os orçamentos da semana: '+lost.length+'\n'+
 'Taxa de aproveitamento das propostas incluídas na semana (status atual): '+win.toFixed(1).replace('.',',')+'%\n\n'+
 'DESEMPENHO POR CLIENTE\n'+clientesTexto+semVinculo+'\n\n'+
 'CARTEIRA EM ABERTO\n'+
 'Orçamentos pendentes/em negociação: '+open.length+' | Valor em aberto: '+money(openValue)+'\n'+
 'Retornos vencidos: '+overdue.length+' | Valor: '+money(overdueValue)+'\n'+
 'Próximo contato hoje: '+todayContacts.length+'\n'+
 'Sem próximo contato definido: '+without.length+'\n'+
 'Próximos contatos em até 7 dias: '+next.length+(agenda?'\n'+agenda:'')+'\n\n'+
 'PRIORIDADES DE ACOMPANHAMENTO\n'+(priorities||'Nenhuma oportunidade em aberto.')+'\n\n'+
 'AÇÕES RECOMENDADAS\n'+a.notes.map((n,i)=>(i+1)+'. '+n).join('\n')+'\n\n'+
 'Observação: o bloco por cliente considera os orçamentos incluídos no período e as vendas registradas no mesmo período, vinculando cada venda ao cliente pelo orçamento relacionado. O relatório usa os dados cadastrados no CRM no momento em que você clica em “Gerar relatório”.'
}'''

s=s[:start]+new_report+s[end:]
for required in ['DESEMPENHO POR CLIENTE','orçamento(s), total','venda(s), total','Aprovados entre os orçamentos da semana']:
    if required not in s:
        raise SystemExit('Validacao falhou: '+required)
p.write_text(s,encoding='utf-8')

# disparo controlado
