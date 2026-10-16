from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
s=s.replace('<label for="email">Usuário</label>','<label for="email">E-mail</label>',1)
s=s.replace("<span>Administrador: '+nome+'</span>","<span>Usuário: Comercial</span>",1)
if '<label for="email">E-mail</label>' not in s:
    raise SystemExit('label e-mail não aplicado')
if 'Usuário: Comercial' not in s:
    raise SystemExit('nome visual não aplicado')
p.write_text(s,encoding='utf-8')
