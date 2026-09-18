from odoo import fields, models


class MeuExemplo(models.Model):
    _name = "meu.exemplo"
    _description = "Exemplo de Modelo"

    name = fields.Char(string="Nome", required=True)
    description = fields.Text(string="Descrição")
