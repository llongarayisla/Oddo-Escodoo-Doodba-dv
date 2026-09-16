# P0 — Ambiente local Odoo 14 com Doodba em container Linux único

Status: implementado e validado em 2026-09-16. Evidências:
[VERSOES.md](../docs/VERSOES.md), [ARQUITETURA.md](../docs/ARQUITETURA.md),
[VALIDACAO-P0.md](../docs/VALIDACAO-P0.md), [OPERACAO.md](../docs/OPERACAO.md).

## 1. Objetivo e definição de P0

P0 é a primeira entrega funcional: construir e iniciar, a partir deste repositório, um
ambiente Linux com Odoo 14 e PostgreSQL 13 dentro de uma única imagem final e um único
container. O ambiente deve permitir acessar o Odoo, entrar em um shell Linux e preservar
banco de dados e filestore após reinício e recriação do container.

O uso do Doodba precisa ser real e rastreável: identificar a imagem-base, os scripts e
as configurações efetivamente reaproveitados. Não chamar uma instalação manual genérica
de Odoo de instalação Doodba.

## 2. Fontes e grau de confirmação

| Fonte                                                                                      | Evidência disponível                                                                                                                | Uso no P0                                                      |
| ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| Instruções do usuário e AGENTS.md                                                          | Windows como host; Linux em Docker; imagem/container únicos; exclusividade; documentação local                                      | Requisitos obrigatórios                                        |
| .agent/rules/REGRAS-DE-NEGOCIO.md                                                          | Registro das regras e das adaptações necessárias                                                                                    | Restrições de arquitetura                                      |
| .agent/docs/INSTALACAO.md                                                                  | Inspeção do host, Docker iniciado e limpeza realizada                                                                               | Estado inicial registrado                                      |
| Playlist Escodoo: https://www.youtube.com/playlist?list=PLs5WR750kjpdPxmU8vE-nIX1flWABqFvu | Títulos, sequência e descrição consultados                                                                                          | Ordem de preparação, criação, workspace, addons e configuração |
| Aula Linux 4: https://www.youtube.com/watch?v=AJKrmk55bEo                                  | Transcrição automática consultada: Odoo 14 em aproximadamente 00:43; PostgreSQL 13 em aproximadamente 01:36; uso do Copier Template | Versões principais e origem do projeto                         |
| Aula Linux 2: https://www.youtube.com/watch?v=mHRIQv10uRY                                  | Tema identificado; conteúdo técnico completo ainda não confirmado                                                                   | Consultar preparação e ferramentas antes de fixar versões      |
| Aula Linux 5: https://www.youtube.com/watch?v=GrcQGAY6kqU                                  | Tema identificado; conteúdo técnico completo ainda não confirmado                                                                   | Consultar workspace e Invoke                                   |
| https://github.com/Tecnativa/doodba-copier-template                                        | README consultado: geração com Copier, dependências e fluxo do template                                                             | Inspecionar uma revisão compatível e registrar adaptações      |

Documentação oficial do Doodba, Docker e PostgreSQL deverá ser consultada durante a
implementação para decisões específicas ainda não verificadas. Ela será registrada como
fonte complementar, sem ser atribuída aos vídeos.

Confirmado: Odoo 14 e PostgreSQL 13. Ainda não confirmado: distribuição Linux da aula,
Python exato, revisão do template, versões de Copier/Invoke e revisão do código Odoo.
Não assumir que o template atual reproduz o template usado na gravação. Quando a aula
não fixar uma versão, registrar a escolha compatível como decisão de implementação, com
justificativa e versão efetivamente instalada.

## 3. Estado inicial conhecido

- Diretório: L:\Sistemas\Doodba.
- Há documentação, mas ainda não há Dockerfile, imagem ou instalação Odoo.
- A inspeção inicial não encontrou repositório Git; verificar novamente antes de
  inicializá-lo. Não criar remoto, publicar ou fazer push.
- Docker Desktop 4.81.0 / Engine 29.6.1, Linux amd64, contexto desktop-linux, conforme
  última verificação; essas versões são do host, não do curso.
- A última limpeza terminou com zero imagens e zero containers ativos.
- Oito containers parados, dez volumes e cache de build foram preservados.
- Revalidar esse estado na execução; não usar o registro como garantia atual.

## 4. Arquitetura pretendida

Windows / PowerShell -> script de operação local e verificação de exclusividade ->
Docker Desktop, contexto local desktop-linux -> uma imagem final doodba-local:14-pg13 ->
um container doodba-local -> supervisor de processos / tratamento de sinais ->
PostgreSQL 13, comunicação interna -> Odoo 14 com componentes Doodba identificados ->
shell e ferramentas Linux de desenvolvimento

