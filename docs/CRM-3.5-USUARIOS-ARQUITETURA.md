# CRM Comercial 3.5 — Usuários e Permissões

## Objetivo
Adicionar administração de usuários ao CRM sem expor senhas ou chaves administrativas no navegador e sem alterar a versão 3.4 em produção durante o desenvolvimento.

## Perfis previstos no CRM
- Administrador: acesso total, inclusive usuários e permissões.
- Comercial: pode trabalhar com clientes, orçamentos, vendas e acompanhamentos nas empresas autorizadas.
- Consulta: somente leitura nas empresas autorizadas.

## Regras de segurança
- Senhas continuam exclusivamente no Supabase Auth.
- O frontend nunca recebe a service_role key.
- Convites/criação de usuários devem ocorrer por Edge Function protegida.
- Cada usuário recebe acesso somente às empresas explicitamente autorizadas.
- As políticas RLS devem validar usuário autenticado + empresa + permissão.
- O usuário administrador atual permanece proprietário das empresas existentes.

## Base preparada para aplicações futuras
A camada de identidade deve ser reutilizável por aplicações separadas:
- CRM Comercial
- Estoque e Insumos
- Controle de Produção

Essas aplicações podem ter interfaces e tabelas separadas, mantendo em comum:
- Supabase Auth
- cadastro de empresas
- usuários
- vínculos de usuários com empresas

Assim, no futuro um mesmo login poderá receber permissões diferentes em cada sistema sem misturar os módulos em uma única interface.

## Estratégia de desenvolvimento
1. Manter `main` na versão 3.4 estável.
2. Desenvolver em `desenvolvimento-3.5-usuarios`.
3. Preferir uma branch de desenvolvimento do Supabase para testar migrations/RLS/Edge Functions.
4. Criar tabelas de perfil e acesso por empresa.
5. Adaptar o frontend para carregar apenas empresas autorizadas.
6. Criar aba Usuários somente para administrador.
7. Implementar convite seguro por e-mail via Edge Function.
8. Testar com usuário fictício: administrador, comercial e consulta.
9. Somente após testes, publicar a 3.5.
