# Versões efetivas do P0

Consulta: 2026-09-16. Valores medidos no container `doodba-local` e na imagem
`doodba-local:14-pg13`.

## Confirmado na aula (Linux 4)

| Componente | Versão | Fonte                                                          |
| ---------- | ------ | -------------------------------------------------------------- |
| Odoo       | 14     | [Linux 4](https://www.youtube.com/watch?v=AJKrmk55bEo), ~00:43 |
| PostgreSQL | 13     | mesma aula, ~01:36                                             |

## Medido nesta instalação

| Componente         | Valor efetivo                                                                                                                                        | Origem da escolha                                                                               |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Imagem do projeto  | `doodba-local:14-pg13` digest `sha256:66376685d956dfb965de70c5cfc933538fd315a8376fbe012027aec3e6a63260`                                              | build local após correções de entrada                                                           |
| Imagem-base Doodba | `tecnativa/doodba:14.0-onbuild@sha256:632793299e2114f1266fee1dc547ab3fe68cfc6df0caaff4840ad6d64cf40df6`                                              | pin explícito; Hub já publica digest mais novo (`104f23b75d5d` em 2026-09-15) e não foi adotado |
| Distribuição       | Debian GNU/Linux 10 (buster)                                                                                                                         | imagem Doodba 14.0; a aula não fixou a distro                                                   |
| Python             | 3.8.17                                                                                                                                               | imagem Doodba 14.0; a aula não fixou o Python                                                   |
| Odoo               | Server 14.0                                                                                                                                          | `odoo --version` no container                                                                   |
| Código Odoo        | [odoo/odoo](https://github.com/odoo/odoo) ramo `14.0`, commit `cc0060e889603eb2e47fa44a8a22a70d7d784185` (2024-10-22, último commit público do ramo) | `custom/src/repos.yaml`; fonte indicada pelo usuário                                            |
| PostgreSQL         | 13.16 (`Debian 13.16-1.pgdg100+1`)                                                                                                                   | pacote `postgresql-13` no build; cluster `PG_VERSION=13`                                        |
| OCA web            | [OCA/web](https://github.com/OCA/web) `14.0`, commit `790767b14b2a2cb24ca9bfe9c9028e4db9fae4c2` (2026-05-18)                                         | `repos.yaml`; `.git` removido no build Doodba                                                   |
| Invoke             | 2.2.0                                                                                                                                                | `custom/dependencies/pip.txt`                                                                   |
| debugpy            | 1.8.1                                                                                                                                                | mesmo arquivo; uso de debug fica para o P1                                                      |
| Host Docker        | Desktop 4.81.0, Engine 29.6.1, linux/amd64, contexto `desktop-linux`                                                                                 | host Windows; não vem da aula                                                                   |

## Não confirmado nos vídeos

- Revisão exata do Copier Template usada na gravação.
- Versões de Copier, pipx e Invoke da máquina da aula.
- Porta 14069, Mailhog, pgweb e wdb da
  [wiki Escodoo](https://github.com/Escodoo/escodoo.github.io/wiki/Doodba):
  deliberadamente não reproduzidos (container único, HTTP só em `127.0.0.1:8069`).
- Template
  [Escodoo/doodba-copier-template](https://github.com/Escodoo/doodba-copier-template)
  com localização brasileira: fora do P0.
