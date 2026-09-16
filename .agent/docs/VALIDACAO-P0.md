# Validação P0

Data: 2026-09-16. Contexto Docker: `desktop-linux`. Sem ferramentas de navegador neste
agente; o login web foi exercitado por sessão HTTP real (GET `/web/login` + POST com
CSRF + redirecionamento para `/web`) e XML-RPC `authenticate`.

## Build e versões

- Imagem `doodba-local:14-pg13` reconstruída com cache das camadas Doodba.
- Dentro do container: Odoo Server 14.0, PostgreSQL 13.16, Python 3.8.17, Debian 10,
  `PG_VERSION=13`.
- Código: `odoo/odoo` `cc0060e889603eb2e47fa44a8a22a70d7d784185`.

## Container único e exclusividade

- Após `start`/`recreate`: somente `doodba-local` em execução.
- HTTP publicado em `127.0.0.1:8069` e `127.0.0.1:6899`; Postgres sem porta no host.
- Volumes `doodba-local-pg13` e `doodba-local-filestore` com label do projeto.
- Container temporário `doodba-exclusivity-test` (mesma imagem, `sleep`, sem label) foi
  parado pelo script (`Exited 137` após timeout de stop) e **não** removido por ele.
  Remoção manual só desse recurso de teste. Volumes de outros projetos permaneceram.

Falha forçada de `docker inspect`/`docker stop` não foi injetada. O script lança exceção
se o Engine falhar ou se algum externo continuar ativo; isso está no código, não em
ensaio de falha.

## Banco, login e filestore

- Healthcheck `healthy` (pg_isready + `/web/login` HTTP 200).
- XML-RPC: `admin` autenticou com `uid=2` no banco `doodba_dev`.
- HTTP: POST em `/web/login` terminou em `http://127.0.0.1:8069/web` com cookie
  `session_id`.
- Registro descartável: `res.partner` id 7, nome `P0 persistencia`.
- Anexo id 34, `p0-filestore.txt`, 15 bytes,
  `store_fname=de/debea6e3998f74948312e3deb5b7d45546c93698`, arquivo presente em
  `/var/lib/odoo/filestore/doodba_dev/...`.

## Persistência

| Operação                                               | Partner 7 | Anexo 34 | Login admin |
| ------------------------------------------------------ | --------- | -------- | ----------- |
| Após `restart`                                         | ok        | ok       | ok          |
| Após `recreate` (novo id de container, mesmos volumes) | ok        | ok       | ok          |
| Após `stop` (exit 0) e `start`                         | ok        | ok       | ok          |

## Shell e parada

- `docker exec -u odoo ... bash` executa no Linux do projeto.
- `stop` deixou o container `Exited (0)`; Postgres e Odoo não ficaram no host.
- Correção aplicada e reconstruída: espera do Postgres como usuário `postgres` (peer);
  `set-admin.py` usa `Environment.manage()` do Odoo 14.

## Limitações observadas

- Na primeira subida, `set-admin.py` antigo falhou
  (`AttributeError: 'tuple' object has no attribute 'cache'`); a senha foi definida
  depois da correção. Imagem nova já contém o script corrigido.
- O entrypoint Doodba ainda registra `Peer authentication failed for user "odoo"` no
  socket Unix; a conexão efetiva do Odoo é TCP `127.0.0.1` e o serviço sobe.
- `web_responsive` está ligado; o diretório `custom/src/web` no runtime não conserva
  `.git`.
- Módulo `local_workshop` existe no bind mount e não foi instalado nesta validação
  (escopo P1).
