from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

repls=[
("let quoteFilters={search:'',status:'todos',start:'',end:''};","let quoteFilters={search:'',status:'todos'};"),
("quoteFilters={search:'',status:'todos',start:'',end:''};","quoteFilters={search:'',status:'todos'};"),
("<div><label>Último contato</label><input name=\"ultimo_contato\" type=\"date\" value=\"'+val('ultimo_contato')+'\"></div>",""),
("if(f.start&&String(o.data_orcamento||'')<f.start)return false;if(f.end&&String(o.data_orcamento||'')>f.end)return false;",""),
("<div><label for=\"quoteStart\">Data inicial</label><input id=\"quoteStart\" type=\"date\" value=\"'+esc(f.start)+'\"></div><div><label for=\"quoteEnd\">Data final</label><input id=\"quoteEnd\" type=\"date\" value=\"'+esc(f.end)+'\"></div>",""),
("<th>Data</th><th>Valor</th><th>Status</th><th>Retorno</th>","<th>Data do orçamento</th><th>Valor</th><th>Status</th><th>Próximo contato</th>"),
("$('quoteStart').onchange=ev=>{quoteFilters.start=ev.target.value;renderQuotes()};\n$('quoteEnd').onchange=ev=>{quoteFilters.end=ev.target.value;renderQuotes()};\n",""),
("$('clearQuoteFilters').onclick=()=>{quoteFilters={search:'',status:'todos',start:'',end:''};renderQuotes()};","$('clearQuoteFilters').onclick=()=>{quoteFilters={search:'',status:'todos'};renderQuotes()};"),
("if(!last&&!o.ultimo_contato&&days(o.data_orcamento)>=5){score+=35;why.push('sem contato registrado há '+days(o.data_orcamento)+' dias')}if((last||o.ultimo_contato)&&days([String(last?.data_contato||'').slice(0,10),o.ultimo_contato||''].sort().at(-1))>=7){score+=25;why.push('último contato há '+days(String(last.data_contato).slice(0,10))+' dias')}","if(!last&&days(o.data_orcamento)>=5){score+=35;why.push('sem acompanhamento registrado há '+days(o.data_orcamento)+' dias')}if(last&&days(String(last.data_contato).slice(0,10))>=7){score+=25;why.push('último acompanhamento há '+days(String(last.data_contato).slice(0,10))+' dias')}")
]
for old,new in repls:
    if old not in s:
        raise SystemExit('Trecho nao encontrado: '+old[:90])
    s=s.replace(old,new,1)

start=s.find('function reportText(){')
end=s.find('\nfunction renderReport(){',start)
if start<0 or end<0:
    raise SystemExit('reportText nao encontrado')
new_report=r'''function reportText(){let end=new Date(today()+'T12:00:00'),start=new Date(end);start.setDate(end.getDate()-6);let future=new Date(end);future.setDate(end.getDate()+6);let d0=start.toLocaleDateString('en-CA'),d1=today(),d2=future.toLocaleDateString('en-CA'),q=data.orcamentos.filter(o=>o.data_orcamento>=d0&&o.data_orcamento<=d1),v=data.vendas.filter(o=>o.data_venda>=d0&&o.data_venda<=d1),open=data.orcamentos.filter(o=>['pendente','negociacao'].includes(o.status)),overdue=open.filter(o=>o.proximo_contato&&o.proximo_contato<d1),todayContacts=open.filter(o=>o.proximo_contato===d1),next=open.filter(o=>o.proximo_contato&&o.proximo_contato>d1&&o.proximo_contato<=d2).sort((a,b)=>String(a.proximo_contato).localeCompare(String(b.proximo_contato))),without=open.filter(o=>!o.proximo_contato),win=q.filter(o=>o.status==='aprovado').length,a=analysis();let agenda=next.slice(0,8).map(o=>'• '+day(o.proximo_contato)+' — '+clientName(o.cliente_id)+' — '+(o.numero_tiny||'sem número')+' — '+money(o.valor)).join('\n');return 'RELATÓRIO SEMANAL — '+empresaNome()+' — '+day(d0)+' a '+day(d1)+'\n\nRESULTADOS DA SEMANA\nOrçamentos incluídos: '+q.length+' | Valor: '+money(q.reduce((s,o)=>s+Number(o.valor),0))+'\nPedidos: '+v.length+' | Valor: '+money(v.reduce((s,o)=>s+Number(o.valor),0))+'\nAproveitamento das propostas incluídas na semana (status atual aprovado): '+(q.length?(win/q.length*100).toFixed(1):'0')+'%\n\nACOMPANHAMENTO PARA FECHAMENTO\nEm aberto: '+open.length+'\nPróximo contato hoje: '+todayContacts.length+'\nRetornos vencidos: '+overdue.length+'\nSem próximo contato definido: '+without.length+'\nPróximos contatos em até 7 dias: '+next.length+(agenda?'\n'+agenda:'')+'\n\nAÇÕES RECOMENDADAS\n'+a.notes.map((n,i)=>(i+1)+'. '+n).join('\n')+'\n\nObservação: a data do orçamento mede quando a proposta foi incluída; o próximo contato organiza o acompanhamento comercial. O histórico de contatos continua sendo registrado na aba Acompanhamentos.'}'''
s=s[:start]+new_report+s[end:]

checks=[
    "let quoteFilters={search:'',status:'todos'};",
    'Data do orçamento',
    'Próximo contato',
    'ACOMPANHAMENTO PARA FECHAMENTO',
    'Sem próximo contato definido',
    'último acompanhamento há'
]
for c in checks:
    if c not in s:
        raise SystemExit('Validacao falhou: '+c)
if 'id="quoteStart"' in s or 'id="quoteEnd"' in s:
    raise SystemExit('Filtros de periodo ainda presentes em Orcamentos')

p.write_text(s,encoding='utf-8')

# disparo controlado
