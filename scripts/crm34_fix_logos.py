from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
s=s.replace("assets/logo-stampo.svg","https://raw.githubusercontent.com/costathiagocs-web/crm-comercial-pessoal/desenvolvimento-3.4-melhorias/assets/logo-stampo.webp")
s=s.replace("assets/logo-eletro.svg","https://raw.githubusercontent.com/costathiagocs-web/crm-comercial-pessoal/desenvolvimento-3.4-melhorias/assets/logo-eletro.webp")
if 'logo-stampo.webp' not in s or 'logo-eletro.webp' not in s:
    raise SystemExit('Não foi possível aplicar os logos')
p.write_text(s,encoding='utf-8')
