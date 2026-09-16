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

## 8. Se Acontecer: Campos "Unidade de Medida" Ausentes no Cadastro de Produtos

- **O Problema:** Ao abrir o formulário de um produto
  (`Inventário > Produtos > Produtos > Cadeira de Escritório Preta`), os campos
  **Unidade de Medida** e **Unidade de Medida de Compra** não aparecem na aba
  _Informações gerais_.
- **A Causa:** O parâmetro global de Unidades de Medida vem desabilitado por padrão nas
  configurações gerais do Inventário, ocultando esses seletores em todos os cadastros de
  produtos.
- **A Solução (Passo a Passo):**

  **Opção 1: Ativar pela Interface Web (Recomendado)**

  1. Acesse **Inventário > Configuração > Definições**.
  2. Na seção **Produtos**, marque a caixa **Unidades de Medida** (_Vender e comprar
     produtos em diferentes unidades de medida_).
  3. Clique em **Salvar** no topo da tela.
  4. Retorne ao formulário do produto e pressione **`Ctrl + Shift + R`** para atualizar
     o cache.

  **Opção 2: Ativar Permissão Técnica via Terminal (Odoo Shell)** Para forçar a
  liberação do grupo de Unidades de Medida diretamente no banco de dados:

  1. Abra o terminal na raiz do projeto e acesse o Odoo Shell:
     ```bash
     docker compose run --rm odoo odoo shell -d devel
     ```
  2. Execute o comando Python para vincular o grupo `uom.group_uom` ao Administrador:
     ```python
     env.ref('uom.group_uom').write({'users': [(4, env.ref('base.user_admin').id)]})
     env.cr.commit()
     ```
  3. Digite `exit()` para encerrar a sessão.

---

### 8.1 Estrutura do Formulário Final (Cadeira de Escritório Preta)

Após a ativação das Unidades de Medida, o cadastro do produto `[FURN_0269]` deve
apresentar a seguinte disposição e preenchimento:

- **Bloco Principal (Cabeçalho):**

  - **Nome do Produto:** `Cadeira de Escritório Preta`
  - **Pode ser Vendido:** Marcado (`✔`)
  - **Pode ser Comprado:** Marcado (`✔`)

- **Aba Informações Gerais:**
  - **Tipo de Produto:** `Produto`
  - **Categoria de Produtos:** `All / Saleable / Office Furniture`
  - **Referência Interna:** `FURN_0269`
  - **Código de Barras:** Em branco
  - **Preços de Venda:** `$12,50`
  - **Impostos de Clientes:** Em branco
  - **Custo:** `$18,00`
  - **Empresa:** Em branco
  - **Unidade de Medida:** `Unidades`
  - **Unidade de Medida de Compra:** `Unidades`

## 9. Instalação e Solução de Problemas: Módulo Stock Request (OCA)

Guia completo para clonagem, configuração, instalação e resolução de exceções técnicas
durante a integração do módulo **`stock_request`** (repositório OCA
`stock-logistics-warehouse`) em ambiente Doodba/Docker (Odoo 14.0).

---

### 9.1. Configuração de Repositórios e Addons

Para que a arquitetura do Doodba reconheça o módulo de requisições de estoque, o
repositório e suas dependências devem estar devidamente mapeados nos arquivos YAML do
diretório `odoo/custom/src/`.

#### 1. Configurar `odoo/custom/src/repos.yaml`

Adicione o repositório da OCA com a sintaxe de checkout e destino corretas:

```yaml
./stock-logistics-warehouse:
  depth: 10
  checkout:
    github_default: "14.0"
  remotes:
    oca: [https://github.com/OCA/stock-logistics-warehouse.git](https://github.com/OCA/stock-logistics-warehouse.git)
  target: oca 14.0
```

#### 2. Configurar `odoo/custom/src/addons.yaml`

Associe o diretório baixado ao módulo específico que deve ser indexado pelo Odoo:

```yaml
stock-logistics-warehouse:
  - stock_request
```

#### 3. Clonagem Manual dos Repositórios no Host

