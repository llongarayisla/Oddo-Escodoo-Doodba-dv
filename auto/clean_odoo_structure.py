import logging
import sys

import psycopg2

_logger = logging.getLogger(__name__)

DB_CONFIG = {
    "dbname": "devel",
    "user": "odoo",
    "password": "",
    "host": "db",
    "port": "5432",
}

CLEANUP_SCRIPT = """
BEGIN;

-- 1. Desvincular Categorias e Atributos dos Produtos/Templates
UPDATE product_template
SET categ_id = (SELECT id FROM product_category WHERE name = 'All' LIMIT 1);
DELETE FROM product_attribute_value_product_template_attribute_line_rel;
DELETE FROM product_template_attribute_value;
DELETE FROM product_template_attribute_line;
DELETE FROM product_attribute_value;
DELETE FROM product_attribute;

-- 2. Limpar Categorias (Preservando apenas 'All')
DELETE FROM product_category WHERE name != 'All' AND parent_id IS NOT NULL;
DELETE FROM product_category WHERE name != 'All';

-- 3. Limpar Regras de Estoque
DELETE FROM stock_rule;

-- 4. Desvincular e Remover Armazéns e Tipos de Operação
UPDATE stock_warehouse
SET reception_route_id = NULL, delivery_route_id = NULL, crossdock_route_id = NULL;
DELETE FROM stock_warehouse;
DELETE FROM stock_picking_type;

-- 5. Limpar Vinculações e Rotas de Estoque
DELETE FROM stock_route_warehouse;
DO $$
BEGIN
    IF EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_name = 'stock_warehouse_orderpoint_route_rel'
    ) THEN
        DELETE FROM stock_warehouse_orderpoint_route_rel;
    END IF;
    IF EXISTS (
        SELECT FROM information_schema.tables
        WHERE table_name = 'stock_location_route_categ_rel'
    ) THEN
        DELETE FROM stock_location_route_categ_rel;
    END IF;
END $$;

DELETE FROM stock_location_route;

-- 6. Desvincular Locais da Empresa e Limpar Locais Customizados
UPDATE res_company SET internal_transit_location_id = NULL;
DELETE FROM stock_location
WHERE location_id IS NOT NULL
  AND usage NOT IN ('supplier', 'customer', 'inventory', 'production');

-- 7. Atualizar Empresa Principal (Matriz - Porto Alegre)
UPDATE res_company
SET name = 'ISLA Sementes (Porto Alegre)'
WHERE id = 1 OR name LIKE '%San Francisco%';

UPDATE res_partner
SET name = 'ISLA Sementes (Porto Alegre)'
WHERE id = (SELECT partner_id FROM res_company WHERE id = 1);

-- 8. Criar a Filial 'ISLA Sementes (Itapuã)' Clonando Atributos da Matriz
DO $$
DECLARE
    new_partner_id INT;
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM res_company WHERE name = 'ISLA Sementes (Itapuã)'
    ) THEN
        INSERT INTO res_partner (name, is_company, active)
        VALUES ('ISLA Sementes (Itapuã)', TRUE, TRUE)
        RETURNING id INTO new_partner_id;

        CREATE TEMP TABLE temp_company AS SELECT * FROM res_company WHERE id = 1;

        UPDATE temp_company
        SET id = nextval('res_company_id_seq'),
            name = 'ISLA Sementes (Itapuã)',
            partner_id = new_partner_id;

        INSERT INTO res_company SELECT * FROM temp_company;
        DROP TABLE temp_company;
    END IF;
END $$;

COMMIT;
"""


def execute_cleanup():
    try:
        _logger.info("Conectando ao banco de dados PostgreSQL...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        _logger.info("Executando a limpeza de estruturas...")
        cursor.execute(CLEANUP_SCRIPT)

        conn.commit()
        cursor.close()
        conn.close()
        _logger.info("Limpeza concluída com sucesso!")

    except Exception as e:
        _logger.error("Erro ao executar o script de limpeza: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    execute_cleanup()
