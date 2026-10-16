from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
start=s.find('function renderSales(){')
end=s.find('\nfunction renderFollowups(){', start)
if start < 0 or end < 0:
    raise SystemExit('renderSales nao encontrado')

new=r'''function renderSales(){
 $('vendas').innerHTML='<div class="card"><h2>Novo pedido de venda</h2><p class="muted">Cadastre pedidos efetivamente realizados. Ao selecionar um orçamento, o valor é preenchido automaticamente e pode ser ajustado antes de salvar.</p><form id="fv"><div class="formgrid"><div><label>Orçamento relacionado (opcional)</label><select name="orcamento_id" id="saleQuote"><option value="">Sem orçamento relacionado</option>'+opts(data.orcamentos,o=>(o.numero_tiny||'Sem número')+' — '+clientName(o.cliente_id))+'</select></div><div><label>Número do pedido Tiny</label><input name="numero_pedido_tiny"></div><div><label>Data da venda</label><input name="data_venda" type="date" value="'+today()+'" required></div><div><label>Valor em R$</label><input name="valor" id="saleValue" type="number" min="0" step="0.01" required></div></div><label>Observações</label><textarea name="observacoes"></textarea><div class="formactions"><button>Salvar venda</button></div></form></div><div class="card"><h2>Pedidos realizados</h2><div class="tablewrap"><table><thead><tr><th>Pedido Tiny</th><th>Data</th><th>Valor</th><th>Orçamento</th></tr></thead><tbody>'+data.vendas.map(v=>'<tr><td>'+esc(v.numero_pedido_tiny)+'</td><td>'+day(v.data_venda)+'</td><td>'+money(v.valor)+'</td><td>'+esc(data.orcamentos.find(o=>o.id===v.orcamento_id)?.numero_tiny||'—')+'</td></tr>').join('')+'</tbody></table></div></div>';
 const preencherValor=()=>{const id=$('saleQuote').value;if(!id){$('saleValue').value='';return}const o=data.orcamentos.find(x=>x.id===id);$('saleValue').value=o&&o.valor!==null&&o.valor!==undefined?Number(o.valor).toFixed(2):''};
 $('saleQuote').onchange=preencherValor;
 if($('saleQuote').value)preencherValor();
 formHandler('fv',p=>save('vendas',p))
}'''

s=s[:start]+new+s[end:]
for required in ['id="saleQuote"','id="saleValue"','preencherValor','toFixed(2)']:
    if required not in s:
        raise SystemExit('Validacao falhou: '+required)
p.write_text(s,encoding='utf-8')

# disparo controlado