Para garantir a presença física dos módulos no sistema de arquivos e evitar falhas na
criação de links simbólicos (_symlinks_), clone os repositórios diretamente na máquina
local:

```bash
# Repositório OCA contendo o módulo stock_request
git clone -b 14.0 --depth 1 [https://github.com/OCA/stock-logistics-warehouse.git](https://github.com/OCA/stock-logistics-warehouse.git) odoo/custom/src/stock-logistics-warehouse

# Repositório de compras complementar registrado no addons.yaml
git clone -b 14.0 --depth 1 [https://github.com/Escodoo/purchase-addons.git](https://github.com/Escodoo/purchase-addons.git) odoo/custom/src/purchase-addons
```

---

### 9.2. Compilação da Imagem e Instalação no Banco de Dados

Após ajustar as configurações e clonar o código-fonte, reconstrua a imagem Docker e
execute a instalação isolada do aplicativo no banco de desenvolvimento (`devel`):

```bash
# 1. Reconstruir a imagem Docker para registrar a nova estrutura do custom/src
docker compose build odoo

# 2. Executar a instalação do módulo stock_request com perfil elevado (root)
docker compose run --rm -u 0 odoo odoo -d devel -i stock_request --stop-after-init

# 3. Inicializar os contêineres em segundo plano
docker compose up -d
```

---

### 9.3. Matriz de Diagnóstico e Solução de Erros (Troubleshooting)

Durante a montagem de ambientes Doodba com permissões mistas (máquina host vs. usuário
interno do container), os seguintes erros podem ocorrer:

| Exceção Identificada nos Logs                                        | Causa Raiz                                                                                                                                               | Procedimento de Correção                                                                                                                                                                                                                   |
| :------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PermissionError: [Errno 13] Permission denied`                      | Arquivos em `/opt/odoo/auto` ou os binários `/usr/local/bin/odoo` foram gravados por comandos com `sudo`/`root` e bloqueiam o usuário `odoo` (UID 1000). | Ajustar permissões da pasta temporária e ownership do volume: <br>`docker compose run --rm --entrypoint "" -u 0 odoo bash -c "chmod -R 777 /opt/odoo/auto /var/lib/odoo /tmp && chown -R 1000:1000 /opt/odoo/auto /var/lib/odoo"`          |
| `FileNotFoundError: [Errno 2] .../stock_request -> .../auto/addons/` | O diretório `/opt/odoo/auto/addons` foi apagado na limpeza de volumes ou o repositório git não existe no caminho local especificado.                     | Clonar o repositório na máquina host e recriar o diretório de destino ignorando o entrypoint padrão: <br>`docker compose run --rm --entrypoint "" -u 0 odoo bash -c "mkdir -p /opt/odoo/auto/addons && chown -R 1000:1000 /opt/odoo/auto"` |
| `WARNING: invalid module names, ignored: stock_request`              | Declaração de URL direta ou nomes com espaços/hífens incorretos no arquivo `addons.yaml`.                                                                | Garantir que o `addons.yaml` contenha apenas a chave do diretório local (`stock-logistics-warehouse:`) e reexecutar o `docker compose build odoo`.                                                                                         |
| `Read-only file system` ao rodar `chmod`/`chown`                     | A pasta `/opt/odoo/custom/src` é montada pelo Docker como volume de apenas leitura (`:ro`).                                                              | Ajustar as permissões de leitura diretamente no terminal do sistema operacional da máquina host: <br>`chmod -R a+rX odoo/custom`                                                                                                           |

---

### 9.4. Script Universal de Restauração de Ambiente

Se o container da aplicação Odoo parar de responder, cair continuamente em loop de
reinicialização ou apresentar erros de permissão ao iniciar, execute a sequência
completa de recuperação abaixo:

```bash
# 1. Dar permissão de leitura global aos arquivos locais da máquina host
chmod -R a+rX odoo/custom

# 2. Recriar diretórios de trabalho internos e ajustar permissões no container
docker compose run --rm --entrypoint "" -u 0 odoo bash -c "mkdir -p /opt/odoo/auto/addons && chmod -R 777 /opt/odoo/auto /var/lib/odoo /tmp && chown -R 1000:1000 /opt/odoo/auto /var/lib/odoo"

