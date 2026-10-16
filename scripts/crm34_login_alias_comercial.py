from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
s=s.replace('<label for="email">E-mail</label>','<label for="email">Usuário</label>',1)
s=s.replace('id="email" type="email"','id="email" type="text"',1)
s=s.replace('placeholder="seuemail@empresa.com"','placeholder="Comercial"',1)
old="const {error}=await sb.auth.signInWithPassword({email:$('email').value.trim(),password:$('password').value});"
new="const usuario=$('email').value.trim();const emailLogin=usuario.toLowerCase()==='comercial'?'costathiagocs@gmail.com':usuario;const {error}=await sb.auth.signInWithPassword({email:emailLogin,password:$('password').value});"
if old not in s: raise SystemExit('login handler alvo não encontrado')
s=s.replace(old,new,1)
old2="const email=$('email').value.trim();if(!email){message('Informe seu usuário (e-mail) para recuperar a senha.',true);return}const {error}=await sb.auth.resetPasswordForEmail(email);"
new2="const usuario=$('email').value.trim();if(!usuario){message('Informe o usuário para recuperar a senha.',true);return}const email=usuario.toLowerCase()==='comercial'?'costathiagocs@gmail.com':usuario;const {error}=await sb.auth.resetPasswordForEmail(email);"
if old2 not in s: raise SystemExit('recovery handler alvo não encontrado')
s=s.replace(old2,new2,1)
p.write_text(s,encoding='utf-8')
