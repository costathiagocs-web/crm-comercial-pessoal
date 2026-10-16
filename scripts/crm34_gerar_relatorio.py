from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

old_buttons='<div class="formactions"><button id="copyReport">Copiar relatório</button><button class="secondary" id="downloadReport">Baixar .txt</button></div>'
new_buttons='<div class="formactions"><button id="generateReport">Gerar relatório</button><button class="secondary" id="copyReport">Copiar relatório</button><button class="secondary" id="downloadReport">Baixar .txt</button></div>'
if old_buttons not in s:
    raise SystemExit('Botoes atuais do relatorio nao encontrados')
s=s.replace(old_buttons,new_buttons,1)

old_handlers="'; $('copyReport').onclick=()=>navigator.clipboard.writeText(reportText()).then(()=>message('Relatório copiado'));"
new_handlers="'; $('generateReport').onclick=()=>{$('reportBody').textContent=reportText();message('Relatório gerado e atualizado')};$('copyReport').onclick=()=>navigator.clipboard.writeText($('reportBody').textContent||reportText()).then(()=>message('Relatório copiado'));"
if old_handlers not in s:
    raise SystemExit('Handlers do relatorio nao encontrados')
s=s.replace(old_handlers,new_handlers,1)

old_download="$('downloadReport').onclick=()=>{let blob=new Blob([reportText()],{type:'text/plain;charset=utf-8'}),a=document.createElement('a');"
new_download="$('downloadReport').onclick=()=>{let blob=new Blob([$(`reportBody`).textContent||reportText()],{type:'text/plain;charset=utf-8'}),a=document.createElement('a');"
if old_download not in s:
    raise SystemExit('Download do relatorio nao encontrado')
s=s.replace(old_download,new_download,1)

for required in ['id="generateReport"','Relatório gerado e atualizado']:
    if required not in s:
        raise SystemExit('Validacao falhou: '+required)

p.write_text(s,encoding='utf-8')
