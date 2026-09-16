# Registro da instalação

## 1. Inspeção inicial

- Diretório: `L:\Sistemas\Doodba`.
- A pasta estava vazia e ainda não era um repositório Git.
- Não havia um `AGENTS.md` no diretório nem nos caminhos ancestrais verificados.
- Host Windows com Docker Desktop instalado; backend Linux inicialmente parado.

## 2. Inicialização do Docker Desktop

Comando executado no Windows:

```powershell
Start-Process -FilePath 'C:\Program Files\Docker\Docker\Docker Desktop.exe' -WindowStyle Hidden
docker --context desktop-linux version
```

Resultado: Docker Desktop iniciado e Engine Linux acessível. Versões observadas: Docker
Desktop 4.81.0; Engine 29.6.1; arquitetura Linux amd64. Essas são as versões existentes
no host, não versões atribuídas aos vídeos.

## 3. Versões confirmadas na aula

Fonte:
[Linux — vídeo 4 — Criando Ambiente Doodba](https://www.youtube.com/watch?v=AJKrmk55bEo).

A transcrição automática exportada pelo navegador registra:

- Aproximadamente 00:43–00:47: seleção do Odoo 14.
- Aproximadamente 01:36–01:40: seleção do PostgreSQL 13.
- Criação do projeto pelo Doodba Copier Template.
- Ambiente de desenvolvimento sem proxy de produção.
- Aula seguinte dedicada a workspace e comandos Invoke.

A revisão do template e as versões exatas das ferramentas Python ainda não foram
confirmadas. A transcrição automática pode conter erros; não usá-la para inferir
argumentos de comandos ilegíveis.

## 4. Regra de exclusividade

Após a nova orientação do usuário, foi executado:

```powershell
docker --context desktop-linux ps --format '{{.ID}}\t{{.Names}}\t{{.Image}}'
```

Resultado: nenhum container em execução. Nenhuma parada foi necessária.

## 5. Implementação P0 (2026-09-16)

- Git local já existia; remoto não foi criado.
- Imagem `doodba-local:14-pg13` construída a partir de `tecnativa/doodba:14.0-onbuild`
  pinada, com PostgreSQL 13 e supervisord na mesma imagem.
- `.env` local gerado fora do Git. Volumes `doodba-local-pg13` e
  `doodba-local-filestore` criados pelo script.
- `.\scripts\doodba.ps1 start` subiu `doodba-local` em `127.0.0.1:8069`. Banco
  `doodba_dev` inicializado com módulo `base`.
- Correções reconstruídas na imagem: espera PostgreSQL com usuário `postgres`;
  `set-admin.py` com `Environment.manage()`.
- Validação em [VALIDACAO-P0.md](VALIDACAO-P0.md). Versões em [VERSOES.md](VERSOES.md).
  Operação em [OPERACAO.md](OPERACAO.md).

## 6. Próximas etapas (após P0)

- P1: workspace, Invoke no container, instalação de `local_workshop`/OCA e debug.
- Não instalar localização brasileira Escodoo/OCA neste estágio.

## 7. Limpeza das imagens solicitada pelo usuário

O usuário solicitou parar todos os containers e remover as imagens existentes antes de
continuar a instalação.

- Engine: `desktop-linux` (Docker local).
- Os oito containers existentes já estavam parados.
- Executada verificação de containers ativos; nenhum precisou ser parado.
- Removidas as 13 imagens com `docker --context desktop-linux image rm --force <ID>`
  para cada ID único listado por `docker image ls -aq`.
- Validação: `docker image ls` vazio e `docker system df` indicando zero imagens e zero
  containers ativos.
- Preservados: oito containers parados, dez volumes e cache de build (3,839 GB exibidos
  pelo Docker).
- Não executados `docker system prune`, remoção de volumes ou remoção de containers.