- Sem daemon Docker dentro do container e sem montagem do socket Docker.
- Sem PostgreSQL, Redis ou proxy em containers adicionais.
- HTTP do Odoo publicado somente em 127.0.0.1:8069, se a porta estiver livre.
- Banco sem publicação de porta no host no P0; acesso por shell interno.
- Verificar antes de reservar qualquer nome, porta, diretório ou volume.
- Odoo e PostgreSQL devem executar com usuários próprios, sem usar root para os
  processos de aplicação e banco.
- A imagem-base proposta é uma variante Doodba compatível com Odoo 14, cuja
  disponibilidade, distribuição e entrypoint serão inspecionados antes da escolha. Não
  existe ainda uma tag/digest validado neste projeto.
- O resultado terá uma imagem final de aplicação. Camadas e cache de build são artefatos
  internos do Docker, não serviços adicionais.

## 5. Etapas de implementação

### P0.1 — Consolidar versões e viabilidade

- [x] Conferir fontes das aulas e recuperar comandos legíveis disponíveis.
- [x] Inspecionar revisão compatível do Copier Template e da imagem Doodba.
- [x] Verificar Python, dependências de sistema e instalação do PostgreSQL 13 na
      distribuição da imagem candidata.
- [x] Registrar tags, digests, commits e versões em .agent/docs/VERSOES.md.
- [x] Mapear o que será mantido do Doodba e o que precisará ser adaptado.
- [x] Documentar em .agent/docs/ARQUITETURA.md a diferença entre o fluxo Compose das
      aulas e a execução de múltiplos processos em um só container.

Saída: matriz de versões e estratégia viável. Se não houver base compatível, registrar o
impedimento antes de construir uma solução diferente. Não alterar Odoo 14/PostgreSQL 13
silenciosamente nem executar a stack convencional.

### P0.2 — Estruturar o repositório e a exclusividade

- [x] Inicializar Git local se ainda ausente; não configurar remoto.
- [x] Criar .gitignore, .dockerignore e regras LF para arquivos shell/Linux.
- [x] Criar scripts/doodba.ps1 como entrada para build, start, stop, restart, shell,
      logs e status; comandos de validação usarão a mesma verificação.
- [x] Fixar explicitamente o contexto local desktop-linux e identificar o container do
      projeto por nome e label, não por correspondência parcial.
- [x] Listar containers ativos, parar os externos com docker stop e verificar novamente
      que nenhum externo permanece ativo antes de prosseguir.
- [x] Se o Docker não responder, houver colisão de identidade ou alguma parada falhar,
      terminar com erro e não executar a operação seguinte.
- [x] Preservar todos os containers/volumes externos e não reiniciá-los ao sair.
- [x] Não incluir prune ou remoção forçada de imagens na rotina de operação: a limpeza
      anterior foi uma solicitação pontual.
- [x] Documentar que operações pelo Docker Desktop ou comandos manuais fora do script
      não são interceptadas; não há monitoramento contínuo.

Saída: operações do projeto passam pela regra de exclusividade. Na manutenção feita pelo
agente, aplicar a mesma checagem antes de trabalhar no ambiente.

### P0.3 — Construir a imagem única

- [x] Criar Dockerfile com a base Doodba validada e versões registradas.
- [x] Instalar PostgreSQL 13 e dependências necessárias dentro dessa imagem.
- [x] Preservar/reutilizar mecanismos Doodba compatíveis de código, addons e
      configuração; evitar executar tarefas Invoke que levantem a stack antiga.
- [x] Implementar entrada e supervisão: preparar diretórios, iniciar PostgreSQL,
      aguardar prontidão e iniciar Odoo em seguida.
- [x] Encaminhar sinais de parada e encerrar o banco de forma controlada.
- [x] Fazer a falha de um serviço essencial aparecer no estado/healthcheck do container;
      não mascarar falhas com um processo de espera infinito.
- [x] Registrar logs úteis para diagnóstico e acesso a shell Linux.

Saída: uma imagem final que contém ambos os serviços e pode ser reconstruída pelos
arquivos versionados. Registrar dependências não totalmente fixáveis.

### P0.4 — Persistência e configuração local

- [x] Definir persistência para PostgreSQL e filestore antes de inicializar o banco.
- [x] Validar permissões, locks e semântica de arquivos no armazenamento escolhido.
- [x] Preferir dados do projeto em caminhos locais somente se o bind mount Windows
      suportar corretamente o PostgreSQL; não forçar PGDATA em NTFS quando isso quebrar
      permissões ou inicialização.
- [x] Se necessário, usar volume Linux nomeado exclusivo do projeto, documentando que
      reside no armazenamento gerenciado do Docker Desktop. Configuração, scripts e
      backups continuam neste repositório. Não mover o armazenamento global do Docker
      nem usar volumes existentes de outros projetos.
- [x] Separar credencial do banco, senha mestra Odoo e usuário da aplicação; gerar
      valores locais fora do Git e fornecer apenas .env.example sem segredos.
