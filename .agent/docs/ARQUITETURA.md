# Arquitetura do P0 — container único

## Fluxo das aulas e da wiki Escodoo

A [playlist](https://www.youtube.com/playlist?list=PLs5WR750kjpdPxmU8vE-nIX1flWABqFvu) e
a [wiki Doodba da Escodoo](https://github.com/Escodoo/escodoo.github.io/wiki/Doodba)
descrevem o Doodba convencional:

- Copier (`tecnativa/doodba-copier-template` ou o fork Escodoo).
- Docker Compose (`devel.yaml`) com vários serviços: Odoo, PostgreSQL, e na wiki também
  Mailhog, pgweb e wdb.
- Tarefas Invoke no host Linux: `develop`, `img-build`, `git-aggregate`, `preparedb`,
  `start`.
- Odoo 14 na porta `14069`.

Esse fluxo viola a regra deste repositório: uma imagem final e um container Linux.

## O que foi mantido do Doodba

- Imagem-base `tecnativa/doodba:14.0-onbuild` (ONBUILD clona código, instala
  `custom/dependencies`, gera addons).
- Árvore `custom/` (`src/repos.yaml`, `src/addons.yaml`, `src/private`, `conf.d`,
  `dependencies`).
- Entrypoint Doodba para concatenar `odoo.conf` e ligar addons em
  `/opt/odoo/auto/addons`.
- Ferramentas da imagem: `odoo`, `git-aggregator`, `click-odoo`, `addons`.

## O que foi adaptado

| Aula / wiki                              | Este projeto                                                                                       |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Compose com Postgres separado            | PostgreSQL 13 no mesmo container, só em `127.0.0.1:5432`                                           |
| `invoke start` no host Linux             | `scripts/doodba.ps1` no Windows, ferramentas Python no Linux                                       |
| Porta 14069 e HTTPS local                | `http://127.0.0.1:8069`                                                                            |
| Mailhog, pgweb, wdb, Traefik             | ausentes no P0                                                                                     |
| Template Escodoo + `l10n_br_setup_tests` | Odoo oficial + `web_responsive`; localização brasileira fica para fase posterior                   |
| PGDATA em volume Compose `db`            | volumes nomeados `doodba-local-pg13` e `doodba-local-filestore` no armazenamento do Docker Desktop |

PID 1 é o supervisord. Ele arranca `postgres` (usuário `postgres`) e `odoo` (usuário
`odoo`). O entrypoint local inicializa o cluster se `PG_VERSION` estiver ausente e
recusa cluster diferente de 13.

## Persistência

Bind mount NTFS para PGDATA não foi usado. Os dados ficam em volumes Linux do Docker
Desktop. Código próprio em `custom/src/private` é bind-mounted para edição no Windows.
Configuração e backups continuam neste repositório; o armazenamento global do Docker não
foi movido.

## Exclusividade

`scripts/doodba.ps1` fixa o contexto `desktop-linux`, identifica o container por nome
`doodba-local` e label `local.doodba.project=workspace-doodba`, para os demais com
`docker stop` e aborta se algum externo continuar ativo. Não remove volumes nem imagens
alheias.
