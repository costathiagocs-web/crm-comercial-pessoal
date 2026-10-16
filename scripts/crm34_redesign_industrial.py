from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
marker='</style>'
if marker not in s:
    raise SystemExit('style nao encontrado')

css=r'''

/* CRM 3.4 • Redesign industrial Eletro Quadros / Stampo */
:root{
 --eq-bg:#11151b;--eq-panel:#1a1f27;--eq-panel-2:#202630;--eq-border:#343c49;
 --eq-text:#f5f7fb;--eq-muted:#9ba8b8;--eq-blue:#173f7a;--eq-blue-2:#225da8;
 --eq-orange:#f5a12a;--eq-green:#4fc77b;--eq-red:#ef6a6a;
}
html{background:var(--eq-bg)}
body{background:radial-gradient(circle at 80% -10%,#18345f33 0,transparent 34%),linear-gradient(180deg,#11151b,#151a21 60%,#11151b);color:var(--eq-text);min-height:100vh}
header{background:linear-gradient(90deg,#0a1b36 0%,#102b54 58%,#0d2345 100%);border-bottom:1px solid #29456c;box-shadow:0 10px 30px #0005;padding:16px max(24px,calc((100vw - 1540px)/2));position:relative}
header:after{content:"";position:absolute;left:0;right:0;bottom:0;height:3px;background:linear-gradient(90deg,var(--eq-orange) 0 14%,#2764b8 14% 50%,transparent 80%)}
header h1{color:white;font-size:22px;display:flex;align-items:center;gap:11px;letter-spacing:-.35px}
header h1:before{content:"EQ";display:grid;place-items:center;width:38px;height:38px;border:2px solid var(--eq-orange);border-radius:9px;color:var(--eq-orange);font-weight:900;font-size:14px;background:#ffffff0b;box-shadow:inset 0 0 0 1px #ffffff0a}
header small{color:#b8c8df!important}
main{max-width:1540px;margin:24px auto;padding:0 22px}
#app{grid-template-columns:225px minmax(0,1fr);gap:22px}
#tabs{background:linear-gradient(180deg,#0b2345,#0a1b36);border:1px solid #24446f;border-radius:16px;box-shadow:0 16px 36px #0005;padding:13px 10px;top:18px}
#tabs:before{content:"COMERCIAL";color:#8fa8ca;border-bottom:1px solid #274669;margin:0 8px 8px;padding:10px 7px 14px;font-size:10px;letter-spacing:2.3px}
#tabs button,#tabs button:not(.secondary){background:transparent!important;color:#cbd8e9!important;border:1px solid transparent!important;box-shadow:none!important;border-radius:9px;padding:12px 13px;font-weight:650;transition:.16s ease}
#tabs button:hover{background:#16365f!important;color:white!important;border-color:#2e568b!important;transform:translateX(2px)}
#tabs button.active,#tabs button[aria-current="page"]{background:linear-gradient(90deg,#173f7a,#1f569b)!important;color:white!important;border-color:#2f68b0!important;box-shadow:inset 4px 0 0 var(--eq-orange),0 6px 16px #0003!important}
#app>.view{min-width:0}
.card{background:linear-gradient(180deg,#1b2028,#181d24);color:var(--eq-text);border:1px solid var(--eq-border);border-radius:14px;box-shadow:0 8px 24px #0002;padding:22px}
.card h2{color:#fff;font-size:20px}
.muted,small{color:var(--eq-muted)}
.grid{gap:13px}
.kpi{background:linear-gradient(145deg,#1d2430,#171c23)!important;border:1px solid #334156!important;position:relative;overflow:hidden;min-height:112px}
.kpi:before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:linear-gradient(var(--eq-orange),#df7f00)}
.kpi small{color:#aab8ca;font-size:11px;text-transform:uppercase;letter-spacing:.7px}
.kpi b{color:#fff;font-size:25px;margin-top:10px}
button{background:linear-gradient(180deg,#2367bd,#194f96);border:1px solid #3477c8;color:#fff;box-shadow:0 3px 9px #0003;border-radius:8px;font-weight:700}
button:hover{filter:brightness(1.1);transform:translateY(-1px)}
button.secondary{background:#252c36;color:#dce7f5;border-color:#465161}
button.danger{background:#8e2f3d;border-color:#b04a59}
input,select,textarea{background:#141920;color:#f5f7fb;border:1px solid #404a58;border-radius:8px;box-shadow:inset 0 1px 0 #ffffff05}
input::placeholder,textarea::placeholder{color:#6f7d90}
input:focus,select:focus,textarea:focus{border-color:#3f82d1;box-shadow:0 0 0 3px #2b6fc527;outline:0}
label{color:#c7d3e2;font-weight:650}
.tablewrap{border:1px solid #303844;border-radius:10px;overflow:auto;background:#151a20}
table{background:#151a20;color:#e9edf4}
th{background:#10151b;color:#9fb0c5;border-bottom:1px solid #37414e;position:sticky;top:0;z-index:1}
td{border-bottom:1px solid #2b323c;color:#eef2f7}
tbody tr:hover{background:#1e2630}
.pill{background:#203c63;color:#dceaff;border:1px solid #315985}
.notice{background:#332815;border:1px solid #6d5224;color:#f5d596}
.good{color:var(--eq-green)}.bad{color:var(--eq-red)}
#msg .card{background:#172437;border-color:#285181}
.auth{background:linear-gradient(180deg,#18202b,#151a21);border:1px solid #34445a;box-shadow:0 22px 60px #0006}
.empresa-controles{gap:9px}
.empresa-controles label{color:#a9bed9!important}
.empresa-controles select{background:#0f1e34;color:#fff;border:1px solid #355d90;min-width:230px}
.empresa-controles span{color:#c7d7eb}
#relatorio pre{background:#13181e;border:1px solid #343d49;border-radius:10px;padding:18px;line-height:1.55;color:#edf2f8}
#historico>.card:first-child{border-top:3px solid var(--eq-orange)}
.item{border-bottom-color:#303945}
.assistantnote{color:#9bacc0}.bubble{background:#202a36;color:#eef3fa}.bubble.me{background:#173b67}
a{color:#69a8f4}
::-webkit-scrollbar{width:10px;height:10px}::-webkit-scrollbar-track{background:#11161c}::-webkit-scrollbar-thumb{background:#3a4655;border-radius:20px;border:2px solid #11161c}
@media(max-width:980px){#app{grid-template-columns:190px minmax(0,1fr);gap:14px}main{padding:0 12px}}
@media(max-width:720px){header{padding:14px 13px}header h1{font-size:18px}header h1:before{width:32px;height:32px;font-size:12px}main{padding:0 10px}#tabs{background:#0b2345;border-radius:11px;padding:8px}#tabs button,#tabs button:not(.secondary){white-space:nowrap!important}.card{padding:16px}.empresa-controles select{min-width:150px;max-width:100%}}
'''

if 'CRM 3.4 • Redesign industrial Eletro Quadros / Stampo' not in s:
    s=s.replace(marker,css+'\n'+marker,1)

s=s.replace('<h1>CRM Comercial Pessoal</h1><small>Versão 3.4 • Multiempresa • Supabase • Olist Tiny (lançamento manual)</small>','<h1>CRM Comercial</h1><small>Eletro Quadros + Stampo • Gestão comercial multiempresa</small>',1)

for required in ['Redesign industrial Eletro Quadros / Stampo','--eq-orange:#f5a12a','CRM Comercial</h1>']:
    if required not in s:
        raise SystemExit('Validacao falhou: '+required)

p.write_text(s,encoding='utf-8')

# trigger redesign workflow
