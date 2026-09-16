# Guia de Uso: Módulo de Inventário (Estoque) no Odoo via Doodba

Documento de referência rápida para instalação, acesso e realização de ajustes de
estoque na plataforma Odoo/Doodba com padrão Escodoo.

---

## 1. Instalação e Acesso Inicial

- **Instalação Direta:** O aplicativo **Inventário** (`stock`) é instalado diretamente
  pela interface em **Apps**.
- **Redirecionamento Padrão:** Após a conclusão da instalação, o sistema redireciona
  automaticamente o usuário para o aplicativo **Conversa** (_Discuss_).
- **Navegação de Acesso:** Para abrir o módulo, clique no alternador de aplicativos
  (canto superior esquerdo) e selecione **Inventário**.
- **Painel Principal:** A tela inicial exibe a **Visão Geral do Inventário** (_Inventory
  Overview_), composta pelos 4 cards operacionais padrão do sistema (como Recebimentos e
  Ordens de Entrega).

---

## 2. Processo de Ajustes de Estoque

Para alinhar o saldo do sistema com a contagem física dos produtos, utilize o fluxo
oficial de inventário:

### 2.1 Navegação e Criação

1. Acesse o menu superior: **Operações** -> **Ajustes de Estoque**.
2. Clique no botão **Criar** no canto superior esquerdo para abrir o formulário de
   inventário.

### 2.2 Configuração do Formulário de Contagem

- **Referência de Inventário:** Digite um nome para identificar a contagem (Exemplo:
  `Contagem do dia 16/09`).
- **Produtos:** Selecione um produto específico ou deixe em branco para incluir todos os
  itens do inventário.
- **Empresa:** Selecione a unidade/empresa correspondente (caso utilize ambiente
  _Multi-Company_).
- **Quantidades Contadas:**
  - _Padrão para estoque disponível:_ Preenche a coluna contada com a quantidade atual
    do sistema.
  - _Padrão para zero:_ Define todas as quantidades iniciais como zero para contagem
    cega.

---

## 3. Lançamento da Contagem e Validação

1. Clique no botão **Começar inventário** para carregar as linhas de produtos.
2. **Edição de Linhas:** Clique diretamente na linha do produto desejado para habilitar
   a edição e informe a quantidade física real encontrada no campo **Contado**.
3. **Lote / Número de Série:** A coluna exibe a identificação rastreável do produto
   quando aplicável, ou permanece em branco para produtos não rastreados.
4. **Cálculo da Diferença:** O Odoo calcula a variação automaticamente entre a
   quantidade **Na Mão** e a quantidade **Contada**:
   - **Valores Positivos (ex: `+1,00`):** Indicam sobra de estoque.
   - **Valores Negativos (ex: `-5,00`):** Indicam perda ou quebra de estoque.
5. **Finalização:** Clique no botão **Validar Inventário** para efetivar os lançamentos
   e atualizar o saldo real dos produtos no banco de dados.

## 4. Se Acontecer (Resolução de Problemas Frequentes)

Guia rápido para identificar e solucionar falhas comuns observadas na operação do módulo
e do ambiente Doodba.

---

### 🛑 Não consigo excluir um Ajuste de Estoque ("Ajuste já Validado")

- **O Problema:** Ao tentar apagar um ajuste de contagem com status **Validado**
  (_Done_), o Odoo bloqueia a ação para proteger a integridade dos registros fiscais e
  contábeis (`stock.move`).
- **A Solução:**
  - **Via Terminal (Mais ágil):** Cancele e remova as movimentações de estoque
    vinculadas executando o script no Odoo Shell:
    ```bash
    docker compose run --rm odoo odoo shell -d devel
    ```
    Cole o código no terminal:
    ```python
    inventories = env['stock.inventory'].search([('state', '=', 'done')])
    moves = inventories.mapped('move_ids')
    moves.write({'state': 'draft'})
    moves.unlink()
    inventories.unlink()
    env.cr.commit()
    ```
  - **Via Interface:** Ative o modo desenvolvedor (`?debug=1`), acesse
    `Configurações > Técnico > Estrutura do Banco de Dados > Movimentos de Estoque`,
    exclua os movimentos vinculados e depois apague a contagem.

---

### 🛑 O formulário de Armazém não exibe as opções de Remessa (1, 2 ou 3 Etapas)

- **O Problema:** A tela de cadastro do Armazém em `Configuração > Armazéns` exibe
  apenas campos básicos, ocultando a seção de **Remessas Recebidas** e **Remessas
  Enviadas**.
- **A Solução:**
  1. Acesse `Inventário > Configuração > Configurações`.
  2. Na seção **Armazém**, marque as opções:
     - **Locais de armazenamento**
     - **Rotas com várias etapas**
  3. Clique em **Salvar** no topo da página. As opções de etapas de remessa reaparecerão
     no cadastro de armazéns.