# 3. Forçar a recriação limpa do container da aplicação
docker compose up -d --force-recreate odoo

# 4. Monitorar o log de execução até a subida do servidor
docker compose logs -f odoo
```

---

### 9.5. Validação da Instalação na Interface Gráfica

1. Abra o navegador web no endereço `http://localhost:14069`.
2. Atualize a página forçando a limpeza do cache local com **`Ctrl + Shift + R`**.
3. Acesse o menu **Aplicativos**, remova o filtro padrão de _Aplicativos_ na barra de
   pesquisa e busque por `stock_request`.
4. Confirme que o cartão **Stock Request** exibe a indicação **Instalado**.
5. Acesse o aplicativo **Inventário** e certifique-se de que os menus **Operações >
   Pedidos de Estoque** (_Stock Requests_) e **Pedidos de Pedido de Estoque** (_Stock
   Request Orders_) estão ativos para operação.

### 9.6. Integração do Card na Visão Geral do Inventário (stock_request_picking_type)

Por padrão, o módulo `stock_request` disponibiliza apenas os menus e fluxos de
solicitação de estoque de forma isolada. Para que o card **Requisições de Estoque** seja
integrado ao painel principal do **Inventário > Visão Geral** (Dashboard Kanban de Tipos
de Operação), é necessário ativar o submódulo estendido
**`stock_request_picking_type`**.

---

#### 1. Mapeamento no `addons.yaml`

Inclua o submódulo sob o diretório do repositório OCA `stock-logistics-warehouse` no
arquivo `odoo/custom/src/addons.yaml`:

```yaml
stock-logistics-warehouse:
  - stock_request
  - stock_request_picking_type
```

---

#### 2. Instalação e Sincronização do Schema no Banco de Dados

Para registrar os novos campos computados no ORM (como o indicador de pendências
`count_sr_todo`) e evitar erros de campos inválidos nas telas, execute a atualização
encadeada dos módulos:

```bash
# 1. Instalar e atualizar os módulos de requisição de estoque no banco de desenvolvimento (devel)
docker compose run --rm -u 0 odoo odoo -d devel -u stock_request,stock_request_picking_type --stop-after-init

# 2. Reiniciar o serviço web da aplicação Odoo
docker compose restart odoo

# 3. Acompanhar os logs até o término da inicialização
docker compose logs -f odoo
```

---

#### 3. Resolução de Erros de Campo Inválido (`count_sr_todo`)

Caso a interface gráfica apresente um pop-up com a exceção abaixo ao tentar abrir a tela
de Visão Geral do Inventário:

```text
ValueError: Invalid field 'count_sr_todo' on model 'stock.picking.type'
```

- **Causa Raiz:** O cache de visões (views XML) do Odoo tentou renderizar o elemento
  `count_sr_todo` no Kanban antes que o campo computado Python do modelo
  `stock.picking.type` fosse totalmente registrado e reindexado na memória do ORM.
- **Solução:** O comando de atualização `-u stock_request,stock_request_picking_type`
  reestrutura a tabela no banco de dados e limpa a memória do registry, resolvendo a
  falha imediatamente após a reinicialização da instância.

---

#### 4. Validação do Dashboard

1. No navegador, acesse `http://localhost:14069`.
2. Force a atualização dos ativos estáticos e limpeza de cache da página pressionando
   **`Ctrl + Shift + R`**.
3. Navegue até o aplicativo **Inventário > Visão Geral**.
4. Confirme a presença do novo painel **Requisições de Estoque** posicionado ao lado das
   demais operações (Recepções, Transferências Internas e Entregas) exibindo os
   contadores em tempo real.

### 9.7. Configuração Global de Rotas e Regras de Reabastecimento para Requisições

Durante a operação das Ordens de Requisição de Estoque (`stock.request.order`), o motor
de aquisição (_procurement_) do Odoo exige que existam rotas e regras de reabastecimento
válidas apontando para a localização de destino selecionada.

Sem essa parametrização global, a tentativa de confirmação de requisições em
localizações secundárias (como `WH/Input`, `WH/Packing Zone` ou sub-estoques de filiais)
gera a exceção:

