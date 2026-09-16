# Regras de negócio do ambiente

## Solicitação do usuário

> O docker deve ser uma img apenas e não varias e nesse repositorio local apenas, sempre
> que abrir ou for mexer no doodba inativar qualquer outro docker em execução.

## Critérios de implementação

1. Entregar uma única imagem final e operar um único container Linux do projeto.
2. Concentrar código e configuração em `L:\Sistemas\Doodba`.
3. Antes de cada operação no ambiente, listar os containers ativos e parar os demais.
4. Preservar os dados dos containers parados; não executar remoções nem limpeza global.
5. Bloquear a operação se a verificação de exclusividade falhar.
6. Não reativar outros containers automaticamente ao encerrar o trabalho.
7. Documentar as diferenças em relação às aulas e validar os serviços necessários dentro
   do container único.

## Consequência arquitetural

O fluxo convencional de Doodba usa Docker Compose com serviços separados. A exigência de
imagem/container únicos requer adaptar a execução, incluindo o banco de dados no mesmo
ambiente Linux. Não executar o Compose convencional sem realizar essa adaptação.

O Docker Desktop armazena internamente imagens, camadas e metadados em seu próprio
armazenamento gerenciado. A restrição de repositório local aplica-se aos arquivos do
projeto; ela não altera a localização global de armazenamento do Docker Desktop. O local
de persistência dos dados deverá ser documentado na implementação.

## Alcance da exclusividade

Aplicar a regra ao Docker Engine selecionado para o projeto, inicialmente
`desktop-linux`. Não acessar nem interromper daemons remotos ou outros hosts. A parada
pode interromper outros trabalhos locais, conforme solicitado pelo usuário.
