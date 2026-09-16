# Pastas técnicas do P0

Documentação das pastas próprias, conforme a convenção em `.agent/rules/ORGANIZACAO.md`.
Não há README duplicado dentro de cada pasta.

## `docker/`

Entrada Linux do container único: `entrypoint.sh` (initdb PostgreSQL 13, recusa cluster
≠ 13), `supervisord.conf`, `start-odoo.sh` (espera peer como `postgres`, cria
papel/banco, instala `base` se vazio, define senha admin, executa o entrypoint Doodba),
`prepare-db.py`, `set-admin.py`, `healthcheck.sh` (Postgres + `/web/login`).

## `scripts/`

`doodba.ps1`: exclusividade no contexto `desktop-linux` e ações
`build|start|stop|restart|recreate|shell|logs|status|versions|exec`.
`scripts/linux/tasks.py`: tarefa Invoke `versions` rodando só dentro do container.

## `custom/`

Contrato Doodba ONBUILD. `src/repos.yaml` puxa `odoo/odoo` 14.0 e `OCA/web` 14.0 em
commits fixos. `src/addons.yaml` ativa `web_responsive` e `local_workshop`.
`conf.d/100-local.conf` define `data_dir=/var/lib/odoo` e workers 0.
`dependencies/apt.txt` instala `postgresql-13` e `supervisor`. Código editável:
`custom/src/private`.

## Volumes (não estão no Git)

`doodba-local-pg13` → `/var/lib/postgresql/data`. `doodba-local-filestore` →
`/var/lib/odoo`. Criados pelo script com a label do projeto.
