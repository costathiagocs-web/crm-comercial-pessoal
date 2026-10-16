from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
start=s.find('\n/* CRM 3.4 • Dashboard por mês */\n')
if start==-1: raise SystemExit('bloco mensal não encontrado')
first_close=s.find('</script>',start)
if first_close==-1: raise SystemExit('fechamento do script externo não encontrado')
block=s[start:first_close]
s=s[:start]+s[first_close:]
last_close=s.rfind('</script>')
if last_close==-1: raise SystemExit('script principal não encontrado')
s=s[:last_close]+block+'\n'+s[last_close:]
if s.find('src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.min.js">\n/* CRM 3.4 • Dashboard por mês */')!=-1:
    raise SystemExit('bloco ainda está dentro do script externo')
if s.rfind('/* CRM 3.4 • Dashboard por mês */') < s.find('<script>'):
    raise SystemExit('bloco não foi movido para o script principal')
p.write_text(s,encoding='utf-8')