- [x] Inicializar banco e usuário de forma idempotente, sem apagar dados existentes.
- [x] Configurar addons próprios e configuração Odoo em diretórios documentados.
- [x] Publicar somente o acesso HTTP local e registrar a URL de uso.

Saída: configuração local com persistência explícita e sem segredos no build, no Git ou
nos documentos de evidência.

### P0.5 — Verificar a entrega funcional

- [x] Build final concluído sem erros.
- [x] Confirmar Odoo 14, PostgreSQL 13 e versões efetivas dentro do container.
- [x] Confirmar exatamente um container do projeto em execução e nenhum externo.
- [x] Confirmar banco pronto e conexão do Odoo funcionando.
- [x] Inicializar um banco de desenvolvimento e verificar login real no navegador; uma
      resposta HTTP 200 isolada não comprova instalação funcional.
- [x] Criar registro e anexo descartáveis para verificar banco e filestore.
- [x] Reiniciar o container e verificar registro e anexo.
- [x] Recriar somente o container do projeto, preservando dados, e repetir a consulta.
- [x] Verificar shell Linux, logs e parada controlada de ambos os serviços.
- [x] Testar exclusividade com um container temporário identificado, usando a mesma
      imagem final, e comprovar que o script o para sem remover seus recursos. Remover
      ao fim somente esse recurso de teste criado para a validação.
- [ ] Verificar que falhas de inspeção/parada bloqueiam a operação dependente.

Saída: evidências em .agent/docs/VALIDACAO-P0.md, com comandos, resultados e limitações.

### P0.6 — Documentar operação e recuperação

- [x] Atualizar README.md com início rápido, URL e comandos de operação.
- [x] Atualizar .agent/docs/INSTALACAO.md a cada etapa efetivamente executada.
- [x] Adicionar README.md às pastas próprias docker/, scripts/, config/ e addons/.
- [x] Documentar persistência, backup conjunto de banco/filestore e recuperação sem
      sugerir remoção de volumes como solução padrão.
- [x] Registrar todos os desvios em relação às aulas e pontos não confirmados.
- [x] Atualizar este plano com o estado real, sem marcar pendências como concluídas.

## 6. Estrutura prevista de entrega

```text
estrutura_odoo_doodba_f884730d532.plan.md
AGENTS.md
README.md
.gitignore
.dockerignore
.gitattributes
.env.example
Dockerfile
docker/
  README.md
  entrypoint.sh
  healthcheck.sh
  [configuração do supervisor escolhido]
scripts/
  README.md
  doodba.ps1
config/
  README.md
  [configuração Odoo sem segredos]
addons/
  README.md
.agent/docs/
  REGRAS-DE-NEGOCIO.md
  INSTALACAO.md
  VERSOES.md
  ARQUITETURA.md
  VALIDACAO-P0.md
```

Diretórios gerados ou copiados do Doodba podem complementar essa estrutura após inspeção
do template. Documentar a origem; não sobrescrever estas regras.

## 7. Critério de conclusão do P0

P0 só está concluído quando o Odoo 14 pode ser usado pelo navegador local, com
PostgreSQL 13 no mesmo container, persistência validada após recriação, operações
protegidas pela exclusividade e documentação suficiente para repetir o procedimento
neste projeto. Somente criar arquivos ou obter um build verde não encerra o P0.

## 8. Fora do P0

- Deploy remoto, publicação de imagem, domínio, TLS e ambiente de produção.
- Migração de versões ou instalação de Odoo/PostgreSQL mais recentes.
- Localização fiscal brasileira, módulos de negócio e importação de dados reais.
- Reprodução de todos os exemplos de addons/PRs da playlist.
- CI/CD, observabilidade externa e automações permanentes no Windows.
- Limpeza adicional de containers, volumes ou cache de outros projetos.
- Configuração de um desktop Linux completo: a experiência de VM solicitada será
  atendida por ambiente persistente, serviços e shell Linux no container.

## Convenção atual de armazenamento

Planos e registros de execução: .agent/plan/. Documentação e fontes: .agent/docs/.
Habilidades comprovadas: .agent/skills/. Regras: .agent/rules/. As árvores ilustrativas
acima devem ser interpretadas conforme essa convenção; README técnico proposto para
pasta própria será documentado em .agent/docs/, exceto o README de apresentação da raiz.
Consulte ../rules/ORGANIZACAO.md.

Registro: implementado em 2026-09-16. README técnico das pastas próprias ficou em
`.agent/docs/PASTAS.md`, não em README.md dentro de cada pasta. Login web validado por
sessão HTTP (CSRF + cookie) e XML-RPC; não havia ferramenta de navegador neste agente.
Pendência restante de ensaio: falha injetada de inspect/stop. Código já aborta nesses
casos.
