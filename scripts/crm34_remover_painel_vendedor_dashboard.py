from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')
# Remove bloco de cálculo do painel de vendedor, se ainda existir
s=re.sub(r"\n\s*const vendedorMap=new Map\(\);.*?const vendedorPainel=.*?;\n", "\n", s, count=1, flags=re.S)
# Remove concatenação do painel do HTML do dashboard
s=s.replace("+'</div>'+vendedorPainel+", "+'</div>'+", 1)
s=s.replace("+'</div>'+ vendedorPainel+", "+'</div>'+", 1)
if 'Vendas por vendedor' in s:
    raise SystemExit('painel Vendas por vendedor ainda presente')
p.write_text(s,encoding='utf-8')
