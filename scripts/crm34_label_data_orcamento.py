from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='<div><label>Data *</label><input name="data_orcamento" type="date"'
new='<div><label>Data do orçamento *</label><input name="data_orcamento" type="date"'
if old not in s: raise SystemExit('Rotulo de data nao encontrado')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
