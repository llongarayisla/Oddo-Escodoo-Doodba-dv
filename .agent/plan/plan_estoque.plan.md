# Plano de Ação: Gestão de Estoque TI (ISLA Sementes)

## Contexto & Mapeamento de Fases

### P0: Infraestrutura e Topologia Multi-Company [CONCLUÍDO]

- **Armazéns**: `Armazém TI Porto Alegre` (`ALM-PA`) e `Armazém TI Itapuã` (`ALM-IT`)
  criados e associados às suas respectivas empresas.
- **Locais Físicos**: `PA/Estoque TI` (com sublocais `Disponível`,
  `Seminovos com Avaria`, `Manutenção ou Defeito`) e `ITAP/Estoque TI`.
- **Locais Virtuais**: `Alocados - Porto Alegre` e `Alocados - Itapuã`.
- **Rotas e Parâmetros de Banco**: Rota global `Comprar / Aquisição TI` associada ao XML
  ORM e acessos de segurança do `Super Admin` ajustados para navegação simultânea.

---

## Próximos Passos (Backlog de Execução)

### P1: Categorização e Rastreabilidade

- **Categoria Equipamentos Seriados**:
  - **Nome**: `TI / Equipamentos Seriados`
  - **Uso**: Notebooks, Monitores, Desktops, Servidores, Celulares.
  - **Estratégia de Remoção**: `FIFO`
  - **Rastreabilidade na Ficha**: `Por Número de Série Único`
- **Categoria Periféricos e Consumíveis**:
  - **Nome**: `TI / Periféricos e Consumíveis`
  - **Uso**: Cabos, Teclados, Mouses, Toners, Adaptações.
  - **Estratégia de Remoção**: `FIFO`
  - **Rastreabilidade na Ficha**: `Sem Rastreamento` (Por Quantidade)

---

### P2: Cadastro do Catálogo de Produtos

- **Criar Modelos de Equipamentos (Seriados)**:
  - Tipo de Produto: `Produto Armazenável` (_Storable Product_)
  - Atribuição de Categoria: `TI / Equipamentos Seriados`
  - Controle: Ativar rastreamento por Número de Série na aba **Inventário**.
- **Criar Modelos de Insumos (Consumíveis)**:
  - Tipo de Produto: `Produto Armazenável` (_Storable Product_)
  - Atribuição de Categoria: `TI / Periféricos e Consumíveis`

---

### P3: Carga Inicial de Estoque (Inventário Físico)

- **Ajuste de Inventário - Porto Alegre**:
  - Lançar quantidade física em `PA/Estoque TI/Disponível`.
  - Vincular os Números de Série reais de cada item ativo.
- **Ajuste de Inventário - Itapuã**:
  - Lançar quantidade física em `ITAP/Estoque TI`.
  - Inserir seriais dos equipamentos alocados na filial.

---

### P4: Validação dos Fluxos Operacionais

- **Atribuição a Colaborador / Setor**:
  - Transferir do estoque `Disponível` para o local virtual `Alocados`.
- **Envio para Manutenção / Garantia**:
  - Transferir equipamento de `Disponível` para `Manutenção ou Defeito`.
- **Transferência Inter-Company**:
  - Testar o envio de suprimentos da Matriz para a Filial Itapuã via Rota de Suprimento.
