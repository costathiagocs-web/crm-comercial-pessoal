-- CRM Comercial 3.4 - Finalizacao pos-publicacao
-- EXECUTAR SOMENTE DEPOIS que a versao 3.4 estiver publicada e os testes
-- de cadastro nas duas empresas estiverem aprovados.

BEGIN;

DO $$
DECLARE
  total_sem_empresa bigint;
BEGIN
  SELECT
    (SELECT COUNT(*) FROM public.clientes WHERE empresa_id IS NULL) +
    (SELECT COUNT(*) FROM public.orcamentos WHERE empresa_id IS NULL) +
    (SELECT COUNT(*) FROM public.vendas WHERE empresa_id IS NULL) +
    (SELECT COUNT(*) FROM public.acompanhamentos WHERE empresa_id IS NULL)
  INTO total_sem_empresa;

  IF total_sem_empresa > 0 THEN
    RAISE EXCEPTION 'Existem % registro(s) sem empresa_id. Corrija-os antes de tornar o campo obrigatorio.', total_sem_empresa;
  END IF;
END $$;

ALTER TABLE public.clientes
  ALTER COLUMN empresa_id SET NOT NULL;

ALTER TABLE public.orcamentos
  ALTER COLUMN empresa_id SET NOT NULL;

ALTER TABLE public.vendas
  ALTER COLUMN empresa_id SET NOT NULL;

ALTER TABLE public.acompanhamentos
  ALTER COLUMN empresa_id SET NOT NULL;

COMMIT;

-- Verificacao final
SELECT table_name, column_name, is_nullable
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name IN ('clientes','orcamentos','vendas','acompanhamentos')
  AND column_name = 'empresa_id'
ORDER BY table_name;
