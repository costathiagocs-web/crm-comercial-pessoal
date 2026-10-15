-- CRM Comercial 3.4 - Pre-publicacao multiempresa
-- Pode ser executado antes do merge da 3.4: nao torna empresa_id obrigatorio.

-- 1) Verificar se existem registros sem empresa definida.
SELECT 'clientes' AS tabela, COUNT(*) AS sem_empresa
FROM public.clientes WHERE empresa_id IS NULL
UNION ALL
SELECT 'orcamentos', COUNT(*) FROM public.orcamentos WHERE empresa_id IS NULL
UNION ALL
SELECT 'vendas', COUNT(*) FROM public.vendas WHERE empresa_id IS NULL
UNION ALL
SELECT 'acompanhamentos', COUNT(*) FROM public.acompanhamentos WHERE empresa_id IS NULL;

-- 2) Indices para acelerar as consultas do CRM por usuario + empresa.
CREATE INDEX IF NOT EXISTS idx_clientes_usuario_empresa_criado
  ON public.clientes (usuario_id, empresa_id, criado_em DESC);

CREATE INDEX IF NOT EXISTS idx_orcamentos_usuario_empresa_data
  ON public.orcamentos (usuario_id, empresa_id, data_orcamento DESC);

CREATE INDEX IF NOT EXISTS idx_vendas_usuario_empresa_data
  ON public.vendas (usuario_id, empresa_id, data_venda DESC);

CREATE INDEX IF NOT EXISTS idx_acompanhamentos_usuario_empresa_data
  ON public.acompanhamentos (usuario_id, empresa_id, data_contato DESC);

-- 3) Verificar se as empresas cadastradas pertencem ao usuario esperado.
SELECT id, nome, usuario_id, criada_em
FROM public.empresas
ORDER BY nome;