```text
Erro de Usuário: Nenhuma regra foi encontrada para reabastecer "[PRODUTO]" em "[LOCALIZAÇÃO]". Verifique a configuração das rotas no produto.
```

---

#### 1. Configuração do Armazém e Habilitação de Rotas de Requisição

Para que qualquer localização do armazém possa receber produtos via requisição sem a
necessidade de rotas MTO manuais por linha:

1. Acesse **Inventário > Configuração > Armazéns**.
2. Abra o armazém desejado (ex: **San Francisco** / `WH`).
3. Na aba **Configuração do Armazém**, certifique-se de definir os fluxos de entrada e
   saída conforme a operação da empresa (ex: _Receber mercadorias diretamente (1 etapa)_
   ou _Regra de 2/3 etapas_).
4. Verifique a seção **Reabastecimento**: garanta que as rotas de fornecimento padrão da
   empresa (_Comprar_, _Fabricar_ ou _Transferências Internas_) estejam ativas.

---

#### 2. Liberação de Rotas nos Produtos (Ação em Massa)

Para evitar ter que editar o cadastro de produto por produto individualmente, aplique a
rota de reabastecimento/compra em lote para todo o catálogo:

1. Acesse **Inventário > Produtos > Produtos**.
2. Alterne para a exibição em **Lista** (ícone no canto superior direito).
3. Selecione a caixa de seleção no topo da tabela para marcar todos os produtos.
4. Clique no botão **Ações** (ícone de engrenagem) e escolha **Ação em Massa / Editar**.
5. No campo **Rotas**, adicione as rotas padrão da sua operação (ex: _Comprar_,
   _Replenish on Order (MTO)_).
6. Clique em **Salvar**.

---

#### 3. Criação de Regras de Reabastecimento Automático (Pull Rules) por Localização

Caso deseje que localizações específicas (como `WH/Input` ou estoques intermediários)
recebam materiais automaticamente via Requisição de Estoque:

1. Acesse **Inventário > Configuração > Regras de Reabastecimento** (ou **Regras de
   Armazenamento**).
2. Clique em **Criar** e configure o padrão de destino:
   - **Localização**: Selecione a localização desejada (ex:
     `WH/Input/Order Processing`).
   - **Quantidade Mínima**: `0,00`
   - **Quantidade Máxima**: `0,00` (ou o limite desejado para o estoque local).
   - **Múltiplo de Quantidade**: `1,00`
3. Salve a regra.

Com essa estrutura ativa, qualquer solicitação criada pelo módulo `stock_request` em
qualquer localização e produto do sistema encontrará a regra de suprimento
correspondente e moverá a ordem para o status **Em Progresso** sem travas operacionais.

## 10. Remoção de Empresas Indesejadas e Purga de Dados do Banco

Durante a inicialização do Odoo em ambiente de desenvolvimento (Doodba/Docker), é comum
a inserção de dados de demonstração contendo múltiplas empresas (como _My Company
(Chicago)_). A exclusão dessas estruturas pela interface web gera bloqueios por conta de
restrições de integridade referencial (_Foreign Keys_) do PostgreSQL.

Abaixo está o procedimento para purgar empresas indesejadas e seus dados correlatos via
terminal, juntamente com o diagnóstico das falhas conhecidas durante o processo.

---

### 10.1. Erros Conhecidos e Soluções

