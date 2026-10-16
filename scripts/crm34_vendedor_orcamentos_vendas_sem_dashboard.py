from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

# 1) Adicionar vendedor no formulário de orçamentos
old="""<div><label>Produto / categoria</label><input name=\"produto\" value=\"'+val('produto')+'\"></div><div><label>Quantidade</label>"""
new="""<div><label>Produto / categoria</label><input name=\"produto\" value=\"'+val('produto')+'\"></div><div><label>Vendedor</label><input name=\"vendedor\" value=\"'+val('vendedor')+'\" placeholder=\"Nome do vendedor\"></div><div><label>Quantidade</label>"""
if old not in s: raise SystemExit('campo vendedor em orcamentos: alvo nao encontrado')
s=s.replace(old,new,1)

# 2) Adicionar vendedor na tabela de orçamentos
old="""<th>Tiny</th><th>Cliente</th><th>Data do orçamento</th><th>Valor</th><th>Status</th><th>Próximo contato</th><th>Ações</th>"""
new="""<th>Tiny</th><th>Cliente</th><th>Vendedor</th><th>Data do orçamento</th><th>Valor</th><th>Status</th><th>Próximo contato</th><th>Ações</th>"""
if old not in s: raise SystemExit('cabecalho orcamentos: alvo nao encontrado')
s=s.replace(old,new,1)
old="""'<tr><td>'+esc(o.numero_tiny)+'</td><td>'+esc(clientName(o.cliente_id))+'</td><td>'+day(o.data_orcamento)+'</td><td>'+money(o.valor)+'</td>"""
new="""'<tr><td>'+esc(o.numero_tiny)+'</td><td>'+esc(clientName(o.cliente_id))+'</td><td>'+esc(o.vendedor||'—')+'</td><td>'+day(o.data_orcamento)+'</td><td>'+money(o.valor)+'</td>"""
if old not in s: raise SystemExit('linha orcamentos: alvo nao encontrado')
s=s.replace(old,new,1)
s=s.replace('<tr><td colspan="7" class="muted">Nenhum orçamento encontrado com os filtros atuais.</td></tr>','<tr><td colspan="8" class="muted">Nenhum orçamento encontrado com os filtros atuais.</td></tr>',1)

# 3) Remover painel Vendas por vendedor do dashboard, preservando dados por vendedor nas abas
start=s.find(" const vendedorMap=new Map();")
end=s.find(" const vendedorPainel=", start)
if start!=-1 and end!=-1:
    panel_end=s.find(";\n", end)
    if panel_end==-1: raise SystemExit('fim painel vendedor nao encontrado')
    s=s[:start]+s[panel_end+2:]

s=s.replace("+'</div>'+vendedorPainel+", "+'</div>'+",1)

p.write_text(s,encoding='utf-8')
# trigger
