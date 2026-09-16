# Fontes já consultadas

Consulta mais recente: 2026-09-16.

## Playlist e aulas

- [Playlist Escodoo — ambiente de desenvolvimento Odoo](https://www.youtube.com/playlist?list=PLs5WR750kjpdPxmU8vE-nIX1flWABqFvu):
  títulos e sequência. Temas não comprovam os comandos de cada aula.
- [Linux 4 — Criando Ambiente Doodba](https://www.youtube.com/watch?v=AJKrmk55bEo):
  transcrição automática. ~00:43 Odoo 14; ~01:36 PostgreSQL 13; Copier Template;
  ambiente sem proxy de produção.

## GitHub indicado pelo usuário

- [odoo/odoo](https://github.com/odoo/odoo): código Community. P0 usa o ramo `14.0` no
  commit `cc0060e889603eb2e47fa44a8a22a70d7d784185` (último commit público do ramo em
  2024-10-22). A página padrão do repositório em 2026 mostra `19.0`; isso não autoriza
  atualizar o P0.
- [Escodoo](https://github.com/escodoo): organização da playlist. Repositórios de addons
  e fork de `l10n-brazil` são fonte para fases de negócio, não instalados no P0.
- [Escodoo/doodba-copier-template](https://github.com/Escodoo/doodba-copier-template):
  template citado na wiki para Odoo 14 com localização brasileira. Não foi aplicado; o
  P0 parte da imagem Tecnativa.
- [Wiki Escodoo — Doodba](https://github.com/Escodoo/escodoo.github.io/wiki/Doodba)
  (página obtida em 2026-09-16): host Debian/Ubuntu, Copier, Invoke, Compose, porta
  14069, Mailhog/pgweb/wdb, `invoke install -m l10n_br_setup_tests`. Usado só para
  contrastar adaptações; comandos Compose não foram executados.

## Doodba / OCA

- [Tecnativa/doodba](https://github.com/Tecnativa/doodba) e
  [imagem Docker](https://hub.docker.com/r/tecnativa/doodba): base `14.0-onbuild`
  pinada. README local em [fontes/doodba-README.md](fontes/doodba-README.md).
- [Tecnativa/doodba-copier-template](https://github.com/Tecnativa/doodba-copier-template):
  `copier.yml` em [fontes/copier.yml](fontes/copier.yml). Odoo 14 admite PostgreSQL
  10–16; 13 é válido.
- [OCA/web 14.0 / web_responsive](https://github.com/OCA/web/tree/14.0/web_responsive):
  addon extra no P0, commit `790767b14b2a2cb24ca9bfe9c9028e4db9fae4c2`.

As demais aulas da playlist têm tema identificado e procedimento completo ainda não
verificado. P1–P4 não reproduzem a playlist por si só.
