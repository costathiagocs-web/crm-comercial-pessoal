from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

# 1) Campo vendedor no formulário de vendas
old='''<div><label>Número do pedido Tiny</label><input name="numero_pedido_tiny" value="'+val('numero_pedido_tiny')+'"></div><div><label>Data da venda</label>'''
new='''<div><label>Número do pedido Tiny</label><input name="numero_pedido_tiny" value="'+val('numero_pedido_tiny')+'"></div><div><label>Vendedor</label><input name="vendedor" value="'+val('vendedor')+'" placeholder="Nome do vendedor"></div><div><label>Data da venda</label>'''
if old not in s: raise SystemExit('form vendas alvo nao encontrado')
s=s.replace(old,new,1)

# 2) Coluna vendedor na listagem de vendas
old='''<th>Pedido Tiny</th><th>Data</th><th>Cliente</th><th>Valor</th><th>Orçamento</th><th>Ações</th>'''
new='''<th>Pedido Tiny</th><th>Data</th><th>Cliente</th><th>Vendedor</th><th>Valor</th><th>Orçamento</th><th>Ações</th>'''
if old not in s: raise SystemExit('cabecalho vendas alvo nao encontrado')
s=s.replace(old,new,1)

old="""'<tr><td>'+esc(v.numero_pedido_tiny)+'</td><td>'+day(v.data_venda)+'</td><td>'+esc(o?clientName(o.cliente_id):'—')+'</td><td>'+money(v.valor)+'</td><td>'+esc(o?.numero_tiny||'—')+'</td><td><div class=\"sale-actions\">"""
new="""'<tr><td>'+esc(v.numero_pedido_tiny)+'</td><td>'+day(v.data_venda)+'</td><td>'+esc(o?clientName(o.cliente_id):'—')+'</td><td>'+esc(v.vendedor||'—')+'</td><td>'+money(v.valor)+'</td><td>'+esc(o?.numero_tiny||'—')+'</td><td><div class=\"sale-actions\">"""
if old not in s: raise SystemExit('linha vendas alvo nao encontrado')
s=s.replace(old,new,1)
s=s.replace("<tr><td colspan=\"6\" class=\"muted\">Nenhuma venda registrada.</td></tr>","<tr><td colspan=\"7\" class=\"muted\">Nenhuma venda registrada.</td></tr>",1)

# 3) Painel por vendedor no dashboard mensal
needle="""const valid=q.filter(o=>o.custo_estimado!==null&&o.custo_estimado!==undefined&&o.custo_estimado!==''&&Number.isFinite(Number(o.custo_estimado))&&Number(o.valor)>0),issues=valid.filter(o=>Number(o.custo_estimado)>Number(o.valor)),gross=valid.reduce((s,o)=>s+Number(o.valor)-Number(o.custo_estimado),0),sales=valid.reduce((s,o)=>s+Number(o.valor),0),margin=sales?gross/sales*100:null;"""
insert=needle+"""
 const vendedorMap=new Map();
 for(const x of v){const nome=String(x.vendedor||'').trim()||'Não informado';const r=vendedorMap.get(nome)||{nome,pedidos:0,valor:0};r.pedidos++;r.valor+=Number(x.valor||0);vendedorMap.set(nome,r)}
 const vendedores=[...vendedorMap.values()].sort((a,b)=>b.valor-a.valor||b.pedidos-a.pedidos||a.nome.localeCompare(b.nome,'pt-BR'));
 const vendedorPainel='<div class=\"card\"><h2>Vendas por vendedor</h2><p class=\"muted\">Desempenho no período selecionado.</p>'+(vendedores.length?'<div class=\"tablewrap\"><table><thead><tr><th>Vendedor</th><th>Pedidos</th><th>Valor vendido</th></tr></thead><tbody>'+vendedores.map(x=>'<tr><td>'+esc(x.nome)+'</td><td>'+x.pedidos+'</td><td>'+money(x.valor)+'</td></tr>').join('')+'</tbody></table></div>':'<p>Nenhuma venda no período selecionado.</p>')+'</div>';
"""
if needle not in s: raise SystemExit('dashboard alvo nao encontrado')
s=s.replace(needle,insert,1)

old="""'<div class=\"grid\">'+kpi('Orçamentos',q.length)+kpi('Valor orçado',money(quoted))+kpi('Pedidos de venda',v.length)+kpi('Valor vendido',money(sum))+kpi('Aproveitamento',rate.toFixed(1).replace('.',',')+'%')+kpi('Ticket médio',money(v.length?sum/v.length:0))+kpi('Em aberto',d.open.length)+kpi('Retornos atrasados',d.overdue.length)+'</div>'+"""
new="""'<div class=\"grid\">'+kpi('Orçamentos',q.length)+kpi('Valor orçado',money(quoted))+kpi('Pedidos de venda',v.length)+kpi('Valor vendido',money(sum))+kpi('Aproveitamento',rate.toFixed(1).replace('.',',')+'%')+kpi('Ticket médio',money(v.length?sum/v.length:0))+kpi('Em aberto',d.open.length)+kpi('Retornos atrasados',d.overdue.length)+'</div>'+vendedorPainel+"""
if old not in s: raise SystemExit('insercao painel vendedor nao encontrada')
s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
# trigger
