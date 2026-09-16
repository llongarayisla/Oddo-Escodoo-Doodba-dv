# Instruções obrigatórias do projeto

## Escopo local

- Este projeto pertence exclusivamente a `L:\Sistemas\Doodba`.
- Manter neste repositório os Dockerfiles, scripts, configurações, código próprio e
  documentação do ambiente.
- Não criar cópias de trabalho em outros projetos, publicar imagens ou configurar
  serviços remotos sem solicitação do usuário.
- O host é Windows. Executar as ferramentas e os serviços do ambiente de desenvolvimento
  em Linux dentro do Docker, tratado operacionalmente como uma VM.

## Imagem e container únicos

- O ambiente final deve utilizar uma única imagem de aplicação e um único container
  Linux do projeto.
- Incluir nesse ambiente os componentes necessários ao Odoo/Doodba, inclusive o
  PostgreSQL quando necessário; não criar uma stack de containers separados.
- Não usar Docker-in-Docker para esconder uma stack de múltiplas imagens ou containers
  dentro do container principal.
- Imagens base e estágios de build não são serviços adicionais: o resultado executado
  deve ser uma única imagem do projeto.
- Documentar qualquer adaptação necessária em relação à arquitetura padrão do Doodba;
  não afirmar que a reprodução é idêntica se houver diferenças.

## Exclusividade de execução

- Antes de abrir, iniciar, reiniciar, instalar, atualizar ou modificar o ambiente
  Doodba, verificar os containers em execução no Docker Engine utilizado pelo projeto.
- Parar todos os containers em execução que não pertençam a este projeto antes de
  prosseguir.
- A instrução do usuário autoriza essa parada; não solicitar novamente aprovação
  funcional para cada container. Respeitar os controles de acesso da ferramenta.
- Inativar significa parar (`docker stop`), nunca remover containers, imagens, volumes
  ou dados.
- Não parar o Docker Engine ou o Docker Desktop, pois são necessários ao projeto.
- Não reiniciar automaticamente os outros containers ao terminar.
- Se não for possível listar ou parar algum container, interromper as operações
  dependentes do ambiente e informar o impedimento.
- Essa verificação precisa integrar o ponto de entrada dos scripts de operação. Uma
  instrução documental sozinha não constitui automação implementada.
- Não instalar monitoramento permanente ou alterar políticas globais de reinício: a
  regra deve ser verificada a cada entrada/operação do projeto.

## Versões e rastreabilidade

- Seguir os procedimentos e versões comprovados na playlist indicada pelo usuário:
  https://www.youtube.com/playlist?list=PLs5WR750kjpdPxmU8vE-nIX1flWABqFvu.
- A transcrição da aula Linux 4 confirma Odoo 14 e PostgreSQL 13. Não substituir por
  versões recentes sem autorização.
- Distinguir versões confirmadas no vídeo, versões não especificadas e decisões de
  adaptação.
- Documentar passos, comandos, resultados e limitações em Markdown em `.agent/docs/` e
  atualizar a execução em `.agent/plan/`, conforme ORGANIZACAO.md. Não inserir
  documentação própria indiscriminadamente em árvores de dependências de terceiros.
- Só declarar a instalação concluída após validar inicialização, banco de dados, acesso
  HTTP e persistência do ambiente.
