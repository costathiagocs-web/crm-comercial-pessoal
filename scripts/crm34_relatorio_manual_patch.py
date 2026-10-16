from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

# estado do relatorio manual
old="let editingClientId=null,clientSearch='';"
new="let editingClientId=null,clientSearch='';\nlet generatedReportText='',reportNeedsGeneration=true;"
if old not in s: raise SystemExit('Estado global nao encontrado')
s=s.replace(old,new,1)

# troca de empresa zera o relatorio gerado
old="empresaAtual=id;editingClientId=null;clientSearch='';editingQuoteId=null;quoteFilters={search:'',status:'todos'};"
new="empresaAtual=id;editingClientId=null;clientSearch='';editingQuoteId=null;quoteFilters={search:'',status:'todos'};generatedReportText='';reportNeedsGeneration=true;"
if old not in s: raise SystemExit('Troca de empresa nao encontrada')
s=s.replace(old,new,1)

# qualquer novo registro via save torna relatorio desatualizado
old="else{message('Registro salvo');await refresh()}"
new="else{reportNeedsGeneration=true;message('Registro salvo');await refresh()}"
if old not in s: raise SystemExit('save generico nao encontrado')
s=s.replace(old,new,1)

# salvar/editar orcamento torna relatorio desatualizado
old="editingQuoteId=null;message(id?'Orçamento atualizado':'Orçamento cadastrado');await refresh()"
new="editingQuoteId=null;reportNeedsGeneration=true;message(id?'Orçamento atualizado':'Orçamento cadastrado');await refresh()"
if old not in s: raise SystemExit('save orcamento nao encontrado')
s=s.replace(old,new,1)

# excluir orcamento torna relatorio desatualizado
old="if(editingQuoteId===id)editingQuoteId=null;message('Orçamento excluído');await refresh()"
new="if(editingQuoteId===id)editingQuoteId=null;reportNeedsGeneration=true;message('Orçamento excluído');await refresh()"
if old not in s: raise SystemExit('delete orcamento nao encontrado')
s=s.replace(old,new,1)

start=s.find('function renderReport(){')
end=s.find('\n\n// V3:',start)
if start<0 or end<0: raise SystemExit('renderReport nao encontrado')
new_render=r'''function renderReport(){const body=generatedReportText?esc(generatedReportText):'Clique em “Gerar relatório” para criar o relatório com os dados atuais.';const aviso=generatedReportText&&reportNeedsGeneration?'<div class="notice">Existem alterações após a última geração. Clique em <b>Gerar relatório</b> para atualizar.</div>':'';$('relatorio').innerHTML='<div class="card"><h2>Relatório semanal</h2><p class="muted">O relatório é gerado manualmente com os dados atuais de orçamentos, pedidos e acompanhamentos.</p>'+aviso+'<pre id="reportBody">'+body+'</pre><div class="formactions"><button id="generateReport">Gerar relatório</button><button class="secondary" id="copyReport">Copiar relatório</button><button class="secondary" id="downloadReport">Baixar .txt</button></div></div><div class="card"><h2>Modelo de mensagem para acompanhamento</h2><p>Olá, tudo bem? Gostaria de saber se você conseguiu avaliar nossa proposta comercial. Estou à disposição para esclarecer dúvidas sobre valores, prazos ou especificações. Podemos conversar?</p><button class="secondary" id="copyMessage">Copiar mensagem</button></div>';
$('generateReport').onclick=()=>{generatedReportText=reportText();reportNeedsGeneration=false;renderReport();message('Relatório gerado com os dados atuais')};
$('copyReport').onclick=()=>{if(!generatedReportText){message('Gere o relatório antes de copiar.',true);return}navigator.clipboard.writeText(generatedReportText).then(()=>message('Relatório copiado'))};
$('downloadReport').onclick=()=>{if(!generatedReportText){message('Gere o relatório antes de baixar.',true);return}let blob=new Blob([generatedReportText],{type:'text/plain;charset=utf-8'}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='relatorio-semanal-crm.txt';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),2000)};
$('copyMessage').onclick=()=>navigator.clipboard.writeText('Olá, tudo bem? Gostaria de saber se você conseguiu avaliar nossa proposta comercial. Estou à disposição para esclarecer dúvidas sobre valores, prazos ou especificações. Podemos conversar?').then(()=>message('Mensagem copiada'))}'''
s=s[:start]+new_render+s[end:]

for required in ['generatedReportText','reportNeedsGeneration','Clique em “Gerar relatório”','Relatório gerado com os dados atuais']:
    if required not in s: raise SystemExit('Validacao falhou: '+required)

p.write_text(s,encoding='utf-8')