---

### 🛑 Erro `Uncaught Error: Service ... already defined` ao rodar testes web/mobile

- **O Problema:** A suíte QUnit falha indicando duplicidade de serviços JavaScript (ex:
  `web.daterangepicker.extensions`). Ocorre quando há pastas de bibliotecas nativas
  clonadas dentro da pasta de customizados (`odoo/custom/src/`).
- **A Solução:**
  1. Remova as pastas duplicadas do diretório `custom/src`:
     ```bash
     rm -rf ~/Projetos/Odoo-Escudo/odoo/custom/src/web ~/Projetos/Odoo-Escudo/odoo/custom/src/website
     ```
  2. Force a recomposição de anexos e reinicie o ambiente:
     ```bash
     invoke preparedb
     invoke restart
     ```

---

### 🛑 Erro `RuntimeError: request not bound to a database`

- **O Problema:** O Odoo recusa a requisição HTTP ao acessar testes ou abas anônimas por
  não reconhecer a qual banco de dados a sessão pertence.
- **A Solução:**
  1. Faça login manualmente no banco de dados desejado (`http://localhost:14069`) antes
     de abrir a URL de teste.
  2. **Solução Definitiva:** Fixe o banco padrão no projeto editando o arquivo
     `odoo/custom/conf.d/00-escodoo.conf`:
     ```ini
     db_name = devel
     ```
  3. Aplique as configurações no terminal:
     ```bash
     invoke preparedb
     invoke restart
     ```

## 5. Se Acontecer: Bloco "Reabastecer" Ausente no Cadastro do Armazém

- **O Problema:** A coluna **Reabastecer** (com a opção _Compre para reabastecer_) não é
  exibida ao lado da seção _Remessas_ na tela de configuração do Armazém
  (`Inventário > Configuração > Armazéns`).
- **A Causa:** O Odoo oculta a regra de reabastecimento do armazém porque o módulo de
  **Compras** (_purchase_) não está instalado na base de dados.
- **A Solução:**

  1. No menu principal do Odoo, acesse a tela de **Apps**.
  2. Remova o filtro padrão de _Apps_ na barra de busca (se necessário) e pesquise por
     **Purchase** ou **Compras**.
  3. Clique no botão **Instalar** no card do aplicativo.
  4. Retorne para **Inventário > Configuração > Armazéns > San Francisco**.

- **Resultado Esperado:** A coluna **Reabastecer** reaparecerá no formulário com a caixa
  de seleção _Compre para reabastecer_, alinhando o ambiente ao material de treinamento.

## 6. Estrutura e Cadastro de Locais de Armazenamento (_Locations_)

A navegação para gestão de sublocações é feita em **Inventário > Configuração >
Locais**.

### 6.1 Visualização e Filtros

- **Filtro Padrão `Interno`:** A listagem inicial do Odoo exibe apenas os locais físicos
  do armazém (_Local Interno_).
- **Exibir Locais Virtuais e Externos:** Remova o filtro `Interno` na barra de pesquisa
  para visualizar locais de trânsito, fornecedores, clientes, sucata e perdas de
  inventário.

---

### 6.2 Campos de Cadastro de um Novo Local (`Criar`)

Ao criar um local (Ex: prateleira, gaveta ou geladeira), preencha os campos estruturais:

- **Nome do Local:** Identificação direta da sublocação (Ex: `Shelf 1`, `Geladeira`).
- **Local Pai (_Parent Location_):** Define a hierarquia da árvore de estoque.
  - _Exemplo:_ Selecionar `WH/Stock` faz o endereço completo se tornar
    `WH/Stock/Shelf 1`.
- **Tipo de Local (_Location Type_):**
  - **Local Interno:** Áreas físicas reais sob controle da empresa (estoque,
    prateleiras, docas).
  - **Localização de Fornecedor / Local do Cliente:** Locais externos usados para
    rastrear origem e destino de mercadorias.
  - **Perda de Inventário / Sucata / Produção:** Locais virtuais do sistema para balanço
    de ajustes de contagem e ordens de produção.
- **Empresa:** Associa o local a uma filial específica em ambientes _Multi-Company_.

## 7. Se Acontecer: Campos "Armazém" e "Pacotes" Ausentes nos Tipos de Operações

- **O Problema:** Ao acessar o formulário de um Tipo de Operação (ex:
  `Inventário > Configuração > Tipos de Operações > San Francisco: Recepções`), o campo
  **Armazém** (abaixo de _Código_) e a seção de **Pacotes** não aparecem na tela,
  diferindo da interface exibida no treinamento.
