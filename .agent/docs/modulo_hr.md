# Guia de Reinstalação e Atualização dos Módulos de HR (OCA v14.0)

Este procedimento descreve como resetar a pasta do repositório `hr`, reclonar a branch
14.0 da OCA e forçar a atualização dos módulos customizados no Odoo via Docker/Doodba.

---

### 1. Limpeza e Reclonagem do Repositório HR

Execute os comandos abaixo na sua máquina host para remover o código antigo e obter uma
cópia limpa da branch 14.0:

```bash
cd ~/Projetos/Odoo-Escudo
rm -rf odoo/custom/src/hr
git clone -b 14.0 https://github.com/OCA/hr.git odoo/custom/src/hr
```

---

### 2. Atualização da Lista de Módulos e Instalação via CLI

Utilize a flag `--http-port=8079` para rodar os comandos de atualização do Odoo em uma
porta alternativa, evitando conflito com o container principal que já está ativo na
porta `8069`:

```bash
# Atualiza a lista base de módulos do sistema
docker compose exec odoo odoo -c /opt/odoo/auto/odoo.conf -d prod -u base --http-port=8079 --stop-after-init

# Força a instalação/atualização dos módulos de Equipamento e EPI
docker compose exec odoo odoo -c /opt/odoo/auto/odoo.conf -d prod -i hr_personal_equipment_request,hr_employee_ppe --http-port=8079 --stop-after-init
```

---

### 3. Reinicialização do Container

Após concluir os comandos do CLI, reinicie o serviço do Odoo para aplicar as alterações:

```bash
docker compose restart odoo
```

---

### 4. Localização dos Módulos na Interface Web

1. Acesse o menu **Aplicativos** no Odoo (`http://localhost:14069`).
2. Remova o filtro padrão **Aplicativos** clicando no ícone `x` da barra de busca.
3. Pesquise por `PPE` ou `Personal Equipment`.
4. Os cards dos módulos **Personal Protective Equipment (PPE) Management**
   (`hr_employee_ppe`) e **Hr Personal Equipment Request**
   (`hr_personal_equipment_request`) estarão visíveis e prontos para uso.
