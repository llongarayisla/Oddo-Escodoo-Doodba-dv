# P2 — Seleção e configuração dos módulos de negócio

Status: planejado; levantamento funcional e implementação não iniciados. Dependências
técnicas: [P0](estrutura_odoo_doodba_f884730d532.plan.md) e
[P1](desenvolvimento_odoo_doodba_p1_7a29c4e81b6.plan.md) concluídos e validados. Nesta
etapa, somente este plano é entregue.

## 1. Objetivo

Definir quais processos o Odoo atenderá e entregar um primeiro conjunto de módulos
configurados, com permissões e fluxos de negócio validados em ambiente local de
homologação. O resultado será uma configuração reproduzível baseada em requisitos
identificados, sem instalar conjuntos de módulos por suposição.

P0 entrega a infraestrutura; P1 entrega o fluxo de desenvolvimento; P2 aplica essa base
a um recorte funcional acordado com o usuário. O escopo de negócio ainda não foi
informado e será definido na primeira etapa de execução do P2.

## 2. Fontes e limites

| Fonte                                                                                        | O que sustenta                                                | Limite                                                    |
| -------------------------------------------------------------------------------------------- | ------------------------------------------------------------- | --------------------------------------------------------- |
| Solicitação do usuário para o P2                                                             | Planejamento de módulos de negócio                            | Não define setor, processos ou módulos específicos        |
| AGENTS.md e .agent/rules/REGRAS-DE-NEGOCIO.md                                                | Repositório local, container único e exclusividade            | Não são requisitos funcionais da empresa                  |
| Planos P0/P1 e .agent/docs/INSTALACAO.md                                                     | Base técnica planejada e versões confirmadas                  | Implementação ainda não concluída                         |
| [Playlist Escodoo](https://www.youtube.com/playlist?list=PLs5WR750kjpdPxmU8vE-nIX1flWABqFvu) | Preparação do ambiente, addons, repositórios e dependências   | Não demonstra quais módulos atendem ao negócio do usuário |
| [Aula Linux 4](https://www.youtube.com/watch?v=AJKrmk55bEo)                                  | Odoo 14 e PostgreSQL 13 confirmados na transcrição consultada | Não comprova versões de addons de negócio                 |

Na execução, consultar documentação oficial Odoo 14 e README, manifest, dependências,
testes e licença de cada addon candidato. Consultar repositórios OCA específicos apenas
conforme os requisitos. Registrar URL, revisão e data em .agent/docs/p2/FONTES.md; não
apresentar uma compatibilidade como verificada antes de inspecionar e testar o código
correspondente.

Localização brasileira é uma possibilidade, não uma seleção já realizada. Se necessária,
verificar as fontes técnicas e os requisitos fiscais aplicáveis na ocasião. Este plano
não contém orientação tributária nem presume conformidade.

## 3. Regras preservadas

- Odoo 14, PostgreSQL 13, uma imagem final e um container Linux do projeto.
- Arquivos próprios em L:\Sistemas\Doodba e ferramentas executadas no Linux.
- Operações pelo ponto de entrada do P0/P1, verificando e parando outros containers
  locais antes de trabalhar no ambiente, sem remover seus dados.
- Nenhum serviço adicional, publicação, deploy ou atualização de versão principal.
- Banco de homologação separado logicamente no mesmo PostgreSQL/container; não criar
  outro container para homologação ou testes.
- Dados sintéticos e usuários de teste; sem importar dados reais nesta fase.
- E-mails externos, webhooks, pagamentos e transmissões fiscais não serão ativados no
  ensaio local. Testar resultados internos sem produzir efeitos externos.
- Credenciais e dados de instância fora do Git; documentação sem segredos.

## 4. Pré-requisitos e decisões pendentes

O levantamento P2.1 pode começar antes da implementação técnica. Instalações e
homologação dependem de P0/P1 validados, incluindo backup/recuperação, sincronização de
fontes, atualização de módulo e testes.

Na execução do levantamento, obter as informações necessárias:

| Decisão         | Informação necessária                            | Impacto                     |
| --------------- | ------------------------------------------------ | --------------------------- |
| Recorte inicial | Processo prioritário e problema a resolver       | Limita módulos e cenários   |
| Organização     | Empresas/unidades envolvidas e operação desejada | Cadastros e isolamento      |
| Operadores      | Papéis e responsabilidades                       | Grupos, acesso e aprovações |
| Fluxo           | Etapas, entradas, saídas, exceções e regras      | Configuração e aceite       |
| Localidade      | País, idioma, moeda e necessidade fiscal         | Localização e dependências  |
| Entrega         | Quem valida e qual resultado comprova sucesso    | Homologação                 |

Exemplos de áreas a discutir: CRM/vendas, compras, estoque, serviços/projetos ou
financeiro. São alternativas de levantamento, não módulos selecionados. Não presumir
regime tributário, CNPJ, múltiplas empresas ou edição Enterprise.

## 5. Etapas de execução

### P2.1 — Definir o recorte funcional

- [ ] Levantar o processo prioritário, responsáveis e resultado esperado.
- [ ] Descrever cenário principal e exceções relevantes em linguagem de negócio.
- [ ] Separar necessidades obrigatórias de melhorias posteriores.
- [ ] Registrar requisitos com identificadores REQ-P2-001, REQ-P2-002 etc.
- [ ] Para cada requisito, definir ator, entrada, ação, saída e critério de aceite.
- [ ] Preparar proposta concreta de escopo para validação do usuário, antes de executar
      instalações dependentes de decisões funcionais ainda ausentes.

Entrega: .agent/docs/p2/REQUISITOS.md com recorte, prioridades e decisões pendentes.
Informação ausente continua pendente; não substituir por resposta inventada.

### P2.2 — Selecionar módulos e mapear lacunas

- [ ] Relacionar cada requisito às funcionalidades nativas disponíveis na versão e
      edição instaladas, conferindo nomes técnicos no código.
- [ ] Avaliar addons OCA apenas para lacunas concretas do recorte.
- [ ] Registrar nome técnico, origem, branch/revisão, licença e dependências.
- [ ] Verificar compatibilidade real com Odoo 14 e Python do P0, incluindo dependências
      transitivas e necessidade de serviços externos.
- [ ] Identificar opções que exigem licença, contrato, credencial ou mudança
      arquitetural; não adquirir, ativar ou contornar essas exigências.
- [ ] Classificar cada requisito: configuração padrão, addon adicional, pequena
      customização ou fora do recorte.
- [ ] Manter explícitas as alternativas rejeitadas e seus motivos quando relevantes para
      compreender a escolha final.

Entrega: .agent/docs/p2/MATRIZ-MODULOS.md com relação requisito → módulo/configuração →
revisão → dependências → cenário de aceite. Não instalar antes dessa seleção.

### P2.3 — Preparar homologação e ponto de recuperação

- [ ] Revalidar saúde e exclusividade do ambiente pelo script do projeto.
- [ ] Inventariar módulos e configurações existentes do P0/P1.
- [ ] Criar backup conjunto de banco/filestore antes de mudanças no banco existente.
- [ ] Preparar banco de homologação com nome explícito, separado do banco de
      desenvolvimento e sem copiar dados privados de outros projetos.
- [ ] Garantir que ações agendadas e integrações dos módulos selecionados não enviem
      mensagens nem executem transações externas durante os testes.
- [ ] Criar conjunto mínimo de dados sintéticos e papéis de teste.
- [ ] Registrar como retornar ao estado anterior, incluindo banco e filestore;
      desinstalar módulo ou reverter Git não será tratado como restauração completa.

Entrega: homologação isolada logicamente e roteiro verificável de recuperação.

### P2.4 — Instalar e parametrizar o recorte

- [ ] Declarar fontes e addons no mecanismo Doodba validado pelo P1, com commits
      fixados.
- [ ] Declarar dependências permanentes no build da única imagem de aplicação.
- [ ] Instalar módulos na ordem necessária, somente no banco explicitamente escolhido.
- [ ] Configurar cadastros, sequências, estágios e regras que os requisitos demandarem.
- [ ] Registrar idioma, moeda, unidades e demais parâmetros apenas quando definidos.
- [ ] Criar grupos/permissões conforme os papéis, evitando depender de administrador
      para o uso normal do fluxo.
- [ ] Registrar configurações manuais e automatizar as repetíveis sem incorporar dados
      de teste, credenciais ou identificadores específicos da instância.
- [ ] Se houver lacuna que exija customização, descrever o comportamento primeiro;
      implementar apenas o mínimo incluído no recorte, com testes correspondentes.

Entrega: módulos configurados e instruções para repetir a configuração.

### P2.5 — Localização brasileira, se necessária

Esta etapa será marcada como não aplicável se não fizer parte dos requisitos.

- [ ] Distinguir idioma/cadastros brasileiros de requisitos contábeis e fiscais.
- [ ] Identificar o conjunto mínimo de addons compatíveis com a necessidade definida.
- [ ] Verificar documentação e revisão das fontes e registrar limitações conhecidas.
- [ ] Levantar parâmetros fiscais junto ao responsável indicado pelo usuário; não
      inferir impostos ou enquadramento tributário.
- [ ] Validar apenas configurações e exemplos locais sintéticos do recorte.
- [ ] Registrar como dependência de fase posterior qualquer certificado, transmissão,
      provedor ou integração externa necessária.

Entrega: aplicabilidade e configuração local documentadas. Não declarar emissão fiscal
ou conformidade integral validadas apenas porque um addon foi instalado.

### P2.6 — Homologar os processos e permissões

- [ ] Executar o cenário principal de cada requisito e registrar resultado.
- [ ] Verificar exceções pertinentes: dados ausentes, operação inválida, cancelamento e
      duplicidade, conforme as regras definidas.
- [ ] Testar com usuários dos papéis reais planejados, incluindo tentativa de acesso
      indevido; usar mais de uma empresa somente se fizer parte do escopo.
- [ ] Conferir documentos, estados, valores e relacionamentos gerados pelo fluxo.
- [ ] Se houver cálculo financeiro/fiscal no recorte, comparar com resultado esperado
      fornecido/validado pelo responsável, sem criar taxas presumidas.
- [ ] Corrigir falhas e repetir os cenários afetados.
- [ ] Apresentar evidências e registrar o aceite funcional do usuário ou responsável;
      validação técnica pelo agente não equivale a aceite funcional automático.

Entrega: .agent/docs/p2/VALIDACAO-P2.md com requisito, cenário, esperado, observado,
evidência, resultado e responsável pelo aceite.

### P2.7 — Verificar reprodução e entregar operação

- [ ] Repetir instalação/configuração em banco de teste limpo no mesmo container,
      preservando os bancos existentes e os demais recursos do Docker.
- [ ] Verificar comportamento dos módulos após reinício/recriação pelo fluxo do P0/P1.
- [ ] Testar atualização controlada de eventual módulo próprio, sem perder registros.
- [ ] Confirmar que continuamos com um container e sem serviços externos necessários
      ocultos para os cenários declarados como concluídos.
- [ ] Atualizar .agent/docs/VERSOES.md e os manifests com revisões efetivamente
      utilizadas.
- [ ] Documentar operação por papel, configuração, diagnóstico e recuperação.
- [ ] Registrar lacunas e encaminhar integrações/importações futuras ao P3 e preparação
      de produção ao P4, sem expandir silenciosamente o P2.

Entrega: configuração homologada, reproduzível e com limitações explícitas.

## 6. Arquivos previstos

```text
modulos_negocio_odoo_doodba_p2_c93a6e702d1.plan.md
.agent/docs/
  VERSOES.md                     # atualizar documento de P0/P1
  p2/
    README.md
    FONTES.md
    REQUISITOS.md
    MATRIZ-MODULOS.md
    CONFIGURACAO.md
    OPERACAO.md
    VALIDACAO-P2.md
    PENDENCIAS.md
```

Atualizar manifests, configurações e scripts já entregues no P1, sem duplicar o ponto de
entrada. Código próprio adicional somente quando um requisito justificar, no diretório
de addons estabelecido, com README e testes adequados.

## 7. Critérios de conclusão

1. Recorte funcional definido com o usuário, sem decisões essenciais pendentes.
2. Todos os requisitos do recorte vinculados a módulos/configurações e cenários.
3. Fontes e revisões compatíveis verificadas e dependências reproduzíveis.
4. Cenários principais, exceções e permissões aprovados com evidências.
5. Configuração repetida em banco limpo, com dados existentes preservados.
6. Uma imagem final/container, versões principais e exclusividade mantidas.
7. Aceite funcional registrado e documentação suficiente para operar o recorte.

Se um requisito do recorte não puder ser atendido, registrar como pendente ou revisar
explicitamente o escopo com o usuário; não marcar o P2 como concluído apenas por
instalar módulos ou por finalizar este documento.

## 8. Fora do P2

- Integrações com outros sistemas, migração/importação de dados reais e sincronização.
- Emissão fiscal externa, transações financeiras e envio de comunicações reais.
- Implantação em produção, publicação de imagem, infraestrutura remota e TLS.
- Atualização das versões principais ou criação de containers adicionais.
- Compra de licenças ou contratação de provedores.
- Customização extensa sem requisito definido e validado no recorte.
- Limpeza global do Docker ou alteração de outros projetos.

## 9. Ordem e tratamento de impedimentos

Levantamento P2.1 → seleção P2.2 → preparação P2.3 → configuração P2.4 → localização
P2.5 quando aplicável → homologação P2.6 → reprodução P2.7.

Sem definição do processo, avançar apenas no levantamento e na organização das
evidências; não escolher módulos pelo usuário. Se uma necessidade exigir versão
diferente, serviço adicional ou licença indisponível, apresentar o conflito concreto e
alternativas antes de executar a parte dependente.

## Convenção atual de armazenamento

Planos e registros de execução: .agent/plan/. Documentação e fontes: .agent/docs/.
Habilidades comprovadas: .agent/skills/. Regras: .agent/rules/. As árvores ilustrativas
acima devem ser interpretadas conforme essa convenção; README técnico proposto para
pasta própria será documentado em .agent/docs/, exceto o README de apresentação da raiz.
Consulte ../rules/ORGANIZACAO.md.

Registro: plano migrado para .agent/plan; fase continua planejada, sem implementação.
