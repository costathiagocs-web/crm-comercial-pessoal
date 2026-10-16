from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
start=s.find('function reportText(){')
end=s.find('\nfunction renderReport(){', start)
if start < 0 or end < 0:
    raise SystemExit('reportText nao encontrado')

new_report=r'''function reportText(){
 const end=new Date(today()+'T12:00:00'),start=new Date(end);start.setDate(end.getDate()-6);
 const d0=start.toLocaleDateString('en-CA'),d1=today();
 const q=data.orcamentos.filter(o=>o.data_orcamento>=d0&&o.data_orcamento<=d1),v=data.vendas.filter(o=>o.data_venda>=d0&&o.data_venda<=d1);
 const soldQuoteIds=new Set(data.vendas.map(x=>x.orcamento_id).filter(Boolean));
 const open=data.orcamentos.filter(o=>['pendente','negociacao'].includes(o.status)&&!soldQuoteIds.has(o.id));
 const approved=q.filter(o=>o.status==='aprovado'||soldQuoteIds.has(o.id)),lost=q.filter(o=>o.status==='perdido'&&!soldQuoteIds.has(o.id));
 const openValue=open.reduce((s,o)=>s+Number(o.valor||0),0);
 const weekQuoted=q.reduce((s,o)=>s+Number(o.valor||0),0),weekSold=v.reduce((s,o)=>s+Number(o.valor||0),0);
 const win=q.length?approved.length/q.length*100:0;

 const clientMap=new Map();
 const touch=id=>{if(!clientMap.has(id))clientMap.set(id,{id,nome:clientName(id),orcamentos:0,valorOrcado:0,vendas:0,valorVendido:0,aprovados:0});return clientMap.get(id)};
 q.forEach(o=>{const c=touch(o.cliente_id);c.orcamentos++;c.valorOrcado+=Number(o.valor||0);if(o.status==='aprovado'||soldQuoteIds.has(o.id))c.aprovados++});
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
 'Orçamentos realmente em aberto: '+open.length+' | Valor em aberto: '+money(openValue)+'\n\n'+
 'Observação: a carteira em aberto considera somente orçamentos pendentes ou em negociação que ainda não possuem venda vinculada. Orçamentos com pedido registrado deixam de compor o valor em aberto, mesmo que o status do orçamento ainda não tenha sido alterado manualmente.'
}'''

s=s[:start]+new_report+s[end:]
for required in ['Orçamentos realmente em aberto','soldQuoteIds','DESEMPENHO POR CLIENTE']:
    if required not in s:
        raise SystemExit('Validacao falhou: '+required)
for removed in ['PRIORIDADES DE ACOMPANHAMENTO','Retornos vencidos:','Próximo contato hoje:','Sem próximo contato definido:','Próximos contatos em até 7 dias:']:
    if removed in new_report:
        raise SystemExit('Campo ainda presente: '+removed)
p.write_text(s,encoding='utf-8')

# trigger workflow 2