- **A Causa:** As opções de empacotamento de produtos estão desabilitadas no parâmetro
  geral do módulo, e o usuário atual não possui a permissão técnica de segurança
  necessária para gerenciar múltiplos armazéns (`stock.group_stock_multi_warehouses`).
- **A Solução (Passo a Passo):**

  **Parte 1: Ativar Funcionalidades na Interface**

  1. Acesse **Inventário > Configuração > Definições**.
  2. Na seção **Operações**, marque a caixa **Pacotes** (_Coloque seus produtos em
     embalagens..._).
  3. Na seção **Armazém**, confirme se **Locais de armazenamento** e **Rotas com várias
     etapas** estão marcadas.
  4. Clique em **Salvar** no topo da tela.

  **Parte 2: Ativar Permissão Técnica do Usuário (Terminal Doodba)** Para forçar a
  exibição do campo "Armazém", aplique a permissão oculta via terminal.

  1. Abra o terminal nativo na raiz do projeto e acesse o Odoo Shell:
     ```bash
     docker compose run --rm odoo odoo shell -d devel
     ```
  2. Cole o código abaixo para vincular o grupo de múltiplos armazéns ao usuário
     Administrador e salvar:
     ```python
     env.ref('stock.group_stock_multi_warehouses').write({'users': [(4, env.ref('base.user_admin').id)]})
     env.cr.commit()
     ```
  3. Digite `exit()` para encerrar a sessão.

- **Resultado Esperado:** Volte à tela do Tipo de Operação no navegador e pressione
  **`Ctrl + Shift + R`** (ou `Ctrl + F5`) para limpar o cache. O campo **Armazém**
  aparecerá na coluna esquerda e o bloco **Pacotes** surgirá na direita, alinhando seu
  ambiente 100% com o da videoaula.

## 7.1 Estrutura do Formulário Final (San Francisco: Recepções)

Após realizar as parametrizações de definições e aplicar as permissões técnicas, o
formulário de **Tipos de Operações**
(`Inventário > Configuração > Tipos de Operações > San Francisco: Recepções`) deve
apresentar exatamente a seguinte disposição e preenchimento de campos:

- **Bloco Principal (Geral):**

  - **Tipo de Operação:** `Recepções`
  - **Sequência de Referência:** `San Francisco Sequence in`
  - **Código:** `IN`
  - **Armazém:** `San Francisco`
  - **Tipo da Operação:** `Recebimento`
  - **Empresa:** `My Company (San Francisco)`
  - **Tipo de operação para devoluções:** `San Francisco: Entregas`
  - **Mostrar operações detalhadas:** Marcado (`✔`)
  - **Pré-preencher Operações Detalhadas:** Desmarcado

- **Bloco Rastreabilidade:**

  - **Criar Novos Números de Lotes/Séries:** Marcado (`✔`)
  - **Usar lotes / números de série existentes:** Desmarcado

- **Bloco Pacotes:**

  - **Mover pacotes inteiros:** Desmarcado

- **Bloco Locais:**
  - **Local de Origem Padrão:** Em branco
  - **Local Padrão de Destino:** `WH/Stock`

## 7.2 Se Acontecer: Campos Ausentes e Erro de Acesso nas Rotas e Regras de Estoque

- **O Problema:** Na tela de Rotas
  (`Inventário > Configuração > Rotas > San Francisco: Entregar em 1 etapa`), a opção
  **Linhas do Pedido de Venda** não aparece. Além disso, no popup da Regra
  (`WH: Stock → Customers`), faltam os campos **Sequência**, **Armazém** e a seção de
  **Propagação**. Ao tentar ativar o Modo Desenvolvedor para visualizar esses campos, o
  sistema exibe um bloqueio de _"Erro de Acesso (account.analytic.group)"_.
- **A Causa:**

  1. O campo _Linhas do Pedido de Venda_ depende diretamente da presença do módulo de
     **Vendas** (`sale`).
  2. Os campos avançados de _Sequência_, _Armazém_ e _Propagação_ são recursos técnicos
     exibidos apenas em **Modo Desenvolvedor** (`?debug=1`).
  3. O erro de acesso ocorre porque a instalação de Vendas cria dependências com a
     Contabilidade Analítica, exigindo que o usuário tenha o grupo de segurança
     `analytic.group_analytic_accounting`.

