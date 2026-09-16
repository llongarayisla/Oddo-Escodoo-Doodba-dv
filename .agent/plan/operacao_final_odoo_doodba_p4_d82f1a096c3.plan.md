# P4 — Operação, recuperação e entrega final

Status: planejado; implementação e entrada em operação não iniciadas. Esta é a fase
final do roteiro P0–P4. Criar este plano não executa implantação, agendamentos, abertura
de portas ou ativação de integrações.

Dependências:

- [P0 — Infraestrutura](estrutura_odoo_doodba_f884730d532.plan.md).
- [P1 — Desenvolvimento](desenvolvimento_odoo_doodba_p1_7a29c4e81b6.plan.md).
- [P2 — Módulos de negócio](modulos_negocio_odoo_doodba_p2_c93a6e702d1.plan.md).
- [P3 — Integrações e dados](integracoes_dados_odoo_doodba_p3_b47e192ac80.plan.md).

## 1. Objetivo e limite da entrega

Consolidar o ambiente, verificar capacidade e controles de acesso, validar
backup/restauração e entregar procedimentos de operação e manutenção. Encerrar o projeto
com evidências de que os processos incluídos funcionam no cenário de uso definido, com
responsáveis, limites e recuperação conhecidos.

O alvo atualmente permitido é o ambiente local Windows/Docker deste projeto. Preparação
para produção não implica autorização para publicar o sistema. Acesso de rede, domínio,
TLS, hospedagem remota e cópia externa de backups dependem de definição específica e
devem respeitar as regras vigentes.

Se o objetivo final continuar sendo desenvolvimento local, concluir a entrega nesse
perfil, identificando itens de produção como não aplicáveis. Não declarar prontidão para
produção real com base apenas no funcionamento local.

## 2. Fontes e grau de confirmação