| Erro Retornado no Terminal                                                        | Causa Raiz                                                                                            | Solução Aplicada                                                                                                          |
| :-------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------ |
| `relation "stock_route" does not exist`                                           | Nome incorreto da tabela de rotas do core do Odoo no script SQL.                                      | Utilizar o nome correto da tabela: `stock_location_route`.                                                                |
| `violates foreign key constraint "stock_warehouse_reception_route_id_fkey"`       | Dependência circular entre armazéns (`stock_warehouse`) e suas rotas de recepção/entrega.             | Zerar previamente os campos de rotas na tabela de armazéns (`reception_route_id = NULL`).                                 |
| `column "pbm_route_id" does not exist`                                            | Tentativa de zerar colunas relativas ao módulo de Fabricação (`mrp`) em bases sem o módulo instalado. | Zerar estritamente os campos nativos do core: `reception_route_id`, `delivery_route_id` e `crossdock_route_id`.           |
| `column "parent_id" does not exist`                                               | Uso de nome de coluna incorreto na hierarquia de localizações.                                        | Utilizar o campo correto do Odoo: `location_id`.                                                                          |
| `violates foreign key constraint "res_company_internal_transit_location_id_fkey"` | A tabela `res_company` possui referência direta para a localização de trânsito interno.               | Desvincular a localização de trânsito na empresa antes de remover as localizações: `internal_transit_location_id = NULL`. |
| `violates foreign key constraint "stock_inventory_line_location_id_fkey"`         | Registros em ajustes de inventário (`stock_inventory_line`) apontando para localizações da empresa.   | Deletar primeiro as linhas de inventário (`stock_inventory_line`) e os inventários (`stock_inventory`) vinculados.        |

---

### 10.2. Comando Necessário para Remoção Completa

Execute o bloco abaixo no terminal para realizar a purga da empresa **Chicago** e manter
exclusivamente a estrutura de **San Francisco**:

```bash
docker compose exec -T db psql -U odoo -d devel -c "
DO \$\$
DECLARE
    chicago_id INT;
BEGIN
    SELECT id INTO chicago_id FROM res_company WHERE name LIKE '%Chicago%';

    IF chicago_id IS NOT NULL THEN
        -- 1. Desvincula a localização de trânsito da própria empresa Chicago
        UPDATE res_company SET internal_transit_location_id = NULL WHERE id = chicago_id;

        -- 2. Desvincula parceiros e usuários
        UPDATE res_partner SET company_id = NULL WHERE company_id = chicago_id;
        UPDATE res_users SET company_id = 1 WHERE company_id = chicago_id;

        -- 3. Limpa movimentações de estoque, ajustes de inventário, quants, ordens e regras
        DELETE FROM stock_inventory_line WHERE company_id = chicago_id OR location_id IN (SELECT id FROM stock_location WHERE company_id = chicago_id);
        DELETE FROM stock_inventory WHERE company_id = chicago_id;
        DELETE FROM stock_request WHERE company_id = chicago_id;
        DELETE FROM stock_move_line WHERE company_id = chicago_id;
        DELETE FROM stock_move WHERE company_id = chicago_id;
        DELETE FROM stock_picking WHERE company_id = chicago_id;
        DELETE FROM stock_quant WHERE company_id = chicago_id;
        DELETE FROM stock_rule WHERE company_id = chicago_id;

        -- 4. Zera as FKs de rotas nativas no armazém
        UPDATE stock_warehouse
        SET reception_route_id = NULL,
            delivery_route_id = NULL,
            crossdock_route_id = NULL
        WHERE company_id = chicago_id;

        -- 5. Remove dependências de armazém, rotas e tipos de operação
        DELETE FROM stock_warehouse_orderpoint WHERE company_id = chicago_id;
        DELETE FROM stock_picking_type WHERE company_id = chicago_id;
        DELETE FROM stock_warehouse WHERE company_id = chicago_id;
        DELETE FROM stock_location_route WHERE company_id = chicago_id;

        -- 6. Quebra a hierarquia e limpa localizações
        UPDATE stock_location SET location_id = NULL WHERE company_id = chicago_id;
        DELETE FROM stock_location WHERE company_id = chicago_id;

        -- 7. Remove a empresa
        DELETE FROM res_company WHERE id = chicago_id;

        RAISE NOTICE 'Empresa Chicago e todas as suas dependências foram removidas com sucesso!';
    END IF;
END \$\$;
"
```

> **Após a Execução:** Pressione **Ctrl + Shift + R** no navegador para recarregar a
> interface web do Odoo e validar a exclusão na Visão Geral do Inventário e em
> Configurações > Empresas.

### 10.3 Resumo dos Problemas Enfrentados, Mapeamento Técnico e Soluções Aplicadas

