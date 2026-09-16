# Organização do conhecimento dos agentes

Status: concluído.

## Solicitação

Concentrar planos/registros em `.agent/plan`, documentação/fontes em `.agent/docs`,
habilidades reutilizáveis em `.agent/skills` e regras em `.agent/rules`.

## Execução

- [x] Migrar os cinco planos P0–P4 para `.agent/plan`, preservando os nomes.
- [x] Migrar o registro de instalação para `.agent/docs`.
- [x] Migrar regras para `.agent/rules` e registrar a convenção em ORGANIZACAO.md.
- [x] Manter AGENTS.md como entrada curta para descoberta das regras.
- [x] Atualizar links do README e referências dos planos para a nova organização.
- [x] Salvar resumo das fontes verificadas, sem atribuir validação às fontes pendentes.
- [x] Criar skill para recuperação do Docker Desktop Linux parado, baseada no
      diagnóstico e resultado observados nesta sessão.
- [x] Conferir links locais: nenhum link quebrado encontrado.

## Verificação e limites

A skill possui frontmatter com nome/descrição, contexto, procedimento, limites e
referência à evidência. A tentativa de executar `quick_validate.py` do skill-creator não
pôde concluir: o Python disponível não contém PyYAML
(`ModuleNotFoundError: No module named 'yaml'`). A estrutura foi revisada manualmente;
não houve instalação de dependências apenas para essa conferência.

Nenhum comando operacional Docker foi executado nesta reorganização documental. P0–P4
continuam planejados; esta conclusão se refere apenas à organização. Skills locais são
descobertas pela orientação no AGENTS.md; não foi feita instalação global de habilidades
no aplicativo.
