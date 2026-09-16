# 🛡️ Odoo-Escudo — Guia de Configuração do Ambiente

> Passo a passo completo para preparar o sistema Linux/Ubuntu, gerar o projeto com
> **Doodba** (Tecnativa), incluir a localização brasileira **Escodoo/OCA** e colocar o
> Odoo rodando localmente com Docker.

---

## 📑 Sumário

| #   | Etapa                                                                         | O que você vai fazer                                    |
| --- | ----------------------------------------------------------------------------- | ------------------------------------------------------- |
| 1   | [Preparação do Ambiente](#1-preparação-do-ambiente)                           | Instalar Pipx, ferramentas CLI, Docker e configurar SSH |
| 2   | [Correções Antes de Instalar](#2-correções-antes-de-instalar)                 | Resolver bloqueios de segurança do sistema e da IDE     |
| 3   | [Doodba & Escodoo](#3-doodba--escodoo)                                        | Gerar o projeto, configurar módulos e subir o Odoo      |
| 4   | [Correções Durante o Desenvolvimento](#4-correções-durante-o-desenvolvimento) | Solucionar avisos e dúvidas comuns                      |
| 5   | [Observações Finais](#5-observações-finais)                                   | Acessar os serviços e consultar referências             |

---

## 1. Preparação do Ambiente

> Antes de gerar ou iniciar o projeto, certifique-se de que o sistema possui todas as
> ferramentas essenciais instaladas.

### 1.1 Instalação do Pipx e Ferramentas Python

Instale o `pipx` para isolar executáveis Python sem quebrar os pacotes nativos do
sistema operacional:

```bash
# 1. Instalar o pipx em nível de usuário
py -m pip install --user pipx
# Se o comando 'py' não for reconhecido, utilize:
# python3 -m pip install --user pipx

# 2. Registrar as ferramentas no PATH
pipx ensurepath
```

---

### 1.2 Instalação das Ferramentas CLI (Copier, Invoke, Pre-commit)

Instale os utilitários que serão usados durante todo o ciclo de vida do projeto:

```bash
pipx install copier
pipx install invoke
pipx install pre-commit

# Validar versões instaladas
copier --version
invoke --version
pre-commit --version
```

---

### 1.3 Instalação Oficial do Docker Engine no Ubuntu

> [!IMPORTANT] Execute a instalação do Docker no **terminal nativo do Ubuntu**
> (**`Ctrl + Alt + T`**) com permissão de `sudo`. Terminais de IDEs em Flatpak/Snap
> podem bloquear o processo.

```bash
# 1. Desinstalar pacotes conflitantes
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove -y $pkg; done

# 2. Configurar o repositório oficial Docker APT
sudo apt-get update
sudo apt-get install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update

# 3. Instalar o Docker Engine e o plugin Compose
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 4. Adicionar seu usuário ao grupo do Docker
sudo usermod -aG docker $USER
```

---

### 1.4 Configuração da Chave SSH com o GitHub

Necessária para clonar e atualizar repositórios privados ou da organização Escodoo sem
erros de autenticação:

```bash
# 1. Gerar a chave SSH Ed25519
ssh-keygen -t ed25519 -C "seu-email@exemplo.com"
# Pressione Enter para aceitar os padrões e deixar sem senha

# 2. Ativar o agente SSH e registrar a chave
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# 3. Exibir a chave pública gerada
cat ~/.ssh/id_ed25519.pub
```

Após gerar a chave:

1. Copie o conteúdo impresso (começa com `ssh-ed25519 ...`).
2. Acesse 👉 [https://github.com/settings/ssh/new](https://github.com/settings/ssh/new).
3. Cole a chave no campo **Key**, dê um título e clique em **Add SSH key**.
4. Teste a conexão no terminal:
   ```bash
   ssh -T git@github.com
   # Digite 'yes' se solicitado. Deve retornar:
   # Hi <seu-usuario>! You've successfully authenticated...
   ```

---

## 2. Correções Antes de Instalar

> Antes de prosseguir para o Doodba, resolva os bloqueios e comportamentos inesperados
> mais comuns no Linux/Ubuntu com IDEs em sandbox.

### 2.1 Trava do `sudo`: "no new privileges flag is set"

|             |                                                                                                               |
| ----------- | ------------------------------------------------------------------------------------------------------------- |
| **Causa**   | IDEs instaladas via Flatpak ou Snap (sem modo clássico) bloqueiam a elevação para `root` em processos filhos. |
| **Solução** | Sempre que precisar de `sudo`, use o **terminal nativo** pressionando **`Ctrl + Alt + T`**.                   |

---

### 2.2 Permissão do Socket do Docker (`/var/run/docker.sock`)

|              |                                                                                                                                        |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| **Problema** | Erro `permission denied while trying to connect to the docker API at unix:///var/run/docker.sock` ao rodar comandos Docker no VS Code. |
| **Solução**  | No terminal nativo (`Ctrl + Alt + T`), libere o acesso ao socket:                                                                      |

```bash
sudo chmod 666 /var/run/docker.sock
```

> Isso resolve instantaneamente para todos os terminais e IDEs sem precisar reiniciar o
> sistema.

---

### 2.3 Erro "setgid/setgroups: Operação não permitida" com `newgrp`

|              |                                                                                                           |
| ------------ | --------------------------------------------------------------------------------------------------------- |
| **Problema** | `newgrp docker` dentro do terminal da IDE falha com `setgid: Operação não permitida`.                     |
| **Solução**  | Não utilize `newgrp` dentro da IDE. Use a correção do socket (item 2.2) ou reinicie sua sessão do Ubuntu. |

---

### 2.4 Aviso do `pipx ensurepath` (apenas ignore)

|              |                                                                                        |
| ------------ | -------------------------------------------------------------------------------------- |
| **Problema** | Aviso com `⚠️` dizendo que `~/.local/bin is already in PATH`.                          |
| **Ação**     | **Apenas ignore!** É só uma confirmação de que o diretório já está registrado no PATH. |

---

### 2.5 Comando `py` ou `python` não encontrado

|              |                                                                       |
| ------------ | --------------------------------------------------------------------- |
| **Problema** | O Ubuntu usa o executável `python3` por padrão, não `py` ou `python`. |
| **Solução**  | Adicione os aliases ao seu `~/.bashrc`:                               |

```bash
echo "alias py='python3'" >> ~/.bashrc
echo "alias python='python3'" >> ~/.bashrc
source ~/.bashrc
```

---

## 3. Doodba & Escodoo

> Com o ambiente pronto, agora você vai gerar a estrutura do projeto, configurar os
> módulos brasileiros e executar o Odoo com Docker.

### 3.1 Geração da Estrutura do Projeto via Copier

No diretório onde o projeto será criado, execute:

```bash
copier copy gh:Tecnativa/doodba-copier-template . --UNSAFE
```

O Copier fará uma série de perguntas interativas. Consulte a tabela da próxima seção
para saber como responder cada uma delas.

---

### 3.2 Respostas para as Perguntas do Copier

> [!TIP] Em campos de múltiplas linhas onde o `Enter` comum quebra linha, use
> **`Alt + Enter`** (ou **`Esc`** e depois **`Enter`**) para confirmar e avançar.

| Pergunta no Terminal                                                  | Significado                                          | Resposta Recomendada                                    |
| :-------------------------------------------------------------------- | :--------------------------------------------------- | :------------------------------------------------------ |
| **On which odoo version is it based?**                                | Versão do Odoo.                                      | `14.0`                                                  |
| **Which proxy will you use to deploy odoo?**                          | Proxy reverso para produção.                         | `No proxy (dangerous for production)` (dev local)       |
| **Indicate the Docker Compose version.**                              | Versão do Compose.                                   | `v2+`                                                   |
| **If you want to initialize Odoo in a specific language...**          | Idioma do banco.                                     | `pt_BR`                                                 |
| **What will be your odoo admin password?**                            | Senha mestra do Odoo.                                | Digite sua senha administrativa.                        |
| **Do you want to list databases publicly?**                           | Exibir seletor de bancos.                            | `Yes`                                                   |
| **If you are using an OCI/Docker image registry...**                  | ⚠️ **NÃO é o autor!** Endereço remoto no Docker Hub. | Tecle `Enter` (vazio para dev local)                    |
| **Tell me who you are.**                                              | Nome do autor para manifestos e linter.              | Ex: `isla_longaray`                                     |
| **What's your project name?**                                         | Nome do projeto (sem espaços ou pontos).             | Ex: `odoo-escudo`                                       |
| **So, what's your project's license?**                                | Licença de software.                                 | `GNU Affero General Public License (AGPL) 3.0 or later` |
| **Use refurb... (y/N)**                                               | Linter extra de Python.                              | `n` + `Enter`                                           |
| **Configure production / test / migration domains**                   | Domínios Traefik.                                    | `Alt + Enter` (aceita padrão vazio)                     |
| **Extra external hosts to allow...**                                  | Whitelist de domínios externos.                      | `Alt + Enter` (aceita os padrões)                       |
| **Docker Compose project name used by whitelist sidecar...**          | Nomes de containers.                                 | `Enter` (aceita os padrões amarelos)                    |
| **Tell me the list of paths where you want to forbid/allow crawlers** | Bloqueios para robôs.                                | `Alt + Enter` (aceita os padrões)                       |
| **If you need to whitelist certain CIDR...**                          | Whitelist de IPs.                                    | `Alt + Enter` (deixa vazio)                             |

---

### 3.3 Configuração de Módulos (`addons.yaml`)

Edite o arquivo [`odoo/custom/src/addons.yaml`](odoo/custom/src/addons.yaml) definindo
quais repositórios de módulos serão vinculados ao projeto:

```yaml
website:
  - "*"

web:
  - "*"

ENV:
  DEFAULT_REPO_PATTERN: https://github.com/Escodoo/{}.git

purchase-addons:
  - "*"

l10n-brazil:
  - "*"
```

---

### 3.4 Configuração de Repositórios e Localização Brasileira (`repos.yaml`)

Edite o arquivo [`odoo/custom/src/repos.yaml`](odoo/custom/src/repos.yaml) incluindo a
localização brasileira da OCA/Escodoo com mesclagem de PR:

```yaml
./l10n-brazil:
  defaults:
    depth: $DEPTH_MERGE
  merges:
    - origin $ODOO_VERSION
    - origin refs/pull/2624/head
  remotes:
    escodoo: https://github.com/Escodoo/l10n-brazil
    origin: https://github.com/OCA/l10n-brazil
  target: origin merged
```

> [!WARNING] Atenção com erros de digitação: escreva **`l10n`** com o número `0`,
> **`$ODOO_VERSION`** com a letra `O`, **`merged`** com `e`, e use
> **`depth: $DEPTH_MERGE`** para garantir histórico suficiente no merge do PR.

---

### 3.5 Otimização de Recursos e Performance

#### A. Configuração do Odoo (`conf.d/00-escodoo.conf`)

Edite o arquivo
[`odoo/custom/conf.d/00-escodoo.conf`](odoo/custom/conf.d/00-escodoo.conf) para evitar
timeouts (_504 Gateway Timeout_) e quedas por falta de memória:

```ini
[options]
limit_memory_hard = 16777721600
limit_memory_soft = 629145600
limit_request = 8192
limit_time_real = 1200
limit_time_cpu = 600
max_cron_threads = 1
workers = 8
```

#### B. Otimização do PostgreSQL (`common.yaml`)

Edite o arquivo [`common.yaml`](common.yaml) na seção do serviço `db`:

```yaml
  db:
    image: ghcr.io/tecnativa/postgres-autoconf:16-alpine
    shm_size: 4gb
    environment:
      POSTGRES_DB: *dbname
      POSTGRES_USER: *dbuser
      PGDATA: "/var/lib/postgresql/data"
      CONF_EXTRA: |
        work_mem = 512MB
    volumes:
      - db:/var/lib/postgresql/data
```

---

### 3.6 Ciclo Completo de Comandos do Invoke

Execute os comandos abaixo dentro da pasta raiz do projeto (onde está o `tasks.py`):

```bash
# 1. Configurar o ambiente (pre-commit e git hooks)
invoke develop

# 2. Construir as imagens Docker baixando as camadas mais recentes
invoke img-build --pull

# 3. Baixar os repositórios definidos em repos.yaml e addons.yaml
invoke git-aggregate

# 4. Inicializar o banco de dados do zero com dados de demonstração
invoke resetdb

# 5. Compilar assets estáticos e mesclar configurações do conf.d
invoke preparedb

# 6. Iniciar todos os containers
invoke start

# 7. Acompanhar os logs em tempo real (Ctrl+C para sair sem parar o container)
invoke logs -f odoo

# 8. Parar todos os containers
invoke stop
```

---

## 4. Correções Durante o Desenvolvimento

> Avisos e comportamentos esperados que surgem durante o uso diário do ambiente.

### 4.1 Diferença entre `invoke resetdb` e `invoke preparedb`

| Comando            | O que faz                                                 | Quando usar                               |
| ------------------ | --------------------------------------------------------- | ----------------------------------------- |
| `invoke resetdb`   | **Apaga** o banco atual e recria do zero com `--demo`.    | Para reiniciar o ambiente completamente.  |
| `invoke preparedb` | **Mantém** os dados, atualiza módulos e mescla `conf.d/`. | No dia a dia, após alterações de módulos. |

---

### 4.2 Aviso: `DOODBA_GITHUB_TOKEN variable is not set`

|           |                                                                                    |
| --------- | ---------------------------------------------------------------------------------- |
| **Causa** | Não há um Personal Access Token do GitHub configurado no arquivo `.env`.           |
| **Ação**  | **Apenas ignore.** Não interfere no funcionamento local com repositórios públicos. |

---

### 4.3 Aviso: `database "devel" does not exist` durante `resetdb`

|           |                                                                                            |
| --------- | ------------------------------------------------------------------------------------------ |
| **Causa** | O script verifica a extensão `unaccent` antes de criar o banco.                            |
| **Ação**  | **Apenas ignore.** O `click-odoo-initdb` cria o banco `devel` com sucesso logo em seguida. |

---

### 4.4 Como fazer novos módulos aparecerem na interface do Odoo

1. Execute no terminal:
   ```bash
   invoke preparedb
   invoke restart
   ```
2. Acesse o Odoo em: **`http://localhost:14069`**.
3. Certifique-se de que o **Modo Desenvolvedor** está ativado — adicione `?debug=1` na
   URL.
4. Acesse o menu **Aplicativos** (Apps).
5. Clique em **Atualizar Lista de Aplicativos** (_Update Apps List_) e confirme.
6. Na barra de pesquisa, **remova o filtro "Aplicativos"** para listar todos os módulos
   técnicos, pesquise pelo módulo e clique em **Instalar**.

---

## 5. Observações Finais

### 5.1 Painéis e Portas Mapeadas no Navegador

Após executar `invoke start`, os seguintes serviços estarão disponíveis:

| Serviço        | Endereço                                         | Descrição                                                                          |
| :------------- | :----------------------------------------------- | :--------------------------------------------------------------------------------- |
| 🚀 **Odoo 14** | [http://localhost:14069](http://localhost:14069) | Porta padrão Doodba: versão `14` + `069` = `14069`. Selecione o banco **`devel`**. |
| 📬 **Mailhog** | [http://localhost:8025](http://localhost:8025)   | Webmail para visualizar e-mails disparados pelo Odoo.                              |
| 🗄️ **Pgweb**   | [http://localhost:8081](http://localhost:8081)   | Interface gráfica para inspecionar o banco PostgreSQL.                             |
| 🐞 **WDB**     | [http://localhost:1984](http://localhost:1984)   | Depurador interativo de código Python.                                             |

---

### 5.2 Links Úteis e Referências

| Recurso                            | Link                                                                                                   |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------ |
| 🏢 Escodoo no GitHub               | [github.com/escodoo](https://github.com/escodoo)                                                       |
| 🎬 Playlist de Treinamento Escodoo | [YouTube](https://www.youtube.com/watch?v=b12GwoSHRHs&list=PLs5WR750kjpdPxmU8vE-nIX1flWABqFvu&index=1) |
| 🔧 Template Doodba (Copier)        | [github.com/Tecnativa/doodba-copier-template](https://github.com/Tecnativa/doodba-copier-template)     |
| 🐳 Guia Oficial Docker no Ubuntu   | [docs.docker.com/engine/install/ubuntu](https://docs.docker.com/engine/install/ubuntu/)                |