Durante a estruturação do fluxo de reabastecimento automatizado e transferência interna
para a **Cadeira de Conferência (CONFIG) (Aço, Branco)**, foram identificados gargalos
operacionais e de configuração no Odoo. A seguir, apresenta-se o detalhamento técnico de
cada evento, incluindo os modelos (`objects`), campos e caminhos de navegação utilizados
para a resolução.

---

#### 1. Limpeza de Demandas Obsoletas e Acumuladas

- **Problema:** Cotações antigas em estado Rascunho acumulavam reservas e inflavam o
  cálculo de necessidade de reposição.
- **Mapeamento Técnico:**
  - **Objeto (`model`):** `purchase.order`
  - **Caminho:** `Compra > Pedidos > Solicitações de Cotação`
- **Solução:** Acesso direto aos registros obsoletos (ex: `P00011`), alteração de estado
  para Cancelado (`action_rfq_send` / `button_cancel`) e reprocessamento do agendador do
  sistema.

---

#### 2. Travamento por Edição em Linha (_Inline Edit_) nas Listas

- **Problema:** Clique sobre os registros acionava o modo de edição direta da tabela,
  ocultando a barra superior de ações e botões de cabeçalho.
- **Mapeamento Técnico:**
  - **Objeto (`model`):** `stock.warehouse.orderpoint`
  - **Caminho:** `Inventário > Operações > Reposição` (Visão `tree` / `list`)
- **Solução:** Uso da ação de cancelamento de edição (`Descartar`) na barra de ação da
  lista para restaurar a navegação padrão e permitir o acesso ao formulário individual
  via visão Kanban/Form.

---

#### 3. Comportamento do Botão "Peça Uma Vez"

- **Problema:** Ausência do botão "Peça Uma Vez" em determinados produtos e tentativa de
  uso para transferências internas.
- **Mapeamento Técnico:**
  - **Objeto (`model`):** `stock.warehouse.orderpoint`
  - **Campos Relevantes:** `trigger` (`'auto'` vs `'manual'`), `qty_to_order`
  - **Caminho:** `Inventário > Operações > Reposição`
- **Solução:** Esclarecimento de que o botão é exclusivo para requisição de ordens de
  compra externas (`purchase.order`). O botão só fica visível quando
  `trigger = 'manual'` e `qty_to_order > 0`. Para reabastecimento automático em lote, o
  campo `trigger` deve ser mantido como `'auto'` e processado via Agendador
  (`stock.scheduler`).

---

#### 4. Atendimento Parcial de Estoque (Atendimento de Demanda Existente)

- **Problema:** Demanda total de 20 unidades registrada, com disponibilidade física de
  apenas 2 unidades em `WH/Stock`, necessitando do envio imediato do saldo em mãos para
  `Office`.
- **Mapeamento Técnico:**
  - **Objetos (`models`):** `stock.picking` (Transferência) / `stock.move`
    (Movimentação)
  - **Caminho:** `Inventário > Operações > Transferências > WH/INT/00003`
  - **Documento de Origem:** `SRO/00004` (Requisição)
- **Solução:** Abertura do registro de transferência interna `WH/INT/00003`, alteração
  do campo `qty_done` (Concluído) para `2.00` e acionamento da validação
  (`button_validate`). O Odoo disparou o assistente de _Backorder_
  (`stock.backorder.confirmation`), gerando uma nova transferência pendente para as 18
  unidades restantes.

---

#### 5. Disparo da Compra da Diferença Líquida (18 Unidades)

- **Problema:** Garantir a emissão da cotação de compra restrita à necessidade real (18
  unidades), considerando a dedução das 2 unidades atendidas via estoque local.
- **Mapeamento Técnico:**
  - **Objetos (`models`):** `stock.scheduler.compute.wizard` -> `purchase.order` /
    `purchase.order.line`
  - **Caminho:** `Inventário > Operações > Executar Agendador` ->
    `Compra > Solicitações de Cotação`
- **Solução:** Execução manual do motor de regras do Odoo (`procurement.group`). O
  sistema recalculou a regra `OP/00006`, identificou o déficit líquido de 18 unidades e
  gerou automaticamente a Solicitação de Cotação `P00012` vinculada à regra de
  reabastecimento.
