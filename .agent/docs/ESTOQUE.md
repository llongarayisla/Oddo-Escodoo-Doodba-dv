# Documentação de Implementação e Operação: Inventário de TI no Odoo

Este documento compõe o guia completo de arquitetura, configuração inicial e operações
contínuas para a gestão do inventário de TI nas filiais **Porto Alegre** e **Itapuã**,
utilizando a estrutura nativa multi-company do Odoo.

---

## Sumário

1. [Estrutura do Projeto e Pré-Requisitos](#1-estrutura-do-projeto-e-pré-requisitos)
2. [Preparação e Configuração Geral](#2-preparação-e-configuração-geral)
3. [P0: Infraestrutura e Topologia Multi-Company](#3-p0-infraestrutura-e-topologia-multi-company)
4. [P1: Categorização e Rastreabilidade](#4-p1-categorização-e-rastreabilidade)
5. [P2: Cadastro do Catálogo de Produtos](#5-p2-cadastro-do-catálogo-de-produtos)
6. [P3: Carga Inicial e Ajustes de Estoque](#6-p3-carga-inicial-e-ajustes-de-estoque)
7. [P4: Validação e Fluxos Operacionais](#7-p4-validação-e-fluxos-operacionais)
8. [Guia de Resolução de Erros e Problemas Frequentes](#8-guia-de-resolução-de-erros-e-problemas-frequentes)

---

## 1. Estrutura do Projeto e Pré-Requisitos

A implementação cobre a gestão do ciclo de vida dos ativos de TI (Notebooks, Desktops,
Monitores) e consumíveis (Cabos, Periféricos), garantindo rastreabilidade
individualizada por Número de Série e isolamento correto por filial/empresa.

---

## 2. Preparação e Configuração Geral

Antes de iniciar o desenho topológico, assegure as definições básicas no Odoo:

### Passos de Preparação:

1. Acesse **Configurações > Usuários e Empresas > Empresas**.
2. Garanta que as duas filiais existam no cadastro:
   - `ISLA Sementes (Porto Alegre)`
   - `ISLA Sementes (Itapuã)`
3. Acesse **Inventário > Configuração > Configurações**:
   - Marque a opção **Multi-Armazéns** (_Multi-Warehouses_).
   - Marque a opção **Locais de Armazenamento** (_Storage Locations_).
   - Marque a opção **Lotes & Números de Série** (_Lots & Serial Numbers_).
4. Clique em **Salvar**.

---

## 3. P0: Infraestrutura e Topologia Multi-Company

Define a estrutura de armazéns físicos e locais virtuais para cada filial, além do local
de transição global.

### 3.1 Armazéns Físicos

- **Porto Alegre**:
  - **Nome**: `Armazém TI Porto Alegre` | **Nome Curto**: `AM-PA`
  - **Empresa**: `ISLA Sementes (Porto Alegre)`
- **Itapuã**:
  - **Nome**: `Armazém TI Itapuã` | **Nome Curto**: `AM-IT`
  - **Empresa**: `ISLA Sementes (Itapuã)`

### 3.2 Estrutura de Locais Internos

Vá em **Inventário > Configuração > Locais** e configure a árvore:

- **Porto Alegre (`ISLA Sementes (Porto Alegre)`)**:
  - `LOCAIS FÍSICOS/PA/Estoque TI/Disponível` (Local Interno)
  - `LOCAIS FÍSICOS/PA/Estoque TI/Manutenção ou Defeito` (Local Interno)
  - `LOCAIS FÍSICOS/PA/Estoque TI/Seminovos com Avaria` (Local Interno)
- **Itapuã (`ISLA Sementes (Itapuã)`)**:
  - `LOCAIS FÍSICOS/ITAP/Estoque TI/Disponível` (Local Interno)

### 3.3 Locais Virtuais e Transitórios

- **Alocações Virtuais (Por Empresa)**:
  - `LOCAIS VIRTUAIS / ALOCAÇÕES/Alocados - Porto Alegre` (Empresa:
    `ISLA Sementes (Porto Alegre)`)
  - `LOCAIS VIRTUAIS / ALOCAÇÕES/Alocados - Itapuã` (Empresa: `ISLA Sementes (Itapuã)`)
- **Trânsito Inter-Company (Global)**:
  - **Nome do Local**: `Trânsito Inter-Company`
  - **Local Pai**: `LOCAIS VIRTUAIS / ALOCAÇÕES`
  - **Tipo de Local**: `Local Transitório` (_Transit Location_)
  - **Empresa**: **EM BRANCO** (Essencial para permitir visibilidade em ambas as
    empresas).

---

## 4. P1: Categorização e Rastreabilidade

Configura as categorias de produto e suas regras de estoque/rastreamento.

### Passos de Configuração:

1. Acesse **Inventário > Configuração > Categorias de Produtos**.
2. **Equipamentos Seriados**:
   - **Nome**: `TI / Equipamentos Seriados`
   - **Estratégia de Remoção**: `FIFO`
3. **Consumíveis e Periféricos**:
   - **Nome**: `TI / Consumíveis e Periféricos`
   - **Estratégia de Remoção**: `FIFO`

---

## 5. P2: Cadastro do Catálogo de Produtos

Define as fichas dos produtos no catálogo global.

### Passos de Configuração:

1. Acesse **Inventário > Produtos > Produtos** e clique em **Criar**.

#### Produto 1: Notebook / Equipamento de Alto Valor

- **Nome**: `Notebook Dell Latitude 3420`
- **Tipo de Produto**: `Produto Estocável` (_Storable Product_) ou `Produto`
- **Categoria do Produto**: `TI / Equipamentos Seriados`
- **Aba Inventário > Rastreabilidade**: Selecione **Por Número de Série Único**.
- **Empresa**: Deixe em **Branco** (para permitir cadastro global).

#### Produto 2: Cabo / Insumo

- **Nome**: `Cabo HDMI 2.0 2m`
- **Tipo de Produto**: `Consumível` ou `Produto`
- **Categoria do Produto**: `TI / Consumíveis e Periféricos`
- **Aba Inventário > Rastreabilidade**: Selecione **Sem Rastreamento**.
- **Empresa**: Deixe em **Branco**.

---

## 6. P3: Carga Inicial e Ajustes de Estoque

Lançamento das quantidades físicas iniciais no sistema.

### Passo a Passo:

1. Acesse **Inventário > Operações > Ajustes de Estoque** e clique em **Criar**.
2. **Referência de Inventário**: Digite `Inventário Inicial TI - PA` ou
   `Inventário Inicial TI - IT`.
3. **Empresa**: Selecione a empresa correspondente (ex: `ISLA Sementes (Porto Alegre)`).
4. **Locais**: Escolha o local específico (ex:
   `LOCAIS FÍSICOS/PA/Estoque TI/Disponível`).
5. **Produtos Contados**: Selecione `Apenas selecionados manualmente`.
6. Clique em **Começar inventário**.
7. Clique em **Criar** na tabela de linhas:
   - **Para o Notebook**: Produto `Notebook Dell Latitude 3420`, digite o serial real em
     **Lote/Número de Série** e defina **Contado** = `1`.
   - **Para o Cabo**: Produto `Cabo HDMI 2.0 2m`, mantenha o serial vazio e defina
     **Contado** = quantidade física (ex: `15`).
8. Clique em **Validar inventário**.
9. Repita o procedimento alterando o seletor de empresa e o local para validar o estoque
   inicial de **Itapuã**.

---

## 7. P4: Validação e Fluxos Operacionais

Procedimento para as movimentações rotineiras do departamento de TI.

### 7.1 Fluxo 1: Atribuição de Equipamento a Colaborador

1. Vá em **Inventário > Operações > Transferências** e clique em **Criar**.
2. **Contato**: Selecione o colaborador.
3. **Tipo de Operação**: `Armazém TI Porto Alegre: Transferências Internas`.
4. **Local de Origem**: `LOCAIS FÍSICOS/PA/Estoque TI/Disponível`.
5. **Local do Destino**: `LOCAIS VIRTUAIS / ALOCAÇÕES/Alocados - Porto Alegre`.
6. Adicione o produto (`Notebook Dell Latitude 3420`), quantidade `1`.
7. Clique em **Salvar**, **Marcar como Para Fazer**, **Verificar Disponibilidade**,
   **Validar** e **Aplicar**.

### 7.2 Fluxo 2: Envio de Equipamento para Manutenção

1. Vá em **Inventário > Operações > Transferências** e clique em **Criar**.
2. **Tipo de Operação**: `Armazém TI Porto Alegre: Transferências Internas`.
3. **Local de Origem**: `LOCAIS FÍSICOS/PA/Estoque TI/Disponível`.
4. **Local do Destino**: `LOCAIS FÍSICOS/PA/Estoque TI/Manutenção ou Defeito`.
5. Adicione o item, clique em **Salvar**, **Marcar como Para Fazer**, **Verificar
   Disponibilidade**, **Validar** e **Aplicar**.

### 7.3 Fluxo 3: Transferência Inter-Company (Porto Alegre ↔ Itapuã)

```
[Porto Alegre / Disponível] ──(Etapa 1)──> [Trânsito Inter-Company] ──(Etapa 2)──> [Itapuã / Disponível]
```

- **Etapa 1: Saída de Porto Alegre**

  1. Empresa ativa no topo: **`ISLA Sementes (Porto Alegre)`**.
  2. Vá em **Inventário > Operações > Transferências > Criar**.
  3. **Tipo de Operação**: `Armazém TI Porto Alegre: Transferências Internas`.
  4. **Local de Origem**: `LOCAIS FÍSICOS/PA/Estoque TI/Disponível`.
  5. **Local do Destino**: `LOCAIS VIRTUAIS / ALOCAÇÕES/Trânsito Inter-Company`.
  6. Adicione o produto, defina a demanda, clique em **Salvar**, **Marcar como Para
     Fazer**, **Verificar Disponibilidade**, **Validar** e **Aplicar**.

- **Etapa 2: Entrada em Itapuã**
  1. Alterne a empresa no topo para **`ISLA Sementes (Itapuã)`**.
  2. Vá em **Inventário > Operações > Transferências > Criar**.
  3. **Tipo de Operação**: `Armazém TI Itapuã: Transferências Internas`.
  4. **Local de Origem**: `LOCAIS VIRTUAIS / ALOCAÇÕES/Trânsito Inter-Company`.
  5. **Local do Destino**: `LOCAIS FÍSICOS/ITAP/Estoque TI/Disponível`.
  6. Adicione o produto, defina a demanda, clique em **Salvar**, **Marcar como Para
     Fazer**, **Verificar Disponibilidade**, **Validar** e **Aplicar**.

---

## 8. Guia de Resolução de Erros e Problemas Frequentes

### ❌ Erro 1: Local da outra filial não aparece no Destino durante a transferência

- **Onde Ocorre**: P4 (Fluxo Inter-Company).
- **Causa**: O Odoo restringe a seleção de locais diretamente associados a outras
  empresas quando o Tipo de Operação pertence a uma empresa específica.
- **Solução**: Não tente selecionar o local físico final da outra empresa diretamente.
  Utilize o local virtual **`Trânsito Inter-Company`** conforme explicado na etapa
  [7.3](#73-fluxo-3-transferência-inter-company-porto-alegre--itapuã).

---

### ❌ Erro 2: "Erro de Usuário: Você não pode validar uma transferência se nenhuma quantidade for reservada ou concluída"

- **Onde Ocorre**: P4 (Validação de Transferências).
- **Causa**: O sistema está no status _Aguardando_ ou _Pronto_, mas nenhuma quantidade
  foi alocada/reservada.
- **Solução**:
  1. Feche o alerta clicando em **Ok**.
  2. Clique no botão roxo **Verificar Disponibilidade** no canto superior esquerdo.
  3. Certifique-se de que a coluna **Reservado** possui valor.
  4. Clique em **Validar** novamente e em **Aplicar**.

---

### ❌ Erro 3: Local de Trânsito não é exibido nas buscas de nenhuma empresa

- **Onde Ocorre**: P0 / P4.
- **Causa**: O local de trânsito foi gravado com uma empresa fixa vinculada no cadastro.
- **Solução**:
  1. Vá em **Inventário > Configuração > Locais**.
  2. Abra o cadastro de `Trânsito Inter-Company` e clique em **Editar**.
  3. Remova a seleção do campo **Empresa** (deixe-o totalmente **vazio**).
  4. Clique em **Salvar**.

---

### ❌ Erro 4: Modal "Transferir Imediatamente?" é exibido ao validar

- **Onde Ocorre**: P3 e P4.
- **Causa**: Aviso padrão informando que as quantidades concluídas serão preenchidas
  automaticamente com base no que foi reservado/demandado.
- **Solução**: Trata-se de uma confirmação normal do Odoo. Apenas clique no botão
  **Aplicar** para efetivar o movimento.