| Fonte                                                                                        | Uso no P4                                   | Limite                                                          |
| -------------------------------------------------------------------------------------------- | ------------------------------------------- | --------------------------------------------------------------- |
| AGENTS.md e .agent/rules/REGRAS-DE-NEGOCIO.md                                                | Restrições obrigatórias                     | Não definem disponibilidade, carga ou acesso de produção        |
| Planos P0–P3                                                                                 | Escopo e critérios das fases anteriores     | Planejamento não comprova implementação                         |
| .agent/docs/INSTALACAO.md                                                                    | Histórico disponível                        | Não comprova operação contínua                                  |
| [Playlist Escodoo](https://www.youtube.com/playlist?list=PLs5WR750kjpdPxmU8vE-nIX1flWABqFvu) | Origem do ambiente e das versões principais | Não comprova implantação de produção ou recuperação de desastre |

O P4 é complemento proposto ao curso. Na execução, consultar documentação oficial e
estado de suporte dos componentes efetivamente instalados, incluindo Odoo 14, PostgreSQL
13, imagem Linux, Docker Desktop e dependências. Registrar fontes, versões e data em
.agent/docs/p4/FONTES.md. Não presumir que versões antigas possuem suporte ou correções
disponíveis, nem trocar versões silenciosamente se surgir incompatibilidade com o uso
final.

## 3. Restrições que permanecem válidas

- Uma imagem final de aplicação e um container Linux do projeto.
- Código e configuração em L:\Sistemas\Doodba; sem publicação ou cópia remota do projeto
  sem solicitação específica.
- Odoo 14 e PostgreSQL 13 mantidos, com revisões efetivas registradas.
- Operações pelo ponto de entrada P0/P1 e sua verificação de exclusividade: parar outros
  containers locais, preservando recursos e dados.
- Não criar containers adicionais de proxy, banco, métricas ou backup.
- Não montar socket Docker ou executar daemon Docker dentro do container.
- Não alterar políticas globais de reinício de outros projetos.
- Não instalar monitoramento permanente sob as regras atuais. Verificações serão locais
  e sob demanda até que o usuário altere explicitamente essa regra.
- Não assumir autorização para transmissões reais, pagamentos, emissão fiscal ou
  mensagens externas a partir da aprovação de um plano técnico.

## 4. Decisões necessárias antes da execução dependente

| Tema            | Definição necessária                                              |
| --------------- | ----------------------------------------------------------------- |
| Perfil final    | Desenvolvimento local, operação interna ou produção               |
| Acesso          | Usuários, dispositivos, localidade e eventual necessidade de rede |
| Capacidade      | Usuários simultâneos, volume de dados e operações críticas        |
| Disponibilidade | Horário de uso e tolerância à parada                              |
| Recuperação     | Perda máxima aceitável de dados (RPO) e tempo de retorno (RTO)    |
| Backup          | Frequência, retenção, destino e responsável                       |
| Suporte         | Responsável por incidentes, manutenção e aceite                   |
| Integrações     | Quais fluxos do P3 realmente serão ativados e com que permissões  |

Não inventar metas numéricas ou prazos. Propor valores somente depois de conhecer o uso
e medir o ambiente, registrando o acordo com o usuário.

Um container concentra banco e aplicação no mesmo domínio de falha; não oferece alta
disponibilidade. A regra de parar outros containers também precisa ser compatível com o
uso final do host. Se os requisitos forem incompatíveis, apresentar o conflito antes de
prometer disponibilidade ou executar publicação.

## 5. Etapas de execução

### P4.1 — Consolidar o estado das fases anteriores

- [ ] Conferir evidências de P0/P1 e critérios funcionais de P2.
- [ ] Conferir P3 para as integrações/importações necessárias; registrar frentes não
      aplicáveis sem exigir conectores desnecessários.
- [ ] Inventariar imagem, digest, commits, módulos, configurações, dados e mounts.
- [ ] Consolidar pendências e distinguir impeditivos de melhorias futuras.
- [ ] Definir o perfil final e os critérios mensuráveis de aceite.
- [ ] Verificar suporte e manutenção disponíveis nas versões efetivas para esse perfil;
      registrar conflitos sem alterar Odoo/PostgreSQL por conta própria.

Entrega: .agent/docs/p4/PRONTIDAO.md com evidência por requisito e decisões pendentes.

### P4.2 — Revisar configuração operacional e acesso

- [ ] Separar configurações de desenvolvimento e operação sem criar outro container
      simultâneo ou outra arquitetura de aplicação.
- [ ] Desabilitar debug, dados de demonstração e tarefas de teste no perfil operacional.
- [ ] Confirmar usuários/grupos mínimos e acesso aos bancos necessários.
- [ ] Verificar segredos fora do Git, imagem, exemplos e logs.
- [ ] Revisar permissões de arquivos e execução dos serviços com usuários próprios.
- [ ] Manter banco sem porta publicada e HTTP restrito a loopback no perfil local.
- [ ] Definir tratamento do gerenciador de bancos, filtros de banco e endpoints
      administrativos de acordo com documentação da versão e uso escolhido.
- [ ] Caso acesso de rede seja requerido, apresentar desenho de portas, origem
      permitida, autenticação e TLS antes de alterar a exposição. Não adicionar proxy em
      outro container nem publicar túnel como solução automática.
- [ ] Testar login e negativa de acesso com usuários não administradores.

Entrega: configuração operacional documentada e verificada para o perfil definido.

### P4.3 — Backup consistente e retenção

- [ ] Inventariar banco, filestore, configuração e chaves necessárias à recuperação.
- [ ] Implementar backup pelo ponto de entrada existente, com exclusividade verificada.
- [ ] Garantir consistência entre banco e anexos por estratégia documentada: janela sem
      gravações ou outro mecanismo validado; pg_dump e cópia de arquivos em momentos
      arbitrários não serão considerados backup consistente.
- [ ] Incluir manifesto de versões e integridade, sem segredos em texto aberto.
- [ ] Gravar inicialmente em destino local do projeto excluído do Git/build.
- [ ] Medir duração, tamanho e espaço livre; detectar falha sem anunciar sucesso.
- [ ] Definir retenção com o responsável antes de implementar expiração automática.
- [ ] Proteger a última cópia validada e evitar excluir backups por padrão.
- [ ] Documentar que backup no mesmo host/disco não cobre perda do equipamento. Cópia
      externa depende de destino definido e autorização para os dados; enquanto ausente,
      registrar explicitamente o limite de recuperação.
- [ ] Se backup automático for necessário, preparar frequência, mecanismo, identidade e
      logs para revisão antes de habilitar a rotina. Não criar agendamento ou serviço
      permanente apenas pela existência deste plano.

Entrega: backup executável e política de retenção adequada ao perfil acordado.

### P4.4 — Ensaiar recuperação completa

- [ ] Restaurar backup em destino de teste separado dentro do mesmo ambiente, sem
      sobrescrever os dados correntes e sem criar outro container.
- [ ] Restaurar banco, filestore e configuração compatível com a revisão do backup.
- [ ] Validar login, registros, anexos, permissões e um fluxo essencial do P2.
- [ ] Manter integrações e ações agendadas desativadas no destino restaurado.
- [ ] Verificar checkpoints do P3 sem repetir efeitos externos já realizados.
- [ ] Medir RTO observado e comparar ponto recuperado com RPO definido.
- [ ] Simular procedimento de recuperação de container perdido com armazenamento
      preservado; não apagar volumes ou dados reais para realizar o ensaio.
- [ ] Documentar cenário de perda total do host, inclusive dependências ainda não
      satisfeitas, como cópia externa e disponibilidade dos artefatos.

Entrega: .agent/docs/p4/RECUPERACAO.md com passos testados, tempos e limitações.

### P4.5 — Diagnóstico, capacidade e manutenção

- [ ] Disponibilizar diagnóstico sob demanda para saúde de Odoo/PostgreSQL, espaço em
      disco, uso de recursos, logs e estado do último backup.
- [ ] Configurar limites/rotação de logs sem expor payloads sensíveis ou segredos.
- [ ] Testar carga representativa acordada usando dados sintéticos e sem requisições
      destrutivas ou transmissões a sistemas externos.
- [ ] Medir latência dos fluxos essenciais, consumo de memória/CPU e crescimento de
      dados; ajustar somente parâmetros justificados pelos resultados.
- [ ] Verificar comportamento em reinício controlado e parada dos serviços.
- [ ] Documentar dependência de Windows, Docker Desktop, sessão do usuário, suspensão do
      host e disponibilidade de disco para o uso escolhido.
- [ ] Definir atualização: revisão de mudanças, ensaio, backup, janela e retorno.
- [ ] Não instalar atualizações automáticas de addons ou dependências durante o uso.

Entrega: .agent/docs/p4/OPERACAO.md com limites medidos e rotina de manutenção.

### P4.6 — Preparar versão de entrega e retorno

- [ ] Registrar commits, digest da imagem de aplicação e manifestos de configuração.
- [ ] Demonstrar reconstrução a partir dos arquivos e dependências declaradas.
- [ ] Preservar meios de recuperar a versão anterior sem manter outro container ativo.
      Se necessário, planejar arquivo local de imagem fora do Git/build; não apagar a
      única versão recuperável antes da validação da nova.
- [ ] Documentar que voltar à imagem/código anterior não reverte alterações de esquema
      ou dados; coordenar retorno de banco e filestore.
- [ ] Para fluxos externos do P3, separar restauração local de compensação/ conciliação
      de efeitos externos, com operações especificamente autorizadas.
- [ ] Preparar checklist de mudança com duração prevista, responsáveis, testes após
      mudança, condição de falha e comando/procedimento de retorno.

Entrega: versão identificada e procedimento de atualização/retorno testável.

### P4.7 — Entrada em operação e aceite final

- [ ] Apresentar evidências e pendências concretas ao responsável pelo uso.
- [ ] Confirmar o perfil e o momento de entrada em operação real, se isso fizer parte do
      objetivo definido; não confundir criação do plano com essa decisão.
- [ ] Fazer backup de referência e aplicar somente a versão validada.
- [ ] Executar login, fluxo essencial, leitura de anexos e diagnóstico após mudança.
- [ ] Ativar integrações ou agendamentos apenas quando seu destino, comportamento e
      autorização estiverem definidos; manter os demais desabilitados.
- [ ] Acompanhar uma janela de validação acordada, sem instalar monitoramento permanente
      ou alterar regras globais do Docker.
- [ ] Registrar aceite ou executar retorno se algum critério impeditivo falhar.
- [ ] Atualizar README e situação real de todos os planos P0–P4.

Entrega: .agent/docs/p4/ENTREGA-FINAL.md e .agent/docs/p4/VALIDACAO-P4.md com aceite,
versão, responsáveis, acesso, procedimentos de suporte e limitações remanescentes.

## 6. Arquivos previstos

```text
operacao_final_odoo_doodba_p4_d82f1a096c3.plan.md
.agent/docs/p4/
  README.md
  FONTES.md
  PRONTIDAO.md
  BACKUP.md
  RECUPERACAO.md
  OPERACAO.md
  ATUALIZACAO-E-RETORNO.md
  VALIDACAO-P4.md
  ENTREGA-FINAL.md
```

Ampliar scripts/doodba.ps1 e arquivos já estabelecidos no P0/P1, preservando uma única
entrada operacional. Backups, exportações de imagem e dados reais ficarão em locais
documentados, excluídos do Git e do build. Não versionar credenciais ou arquivos de
backup como anexos de evidência.

## 7. Critérios de conclusão do P4 e do roteiro

1. Perfil final e critérios de disponibilidade/capacidade/recuperação definidos.
2. P0–P3 aplicáveis concluídos, com pendências impeditivas resolvidas.
3. Configuração operacional e permissões validadas para o acesso escolhido.
4. Backup consistente restaurado com registros e anexos comprovados.
5. RPO/RTO e capacidade medidos atendem ao uso acordado, ou o escopo é revisto
   explicitamente antes de declarar conclusão.
6. Versão de entrega e procedimento de retorno registrados e ensaiados.
7. Container único, exclusividade e versões obrigatórias preservados.
8. Responsável consegue operar, diagnosticar e seguir o roteiro de recuperação.
9. Aceite final registrado e README reflete o estado efetivamente entregue.

Se houver exigência de produção incompatível com versões, host local, container único ou
proibição de monitoramento permanente, registrar impedimento e alternativas. Não marcar
produção como pronta enquanto o requisito estiver sem solução. Uma entrega aceita como
desenvolvimento local deve ter esse nome.

## 8. Fora do escopo automático

- Mudança de versão principal, migração de arquitetura ou alta disponibilidade.
- Novos containers ou publicação remota do repositório/imagem.
- Exposição pública, alterações globais de firewall, DNS e contratação de serviços.
- Monitoramento permanente proibido pelas regras atuais.
- Envio de backups/dados a terceiros sem destino e autorização definidos.
- Limpeza global de Docker, remoção de dados ou interferência em outros projetos além da
  parada de containers já solicitada.

Esses itens não se tornam autorizados por serem mencionados como opções futuras. Se
necessários ao uso final, apresentar a necessidade e ajustar explicitamente o escopo
antes de executar.

## 9. Sequência final

P4.1 → P4.2 → P4.3 → P4.4 → P4.5 → P4.6 → P4.7.

Não é necessário criar P5 para encerrar o roteiro definido. Melhorias posteriores serão
registradas como backlog, sem impedir a entrega quando estiverem fora do recorte
acordado. Itens obrigatórios incompletos continuam pendentes, mesmo ao chegar à última
fase do planejamento.

## Convenção atual de armazenamento

Planos e registros de execução: .agent/plan/. Documentação e fontes: .agent/docs/.
Habilidades comprovadas: .agent/skills/. Regras: .agent/rules/. As árvores ilustrativas
acima devem ser interpretadas conforme essa convenção; README técnico proposto para
pasta própria será documentado em .agent/docs/, exceto o README de apresentação da raiz.
Consulte ../rules/ORGANIZACAO.md.

Registro: plano migrado para .agent/plan; fase continua planejada, sem implementação.