- **A Solução (Passo a Passo):**

  **Parte 1: Instalar o Módulo de Vendas**

  1. Acesse o menu de **Apps**.
  2. Pesquise por **Sales** (Vendas) e clique em **Instalar**.

  **Parte 2: Corrigir a Permissão de Contabilidade Analítica (Terminal Doodba)**

  1. Abra o terminal na raiz do projeto e acesse o Odoo Shell:
     ```bash
     docker compose run --rm odoo odoo shell -d devel
     ```
  2. Cole o comando Python para conceder acesso de Contabilidade Analítica ao
     Administrador:
     ```python
     env.ref('analytic.group_analytic_accounting').write({'users': [(4, env.ref('base.user_admin').id)]})
     env.cr.commit()
     ```
  3. Digite `exit()` para encerrar a sessão.

  **Parte 3: Ativar o Modo Desenvolvedor**

  1. Adicione `?debug=1` na URL do seu navegador (ex:
     `http://localhost:14069/web?debug=1#...`).
  2. Recarregue a página pressionando **`Ctrl + Shift + R`**.

- **Resultado Esperado:** A Rota exibirá a caixa **Linhas do Pedido de Venda**, e ao
  abrir a Regra `WH: Stock → Customers`, o popup carregará perfeitamente com o campo
  **Armazém** (`San Francisco`), a **Sequência** (`20`) e o bloco lateral de
  **Propagação** ativos sem erros de permissão.

## 7.3 Elevação de Privilégios (Superuser) e Personalização do Administrador via Terminal

- **O Problema:** O usuário padrão do Odoo (`Mitchell Admin` / `base.user_admin`) é
  criado com limitações de permissão. Ele não possui acesso a diversos menus técnicos,
  botões de ação e campos avançados de configuração.
- **A Causa:** O Odoo restringe o perfil do administrador padrão por segurança e impõe
  validações de integridade no banco de dados. Tentativas de adicionar
  indiscriminadamente todos os grupos de segurança falham devido a conflitos de
  exclusividade mútua (ex.: ter simultaneamente os perfis _Utilizador Interno_, _Portal_
  e _Público_, ou ter ativos os grupos de subtotal de impostos _B2B_ e _B2C_ ao mesmo
  tempo).
- **A Solução (Passo a Passo via Terminal):** Para contornar as validações e transformar
  o `Mitchell Admin` em um **Superuser real** com perfil personalizado (nome, e-mail e
  foto), utilize o `odoo shell` com filtragem inteligente dos grupos conflitantes.

**1. Acessar o Odoo Shell** No terminal da máquina host, na raiz do projeto, execute:

```bash
docker compose run --rm odoo odoo shell -d devel
```

**2. Executar o Script de Manutenção no Console Python** Cole o bloco de código abaixo
no terminal interativo (`>>>`) e pressione **Enter**:

```python
import base64

# 1. Definir credenciais e caminho do arquivo de imagem
NOME_ADMIN = 'Super Admin'
LOGIN_ADMIN = 'admin'
EMAIL_ADMIN = 'admin@escudo.local'
CAMINHO_FOTO = '/opt/odoo/custom/src/logo.jpeg'

# 2. Carregar o usuário Administrador principal
admin = env.ref('base.user_admin')

# 3. Atualizar Nome, Login e E-mail
admin.write({
    'name': NOME_ADMIN,
    'login': LOGIN_ADMIN,
    'email': EMAIL_ADMIN
})

# 4. Atualizar Foto de Perfil via Arquivo Físico
try:
    with open(CAMINHO_FOTO, 'rb') as img_file:
        admin.write({'image_1920': base64.b64encode(img_file.read())})
    print("Foto atualizada com sucesso!")
except Exception as e:
    print(f"Erro ao carregar foto: {e}")

# 5. Mapear e tratar grupos com restrições de exclusividade mútua
cat_user_type = env.ref('base.module_category_user_type')
grupos_user_type = env['res.groups'].search([('category_id', '=', cat_user_type.id)])
grupo_interno = env.ref('base.group_user')

# Remove Portal e Público para manter apenas Utilizador Interno
grupos_proibidos = grupos_user_type - grupo_interno

# Trata conflito do grupo de exibição de impostos B2C (Tax-Included)
grupo_tax_b2c = env.ref('account.group_show_line_subtotals_tax_included', raise_if_not_found=False)
if grupo_tax_b2c:
    grupos_proibidos |= grupo_tax_b2c

# 6. Filtrar grupos permitidos e atribuir ao Administrador
grupos_permitidos = env['res.groups'].search([('id', 'not in', grupos_proibidos.ids)])
admin.write({'groups_id': [(6, 0, grupos_permitidos.ids)]})

# 7. Persistir as alterações no banco de dados
env.cr.commit()
```

**3. Encerrar o Shell**

```python
exit()
```

- **Resultado Esperado:** Ao recarregar a interface web (`Ctrl + Shift + R`), o usuário
  exibirá o nome **Super Admin**, o logotipo customizado no canto superior direito e
  acesso irrestrito a todos os módulos, menus técnicos e campos ocultos do Odoo.
