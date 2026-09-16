---
name: recuperar-docker-linux
description:
  Diagnosticar conexão ausente com o Docker Desktop Linux no Windows deste projeto e
  recuperar o backend parado sem remover dados.
---

# Recuperar Docker Linux parado

## Quando aplicar

Docker CLI está instalado, mas a conexão falha porque o named pipe do Engine não existe.
Caso observado: Docker Desktop 4.81.0, Engine 29.6.1, Windows, backend `docker-desktop`
do WSL 2 parado. Não tratar qualquer falha de build ou erro de permissão como esse mesmo
problema.

## Diagnóstico

```powershell
docker context ls
docker --context desktop-linux version
wsl --list --verbose
Test-Path 'C:\Program Files\Docker\Docker\Docker Desktop.exe'
```

No caso comprovado, o sandbox também não conseguia ler `.docker/config.json` e mostrava
contexto `default`. Repetir a inspeção com a permissão apropriada da ferramenta revelou
o contexto real `desktop-linux`. Não editar credenciais, configuração Docker ou ACLs
para contornar restrição do sandbox.

## Solução comprovada para backend parado

Com Docker Desktop instalado no caminho verificado e tarefa de Docker autorizada:

```powershell
Start-Process -FilePath 'C:\Program Files\Docker\Docker\Docker Desktop.exe' -WindowStyle Hidden
docker --context desktop-linux version
```

Esperar a inicialização com verificações limitadas, sem reiniciar repetidamente o
Desktop. Sucesso exige seção `Server` acessível com `OS/Arch: linux/amd64` (arquitetura
observada neste host), e não apenas a seção `Client`.

Depois, aplicar a regra de exclusividade do projeto antes de operar o Doodba. Não
remover imagens/volumes nem executar factory reset, prune ou reinstalação como parte
desta solução. A limpeza de imagens feita na sessão foi outra solicitação do usuário e
não era necessária para recuperar o Engine.

Se o serviço continuar inacessível após inicialização, ou o erro for diferente,
registrar a saída sem segredos e investigar o novo diagnóstico; esta skill não comprova
solução para virtualização desabilitada, corrupção de disco ou WSL.

## Evidência

A sequência acima tornou o Engine acessível na sessão do projeto. Registro:
[instalação, etapas 1 e 2](../../docs/INSTALACAO.md).
