from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"  # Nome técnico do modelo no Odoo (hr.employee)

    # 1. Adicionar novos campos para a sua interface simplificada
    codigo_interno = fields.Char(string="Código do Servidor/Funcional")
    resumo_status = fields.Char(
        string="Status Consolidado", compute="_compute_resumo_status", store=True
    )

    # 2. Criar lógica computada combinando dados existentes do modelo original
    @api.depends("department_id", "job_id", "active")
    def _compute_resumo_status(self):
        for record in self:
            if not record.active:
                record.resumo_status = "Inativo"
            else:
                depto = record.department_id.name or "Sem Depto"
                cargo = record.job_id.name or "Sem Cargo"
                record.resumo_status = f"{depto} - {cargo}"
