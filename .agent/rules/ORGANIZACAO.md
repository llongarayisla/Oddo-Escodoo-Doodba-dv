# Organização obrigatória dos dados de agentes

Convenção definida pelo usuário para este projeto:

| Diretório        | Conteúdo                                                                                                                                   |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `.agent/plan/`   | Planos do que será feito e registro do que foi efetivamente executado. Usar nomes descritivos com identificador e extensão `.plan.md`.     |
| `.agent/docs/`   | Documentação, fontes, evidências e referências preservadas para consultas futuras.                                                         |
| `.agent/skills/` | Habilidades reutilizáveis, especialmente diagnósticos e soluções comprovadas de problemas. Cada habilidade tem pasta própria e `SKILL.md`. |
| `.agent/rules/`  | Regras de negócio, obrigações, proibições e limites de atuação e acesso.                                                                   |

## Aplicação

- Todo novo material de conhecimento mantido pelos agentes deve ficar nessas categorias,
  incluindo documentação de pastas de código: usar uma seção ou documento correspondente
  em `.agent/docs/`.
- Manter `AGENTS.md` na raiz somente como ponto de descoberta das regras, e `README.md`
  como apresentação e índice do projeto. Não duplicar neles o corpo das regras e
  documentos.
- Código executável do produto, Dockerfiles e configurações de runtime mantêm seus
  caminhos técnicos; não são movidos para `.agent/` por esta convenção.
- Antes de pesquisar novamente um problema, consultar as skills pertinentes e as
  evidências existentes. Verificar se ainda se aplicam às versões atuais.
- Ao resolver um erro, registrar sintomas, contexto/versões, diagnóstico, passos
  realmente executados, resultado comprovado e limite de aplicação em uma skill. Não
  transformar hipótese em solução validada.
- Skills não ampliam permissões nem substituem regras de negócio. Não salvar
  credenciais, tokens ou dados privados em conhecimento versionado.
- Nos planos, manter status, pendências e evidências da execução. Não marcar uma fase
  como implementada apenas porque seu plano foi criado.
- Ao salvar fontes, registrar URL/origem, data de consulta quando conhecida, conteúdo
  necessário e limites da verificação; não depender apenas de arquivo temporário.
- Atualizar links quando mover arquivos e evitar cópias concorrentes do mesmo documento.

Esta convenção substitui os caminhos anteriores `docs/` e os planos na raiz. Estruturas
propostas nos planos deverão obedecê-la durante a implementação.
