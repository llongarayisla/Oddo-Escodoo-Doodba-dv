# P1 — Fluxo de desenvolvimento Odoo/Doodba

Status: planejado; implementação não iniciada. Dependência:
[P0](estrutura_odoo_doodba_f884730d532.plan.md) validado em 2026-09-16
([VALIDACAO-P0.md](../docs/VALIDACAO-P0.md)). Este documento define o P1; a
implementação do fluxo de desenvolvimento ainda não foi executada.

## 1. Objetivo

Transformar o ambiente funcional do P0 em um ambiente de desenvolvimento reproduzível:
editar código local, gerenciar addons próprios e OCA, instalar e atualizar um módulo,
executar testes e depurar dentro do Linux do projeto.

O P0 entrega infraestrutura e persistência. O P1 entrega o ciclo de trabalho do
desenvolvedor, preservando Odoo 14, PostgreSQL 13, uma imagem final e um container. Não
reconstruir a infraestrutura antes de avaliar o resultado do P0.

## 2. Fontes e limites da evidência

| Fonte                                                                                        | Informação disponível                                                   | Aplicação                                                  |
| -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- | ---------------------------------------------------------- |
| AGENTS.md e .agent/rules/REGRAS-DE-NEGOCIO.md                                                | Regras explícitas do usuário                                            | Localidade, exclusividade e container único                |
| Plano P0 e .agent/docs/INSTALACAO.md                                                         | Arquitetura planejada e versões principais confirmadas                  | Base e pré-requisitos                                      |
| [Playlist Escodoo](https://www.youtube.com/playlist?list=PLs5WR750kjpdPxmU8vE-nIX1flWABqFvu) | Descrição e sequência consultadas                                       | Organização do P1                                          |
| [Linux 3 — VS Code](https://www.youtube.com/watch?v=-a_JC7uEubY)                             | Título confirmado; comandos e extensões ainda não verificados           | Workspace e editor                                         |
| [Linux 5 — Workspace e Doodba](https://www.youtube.com/watch?v=GrcQGAY6kqU)                  | Tema confirmado; procedimento completo ainda não verificado             | Workspace e Invoke                                         |
| [Linux 6 — Addons OCA e privados](https://www.youtube.com/watch?v=z2XXTlxctO0)               | Título confirmado; módulos específicos ainda não verificados            | Gerenciamento de addons                                    |
| [Linux 7 — PR e repositórios](https://www.youtube.com/watch?v=3vC5tmaKSvo)                   | Título confirmado; repositórios e PRs específicos ainda não verificados | Fontes Git e referências fixadas                           |
| [Linux 8 — odoo.conf e dependências](https://www.youtube.com/watch?v=an0SSXcXDYE)            | Título confirmado; parâmetros e pacotes ainda não verificados           | Configuração e dependências                                |
| [Doodba Copier Template](https://github.com/Tecnativa/doodba-copier-template)                | README consultado na preparação                                         | Inspecionar tarefas e estrutura na revisão escolhida no P0 |

A implementação consultará a documentação oficial da versão 14 do Odoo e dos componentes
efetivamente selecionados. Registrar links, commits e trechos de evidência em
.agent/docs/FONTES-P1.md. Não atribuir comandos, módulos, extensões ou versões às aulas
sem verificar seu conteúdo.

Depuração, módulo de exemplo, testes e ensaio de recuperação são complementos propostos
para validar o fluxo; não estão confirmados como conteúdo dos vídeos.

## 3. Condições para iniciar a implementação

- [x] P0 concluído, com evidências em .agent/docs/VALIDACAO-P0.md.
- [x] Login, conexão com PostgreSQL e persistência após recriação funcionando.
- [x] Revisões Doodba/Odoo e versões Python registradas em .agent/docs/VERSOES.md.
- [x] Script de exclusividade implementado e validado no P0.
- [x] Inventário do código, mounts, usuários e caminhos Linux resultantes do P0.

Se algum requisito falhar, corrigir e registrar a pendência no P0 antes das etapas
dependentes do P1. Não presumir que os caminhos propostos nos planos já existem ou que a
instalação já foi executada.

## 4. Restrições permanentes

- Arquivos próprios em L:\Sistemas\Doodba; ferramentas de desenvolvimento executadas no
  Linux do container. Editor pode permanecer no Windows.
- Uma imagem final de aplicação e um container de execução; sem Docker-in-Docker, socket
  Docker montado ou serviços adicionais.
- Cada entrada operacional pelo script do projeto verifica e para containers externos
  ativos no contexto local, sem remover seus dados.
- Não instalar monitoramento permanente nem alterar reinício de outros projetos.
- Não aumentar versões principais ou adicionar módulos fiscais por conveniência.
- Não publicar Git, imagens ou PRs; usar fontes públicas para leitura e obtenção de
  código. Repositórios privados dependem de uma origem informada e acesso existente.
- Nenhuma credencial em manifests, configurações versionadas, imagens ou logs.

## 5. Etapas e entregas

### P1.1 — Mapear o fluxo das aulas para a arquitetura do P0

- [ ] Consultar as aulas Linux 3, 5, 6, 7 e 8 e registrar o que foi verificável.
- [ ] Inspecionar os arquivos de configuração de repositórios, addons e tarefas da
      revisão Doodba escolhida no P0.
- [ ] Separar comandos reutilizáveis de comandos que tentariam criar a stack Compose.
- [ ] Definir o equivalente para container único, sem substituir o uso real do Doodba.
- [ ] Registrar cada diferença e versões não especificadas em .agent/docs/FONTES-P1.md.

Entrega: tabela aula/procedimento original/adaptação/comando validado.

### P1.2 — Workspace e execução das ferramentas

- [ ] Criar workspace local do VS Code apontando para código e configuração existentes.
- [ ] Configurar tarefas que chamem scripts/doodba.ps1, incluindo verificação de
      exclusividade antes de shell, execução, testes e depuração.
- [ ] Executar ferramentas Python e Invoke dentro do container; não depender de
      instalação Python no Windows.
- [ ] Reutilizar tarefas Invoke compatíveis ou adaptar tarefas específicas com
      documentação, sem executar comandos Compose que criem outros containers.
- [ ] Evitar processos Odoo duplicados ao iniciar uma tarefa de desenvolvimento.
- [ ] Documentar o caminho Windows e seu correspondente Linux para cada mount.

Entrega: workspace, tarefas e guia de entrada no ambiente. Abrir um arquivo no editor
não é automaticamente interceptável pelo script; documentar o comando oficial de
abertura/operação e não prometer exclusividade fora desse fluxo.

### P1.3 — Addons próprios e OCA

- [ ] Organizar addons próprios e fontes externas conforme os caminhos reais do P0.
- [ ] Preservar checkout de terceiros sem inserir documentação própria em cada pasta.
- [ ] Registrar URL, branch compatível 14.0, commit e licença das fontes selecionadas.
- [ ] Selecionar um addon OCA pequeno para validar o fluxo; priorizar o exemplo da aula
      se confirmado e compatível. Documentar qualquer substituição.
- [ ] Declarar repositório e seleção de addons no mecanismo Doodba identificado.
- [ ] Verificar dependências transitivas e evitar carregar todos os addons de um
      repositório quando apenas um foi escolhido.
- [ ] Configurar o caminho de addons, atualizar catálogo e instalar o addon selecionado
      somente no banco de desenvolvimento/teste.
- [ ] Reservar estrutura para addons privados locais sem inventar URL ou solicitar
      credenciais para um repositório que o usuário ainda não indicou.

Entrega: um addon OCA instalado e rastreável, e caminho funcional para código próprio.

### P1.4 — Repositórios e referências de PR

- [ ] Implementar sincronização explícita a partir das declarações de fontes.
- [ ] Bloquear sobrescrita de alterações locais; registrar conflito antes de atualizar.
- [ ] Usar commits fixados para reprodução; não buscar automaticamente o último conteúdo
      remoto a cada inicialização.
- [ ] Documentar como aplicar uma referência de PR em checkout local, inspecionar o diff
      e voltar ao commit anterior, conforme o mecanismo suportado.
- [ ] Se o PR da aula não puder ser confirmado ou não for compatível, registrar essa
      limitação e validar o mecanismo com referências locais controladas; não aplicar um
      PR arbitrário ao ambiente.
- [ ] Manter backup e estratégia de retorno antes de alterações de módulos que
      modifiquem o banco; reverter Git sozinho não desfaz alterações no banco.

Entrega: procedimento reproduzível de sincronização e experimentação, sem publicação.

### P1.5 — Configuração Odoo e dependências

- [ ] Documentar quais opções são geradas pelo Doodba e quais pertencem ao projeto.
- [ ] Validar precedência de arquivos, variáveis e argumentos efetivamente usados.
- [ ] Declarar dependências Python e de sistema nos arquivos apropriados da base
      adotada, fixando versões compatíveis quando possível.
- [ ] Fazer dependências permanentes entrarem no build; não depender de instalações
      manuais feitas apenas no container em execução.
- [ ] Validar reconstrução da imagem com as dependências declaradas.
- [ ] Manter acesso local e dados do P0 após a reconstrução.

Entrega: configuração explicada e dependências reproduzíveis.

### P1.6 — Ciclo completo de um módulo próprio

- [ ] Criar módulo técnico mínimo compatível com Odoo 14, com manifest, modelo, menu,
      view e permissões explícitas para usuário interno de teste.
- [ ] Instalar no banco de teste e criar um registro pela interface.
- [ ] Alterar um campo/view e atualizar apenas o módulo identificado, com banco
      explícito; não usar atualização indiscriminada de todos os módulos.
- [ ] Verificar a alteração na interface e a preservação do registro existente.
- [ ] Adicionar teste Odoo significativo para persistência/regra simples do módulo e
      validar permissões; evitar testes que apenas repetem a implementação.
- [ ] Rodar testes em banco separado no mesmo PostgreSQL/container, serializando
      execução e controlando o processo Odoo para evitar concorrência indevida.

Entrega: módulo de exemplo com evidência de instalação, atualização e teste Linux.

### P1.7 — Depuração e diagnóstico

- [ ] Escolher ferramenta de depuração compatível com o Python do P0 e registrar versão.
- [ ] Configurar mapeamento de caminhos do editor para o container.
- [ ] Habilitar debug somente em modo explícito de desenvolvimento, com porta publicada
      em loopback quando necessária e sem outro container.
- [ ] Demonstrar breakpoint em ação do módulo próprio, inspeção de variável e retomada.
- [ ] Garantir exclusividade antes de entrar no modo debug e impedir instâncias Odoo
      concorrentes não intencionais.
- [ ] Documentar logs e recuperação para erro de importação, dependência ausente,
      configuração inválida e falha na atualização do módulo.

Entrega: uma sessão de debug comprovada e um roteiro curto de diagnóstico.

### P1.8 — Validar repetibilidade e documentar

- [ ] Reconstruir/recriar o ambiente do projeto pelos arquivos declarados, preservando
      dados; não executar limpeza global de imagens ou cache.
- [ ] Comprovar permanência dos addons instalados, registro e anexo do teste.
- [ ] Reexecutar sincronização sem perder alterações locais e sem mudar commits fixados.
- [ ] Validar parada de container externo pelo fluxo operacional, conforme teste do P0.
- [ ] Ensaiar backup e restauração de banco/filestore em destino de teste separado no
      mesmo ambiente, sem sobrescrever o banco de desenvolvimento.
- [ ] Registrar comandos e resultados em .agent/docs/VALIDACAO-P1.md.
- [ ] Atualizar README.md, .agent/docs/VERSOES.md e documentação de cada pasta própria.

Entrega: sequência editável → instalável → testável → depurável → reproduzível.

## 6. Arquivos previstos

Complementar, sem substituir, os arquivos entregues pelo P0:

```text
desenvolvimento_odoo_doodba_p1_7a29c4e81b6.plan.md
doodba-local.code-workspace
.vscode/
  README.md
  tasks.json
  launch.json
scripts/
  doodba.ps1                  # extensão do ponto de entrada do P0
addons/
  README.md
  [módulo técnico de exemplo]/
    README.md
    __manifest__.py
    __init__.py
    models/
    security/
    views/
    tests/
.agent/docs/
  FONTES-P1.md
  DESENVOLVIMENTO.md
  ADDONS-E-REPOSITORIOS.md
  DEBUG.md
  VALIDACAO-P1.md
```

Os manifests de repositórios, addons e dependências usarão nomes/caminhos confirmados na
revisão Doodba do P0. A estrutura acima é proposta, não inventário. Pastas próprias
adicionadas receberão documentação proporcional ao seu conteúdo.

## 7. Critérios de aceite do P1

1. Partindo do P0, um desenvolvedor consegue abrir o workspace e usar o Linux sem
   instalar as ferramentas Python no Windows.
2. Todos os pontos de entrada entregues aplicam a exclusividade do Docker.
3. Há uma imagem final e um container de aplicação, mantendo Odoo 14/PostgreSQL 13.
4. Um addon OCA e um módulo próprio estão instalados e identificados por origem/versão.
5. Instalação, alteração, atualização, teste e breakpoint do módulo próprio funcionam.
6. Reconstrução não depende de alterações manuais efêmeras e não perde banco/filestore.
7. Sincronização respeita commits fixados e protege código local não salvo em Git.
8. Documentação distingue procedimentos comprovados nas aulas de adaptações propostas.

Cada critério terá evidência em .agent/docs/VALIDACAO-P1.md. Um guia escrito sem
execução dos fluxos não basta para declarar o P1 implementado.

## 8. Fora do P1

- Produção, deploy remoto, TLS, publicação de imagens, push ou abertura de PR.
- Atualização de versões principais, migração de dados empresariais e requisitos
  fiscais.
- Integrações externas, filas e serviços em containers adicionais.
- Acesso a repositórios privados não identificados pelo usuário.
- Aplicação de PR específico não verificado, atualização automática de dependências e
  alteração global do Docker Desktop ou de configurações pessoais do editor.

## 9. Ordem e impedimentos

Executar P1.1 → P1.2 → P1.3 → P1.4 → P1.5 → P1.6 → P1.7 → P1.8. Se fontes estiverem
indisponíveis, registrar a lacuna e usar documentação primária para uma adaptação
explicitamente identificada; não afirmar reprodução fiel. Se houver incompatibilidade
que exija alterar Odoo 14, PostgreSQL 13 ou container único, interromper a etapa
dependente e apresentar o conflito concreto ao usuário.

## Convenção atual de armazenamento

Planos e registros de execução: .agent/plan/. Documentação e fontes: .agent/docs/.
Habilidades comprovadas: .agent/skills/. Regras: .agent/rules/. As árvores ilustrativas
acima devem ser interpretadas conforme essa convenção; README técnico proposto para
pasta própria será documentado em .agent/docs/, exceto o README de apresentação da raiz.
Consulte ../rules/ORGANIZACAO.md.

Registro: plano migrado para .agent/plan; fase continua planejada, sem implementação.
