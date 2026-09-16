# Operação do ambiente P0

Ponto de entrada: `L:\Sistemas\Doodba\scripts\doodba.ps1`. Toda ação lista containers
ativos no contexto `desktop-linux` e para os que não são deste projeto.

```powershell
cd L:\Sistemas\Doodba
Copy-Item .env.example .env   # só na primeira vez; gerar senhas locais
.\scripts\doodba.ps1 build
.\scripts\doodba.ps1 start
.\scripts\doodba.ps1 status
```

| Ação       | Efeito                                                        |
| ---------- | ------------------------------------------------------------- |
| `build`    | Constrói `doodba-local:14-pg13`                               |
| `start`    | Cria volumes do projeto se faltarem e sobe o container        |
| `stop`     | Para só `doodba-local` (exit 0 observado)                     |
| `restart`  | Reinicia o mesmo container                                    |
| `recreate` | Remove só o container do projeto e recria; volumes permanecem |
| `shell`    | `bash` como usuário `odoo` (requer TTY)                       |
| `logs`     | Últimas 120 linhas                                            |
| `status`   | Estado e healthcheck                                          |
| `versions` | Invoke `versions` dentro do Linux                             |
| `exec ...` | Comando arbitrário no container                               |

## Acesso

- URL: http://127.0.0.1:8069
- Banco: `doodba_dev`
- Usuário: `admin`
- Senha: `ODOO_ADMIN_PASSWORD` no `.env` local (não versionado)

PostgreSQL não é publicado no host. Cliente: `.\scripts\doodba.ps1 exec psql`.

## Backup conjunto (banco + filestore)

Os dois volumes precisam ser copiados juntos. Não usar `docker volume rm` como
recuperação.

```powershell
.\scripts\doodba.ps1 stop
docker --context desktop-linux run --rm --volumes-from doodba-local -v ${PWD}\.local\backup:/backup debian:buster-slim tar -C / -cf /backup/pgdata.tar var/lib/postgresql/data
docker --context desktop-linux run --rm --volumes-from doodba-local -v ${PWD}\.local\backup:/backup debian:buster-slim tar -C / -cf /backup/filestore.tar var/lib/odoo
```

Com o container parado, `--volumes-from` só funciona se o container ainda existir.
Alternativa: montar os volumes nomeados `doodba-local-pg13` e `doodba-local-filestore`.
Restauração inverte o `tar` nos mesmos destinos, sem apagar o volume como primeiro
passo.

## Limites

- Operações feitas só pelo Docker Desktop ou `docker` cru não passam pela exclusividade.
- Não há monitoramento permanente nem restart de outros projetos ao sair.
- Debug na porta `127.0.0.1:6899` está publicada; o uso fica para o P1.
