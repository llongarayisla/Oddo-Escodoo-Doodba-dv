# P3 — Integrações e importação de dados

Status: planejado; implementação não iniciada. Dependências:
[P0](estrutura_odoo_doodba_f884730d532.plan.md),
[P1](desenvolvimento_odoo_doodba_p1_7a29c4e81b6.plan.md) e
[P2](modulos_negocio_odoo_doodba_p2_c93a6e702d1.plan.md) validados para os processos
envolvidos. Nesta etapa, somente o plano é entregue; nenhum sistema externo será
acessado e nenhum dado será importado pela criação deste arquivo.

## 1. Objetivo

Importar dados e integrar os sistemas efetivamente necessários ao recorte do P2, com
mapeamento explícito, validação, prevenção de duplicidades, recuperação de falhas e
conciliação dos resultados.

P3 tem duas frentes independentes: carga de dados e integração contínua. Executar apenas
as frentes necessárias. Se não houver origem ou sistema a integrar, registrar como não
aplicável com o usuário, sem inventar conectores. Os sistemas, formatos, volumes e
sentidos de integração ainda não foram definidos.

## 2. Fontes e evidências

| Fonte                                                                                        | Uso                                                 | Limite                                                           |
| -------------------------------------------------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------------------------- |
| AGENTS.md e .agent/rules/REGRAS-DE-NEGOCIO.md                                                | Restrições técnicas e operacionais                  | Não identificam sistemas externos                                |
| Planos P0/P1/P2                                                                              | Infraestrutura, desenvolvimento e recorte funcional | São planos, não evidências de implementação                      |
| .agent/docs/INSTALACAO.md                                                                    | Histórico técnico disponível                        | Não contém contratos de integração                               |
| [Playlist Escodoo](https://www.youtube.com/playlist?list=PLs5WR750kjpdPxmU8vE-nIX1flWABqFvu) | Base do ambiente e gerenciamento de addons          | Não confirma procedimentos de migração ou conectores específicos |

Este P3 é uma proposta complementar à playlist. Na implementação, consultar documentação
oficial Odoo 14 e documentação/API da versão exata de cada sistema selecionado. Conferir
manifest, código, licença e dependências de conectores candidatos. Registrar URLs,
versões, revisões e data em .agent/docs/p3/FONTES.md. Não pressupor suporte a uma API,
autenticação ou recurso antes dessa verificação.

## 3. Regras e fronteiras

- Manter Odoo 14 e PostgreSQL 13, uma imagem final e um container Linux.
- Usar o ponto de entrada do P0/P1 e sua verificação de exclusividade do Docker local
  antes de operar; preservar containers, imagens e volumes alheios.
- Não criar Redis, workers ou bancos em containers adicionais. Processamento necessário
  deverá caber na arquitetura validada, ou ser apresentado como conflito.
- Código, mapeamentos e documentação neste repositório; dependências permanentes
  declaradas no build, sem instalações manuais efêmeras.
- Não montar socket Docker, criar daemon aninhado, publicar túnel ou abrir portas
  externas para resolver conectividade sem decisão específica do projeto.
- A regra de exclusividade não manda parar sistemas remotos. Se a origem estiver em
  outro container do mesmo Docker local, haverá conflito: priorizar exportação prévia
  para arquivo ou outra solução explicitamente acordada, sem reativá-lo silenciosamente
  durante a operação do Doodba.
- Dados reais, arquivos de entrada, backups, tokens e logs com conteúdo sensível fora do
  Git e do contexto de build. Versionar apenas amostras sintéticas.
- A autorização para criar este plano não autoriza envios, exclusões ou alterações em
  sistemas externos. Antes de executar, estabelecer origem, destino, dados, sentido e
  operações autorizadas; reutilizar autorizações específicas já existentes.

## 4. Pré-requisitos e decisões pendentes

O inventário pode começar antes da implementação. Cargas e integração funcional dependem
do ambiente validado e dos modelos/processos selecionados no P2.

| Decisão     | Informação necessária                                                   |
| ----------- | ----------------------------------------------------------------------- |
| Origem      | Sistema/arquivo, proprietário, versão e método autorizado de leitura    |
| Destino     | Banco Odoo, modelos e campos do recorte P2                              |
| Direção     | Entrada, saída ou bidirecional; uma carga ou sincronização recorrente   |
| Autoridade  | Qual sistema decide cada entidade/campo em caso de divergência          |
| Identidade  | Identificador estável e regra para registros já existentes              |
| Volume      | Quantidade, tamanho, frequência e janela de processamento               |
| Regras      | Obrigatórios, conversões, duplicidades, cancelamentos e exclusões       |
| Recuperação | Ponto de retorno, tolerância a rejeições e responsável pela conciliação |
| Acesso      | Ambiente de teste, permissões mínimas e forma de fornecer credenciais   |

Não presumir cliente/fornecedor/produto como escopo; são exemplos de entidades
possíveis, a selecionar conforme os requisitos reais.

## 5. Etapas de implementação

### P3.1 — Inventário e recorte de dados

- [ ] Identificar fontes, entidades e operações necessárias ao P2.
- [ ] Classificar carga inicial, complemento de dados e integração contínua.
- [ ] Obter esquema e amostra sintética ou anonimizada suficiente para análise.
- [ ] Registrar operações permitidas e impedir ações fora desse recorte.
- [ ] Definir responsável pela qualidade e pelo aceite dos dados.
- [ ] Identificar restrições de conectividade compatíveis com o container único.

Entrega: .agent/docs/p3/ESCOPO.md com origens, destinos, volumes estimados e decisões.

### P3.2 — Mapeamento e contrato

- [ ] Mapear campo de origem para modelo/campo Odoo, incluindo tipo, tamanho, nulidade,
      valor padrão e transformação.
- [ ] Definir datas/fusos, separadores decimais, moedas, unidades e codificação.
- [ ] Definir identidade estável: sistema de origem + entidade + ID externo.
- [ ] Definir criação versus atualização, precedência e proteção de campos que não
      pertencem à integração.
- [ ] Ordenar entidades pelas relações e definir tratamento de referências ausentes.
- [ ] Definir como duplicidades, conflitos e registros inválidos serão reportados.
- [ ] Exigir regra explícita para exclusão/cancelamento; ausência na origem não implica
      exclusão automática no Odoo.
- [ ] Para sincronização bidirecional, definir propriedade de campos e prevenção de
      ciclos; não habilitar bidirecionalidade por padrão.

Entrega: .agent/docs/p3/MAPEAMENTO.md e contratos versionados com exemplos sintéticos.

### P3.3 — Preparação e validação sem gravação

- [ ] Criar comando de validação/dry-run pelo ponto de entrada do projeto.
- [ ] Verificar esquema, tipos, obrigatórios, relações, duplicidades e regras do P2.
- [ ] Gerar resumo do que será criado, atualizado, ignorado ou rejeitado.
- [ ] Assegurar que dry-run não persiste alterações nem dispara efeitos externos; apenas
      rollback de transação não comprova ausência desses efeitos.
- [ ] Registrar checksum e versão do arquivo/contrato para vincular execução posterior
      ao material efetivamente validado.
- [ ] Separar erros de dados de falhas técnicas e fornecer motivos acionáveis.

Entrega: relatório prévio e dados preparados sem alteração de negócio.

### P3.4 — Importação controlada

- [ ] Escolher importador nativo ou módulo/script conforme requisitos verificados;
      utilizar ORM/API apropriada, evitando escrita direta nas tabelas de negócio.
- [ ] Realizar backup consistente de banco e filestore antes de carga real.
- [ ] Ensaiar em banco de homologação no mesmo PostgreSQL/container.
- [ ] Processar lotes com identidade de execução, limites transacionais e checkpoints.
- [ ] Usar identificadores estáveis para reexecução sem duplicação e atualização somente
      de campos previstos no contrato.
- [ ] Preservar correspondência origem/destino e resultado de cada registro, sem copiar
      payload sensível integralmente para logs comuns.
- [ ] Definir retomada após falha parcial, mantendo lotes concluídos rastreáveis.
- [ ] Para anexos, validar referência, conteúdo e persistência no filestore.

Entrega: carga repetível com relatório de resultados e rejeições explicadas.

### P3.5 — Conector, quando necessário

- [ ] Comparar funcionalidade nativa, addon compatível e implementação mínima com base
      em documentação oficial e testes da versão selecionada.
- [ ] Verificar autenticação, paginação, limites, timeouts, erros e limites de acesso.
- [ ] Declarar dependências e fixar revisões do código utilizado.
- [ ] Usar ambiente externo de teste quando disponível e autorizado; na ausência,
      validar contrato com fixtures/mocks e registrar que o teste externo ficou
      pendente.
- [ ] Implementar limites de lote e retry com atraso apenas para falhas transitórias.
- [ ] Tratar timeout após envio como resultado incerto: consultar/reconciliar antes de
      reenviar operação que possa duplicar efeito externo.
- [ ] Persistir checkpoint e identidade de eventos/operações; impedir execução
      concorrente do mesmo trabalho quando isso comprometer consistência.
- [ ] Manter sincronização desabilitada por padrão até validar o fluxo completo.
- [ ] Preferir fluxo de consulta compatível com ambiente local se atender ao requisito.
      Se webhooks públicos forem indispensáveis, registrar dependência de exposição a
      resolver no P4; não abrir túnel como atalho.

Entrega: conector do recorte com limitações de cobertura claramente identificadas.

### P3.6 — Conciliação e testes de falha

- [ ] Conciliar contagens: entradas = criados + atualizados + ignorados + rejeitados,
      com categorias mutuamente exclusivas e motivos definidos.
- [ ] Comparar campos e relações críticas por ID externo, além das contagens.
- [ ] Conferir totais/valores com as regras aprovadas no P2, quando aplicável.
- [ ] Testar segunda execução sem duplicação e atualização incremental correta.
- [ ] Testar duplicidade, relação ausente, dados inválidos e permissões insuficientes.
- [ ] Simular timeout, falha parcial, retomada e reinício do container.
- [ ] Verificar que registros/campos fora do escopo permanecem intactos.
- [ ] Testar prevenção de ciclos e conflitos se houver fluxo bidirecional.
- [ ] Registrar evidências de integração real separadamente dos testes com mocks.

Entrega: .agent/docs/p3/VALIDACAO-P3.md com resultados por requisito e cobertura
efetiva.

### P3.7 — Recuperação, operação e aceite

- [ ] Ensaiar restauração em banco/destino de teste separado, sem sobrescrever o banco
      corrente. Coordenar backup de banco e filestore.
- [ ] Documentar que restauração local não desfaz efeitos já enviados a outros sistemas;
      definir conciliação/compensação específica antes de permitir escrita externa.
- [ ] Entregar comandos para validar, executar, consultar estado, interromper novos
      lotes e retomar, usando o mesmo ponto de entrada.
- [ ] Definir retenção dos arquivos de entrada, rejeições e backups conforme o recorte;
      não executar exclusão automática por prazo arbitrário.
- [ ] Atualizar versões, configuração e guias das pastas próprias.
- [ ] Obter aceite dos resultados pelo responsável pelos dados; registrar pendências.

Entrega: operação manual controlada e recuperável. Agendamento de produção e
monitoramento permanente pertencem ao P4; não criar automações nesta etapa.

## 6. Estrutura prevista

```text
integracoes_dados_odoo_doodba_p3_b47e192ac80.plan.md
.agent/docs/p3/
  README.md
  FONTES.md
  ESCOPO.md
  MAPEAMENTO.md
  OPERACAO.md
  RECUPERACAO.md
  VALIDACAO-P3.md
  PENDENCIAS.md
integracoes/
  README.md
  contratos/
    README.md
  exemplos/
    README.md                 # somente exemplos sintéticos
```

Código de integração ficará no diretório de addons ou scripts estabelecido no P1,
conforme a implementação escolhida. Atualizar scripts/doodba.ps1, manifests e
.agent/docs/VERSOES.md, sem criar um segundo mecanismo operacional. Dados reais ficarão
em diretório local explicitamente ignorado pelo Git e Docker build, com localização
registrada; não criá-los com conteúdo fictício apresentado como dados do usuário.

## 7. Critérios de conclusão

1. Origem, destino, sentido e operações do recorte estão definidos e autorizados.
2. Mapeamento e identidades estão documentados e testados.
3. Dry-run entrega relatório sem alterações persistentes nem efeitos externos.
4. Carga/sincronização preserva relações, não duplica na reexecução e permite retomada.
5. Dados conciliados atendem aos critérios definidos; rejeições e divergências estão
   resolvidas ou aceitas explicitamente pelo responsável.
6. Falhas parciais, resultado incerto e recuperação têm comportamento verificado.
7. Versões, container único, exclusividade e persistência de P0/P1 permanecem válidos.
8. Não há segredos/dados reais nos arquivos versionados ou imagem de aplicação.
9. Responsável pelos dados registrou aceite das frentes incluídas no escopo.

Uma frente não necessária pode ser marcada como não aplicável. Uma integração necessária
testada somente com mocks continua pendente de validação externa; não declarar P3
completo por testes locais que não cobrem o contrato real exigido.

## 8. Fora do P3

- Produção, publicação de imagem, exposição pública, túneis, TLS e novos containers.
- Troca de versão Odoo/PostgreSQL e migração estrutural entre versões do ERP.
- Integrações com sistemas não identificados ou uso de credenciais não fornecidas.
- Emissão fiscal, pagamentos, mensagens reais e exclusões externas não autorizadas.
- Agendamentos permanentes, monitoramento contínuo e contratação de provedores.
- Limpeza adicional de imagens, volumes, cache ou dados de outros projetos.

## 9. Sequência e impedimentos

P3.1 → P3.2 → P3.3 → P3.4 para carga; P3.5 para integração necessária; ambas seguem para
P3.6 → P3.7. Etapas não aplicáveis serão justificadas.

Sem origem definida, executar apenas levantamento e desenho do contrato. Sem acesso
autorizado, continuar com amostras sintéticas e registrar limites. Se a implementação
exigir serviço adicional, versão incompatível ou acesso externo ainda não definido,
apresentar o conflito concreto antes de executar a operação dependente, preservando as
regras do projeto.

## Convenção atual de armazenamento

Planos e registros de execução: .agent/plan/. Documentação e fontes: .agent/docs/.
Habilidades comprovadas: .agent/skills/. Regras: .agent/rules/. As árvores ilustrativas
acima devem ser interpretadas conforme essa convenção; README técnico proposto para
pasta própria será documentado em .agent/docs/, exceto o README de apresentação da raiz.
Consulte ../rules/ORGANIZACAO.md.

Registro: plano migrado para .agent/plan; fase continua planejada, sem implementação.
