from odoo import api, fields, models


class EpiProductTimeline(models.Model):
    """Modelo legado mantido para limpeza sem KeyError."""

    _name = "epi.product.timeline"
    _description = "Modelo Legado para Limpeza"


class ProductProduct(models.Model):
    _inherit = "product.product"

    total_qty_company = fields.Float(
        string="Total Empresa (Soma Global)",
        compute="_compute_total_qty_company",
        search="_search_total_qty_company",
        help=(
            "Quantidade total em mão somando todos os locais físicos "
            "pertencentes à empresa."
        ),
    )

    def _compute_total_qty_company(self):
        for product in self:
            quants = self.env["stock.quant"].search(
                [
                    ("product_id", "=", product.id),
                    ("company_id", "=", self.env.company.id),
                    ("location_id.usage", "=", "internal"),
                ]
            )
            product.total_qty_company = sum(quants.mapped("quantity"))

    def _search_total_qty_company(self, operator, value):
        quants = self.env["stock.quant"].search(
            [
                ("company_id", "=", self.env.company.id),
                ("location_id.usage", "=", "internal"),
                ("quantity", operator, value),
            ]
        )
        product_ids = quants.mapped("product_id").ids
        return [("id", "in", product_ids)]


class EpiTimelineWizard(models.TransientModel):
    _name = "epi.timeline.wizard"
    _description = "Consultor de Timeline de Rastreabilidade"

    product_id = fields.Many2one(
        "product.product",
        string="Produto / EPI",
        required=True,
    )
    lot_id = fields.Many2one(
        "stock.production.lot",
        string="Número de Lote / Série",
    )
    line_ids = fields.One2many(
        "epi.timeline.wizard.line",
        "wizard_id",
        string="Linha do Tempo Registrada",
    )

    @api.onchange("product_id", "lot_id")
    def _onchange_search_timeline(self):
        """Varre o banco auditando estoque, solicitações e alocações."""
        self.line_ids = [(6, 0, [])]

        if not self.product_id:
            return

        events = []

        # 1. Movimentações Físicas de Estoque (Stock Move Line)
        stock_domain = [
            ("product_id", "=", self.product_id.id),
            ("state", "=", "done"),
        ]
        if self.lot_id:
            stock_domain.append(("lot_id", "=", self.lot_id.id))

        moves = self.env["stock.move.line"].search(
            stock_domain,
            order="date asc",
        )
        for move in moves:
            user_emp = move.write_uid.name if move.write_uid else "Sistema"
            desc = (
                f"Movido de '{move.location_id.display_name}' para "
                f"'{move.location_dest_id.display_name}' "
                f"(Qtd: {move.qty_done})"
            )
            events.append(
                {
                    "date": move.date,
                    "event_type": "Logística / Estoque",
                    "reference": (move.reference or move.origin or "Movimentação"),
                    "description": desc,
                    "user_or_employee": user_emp,
                }
            )

        # 2. Registros de Alocação e Posse com o Funcionário
        alloc_models = [
            "hr.employee.ppe",
            "hr.personal.equipment.allocation",
            "hr.personal.equipment.request",
        ]

        for model_name in alloc_models:
            if model_name not in self.env:
                continue

            alloc_env = self.env[model_name]
            prod_field = None
            for candidate in [
                "product_id",
                "product_variant_id",
                "equipment_id",
            ]:
                if candidate in alloc_env._fields:
                    prod_field = candidate
                    break

            if not prod_field:
                continue

            domain = [(prod_field, "=", self.product_id.id)]
            if self.lot_id and "lot_id" in alloc_env._fields:
                domain.append(("lot_id", "=", self.lot_id.id))

            records = alloc_env.search(domain)
            for rec in records:
                emp_name = "N/A"
                if hasattr(rec, "employee_id") and rec.employee_id:
                    emp_name = rec.employee_id.name

                start_date = (
                    getattr(rec, "date_start", None)
                    or getattr(rec, "start_date", None)
                    or getattr(rec, "create_date", None)
                )

                is_valid = getattr(rec, "is_valid", True)
                status_str = "Ativo / Em Posse" if is_valid else "Expirado / Devolvido"

                events.append(
                    {
                        "date": start_date,
                        "event_type": "Posse / Alocado",
                        "reference": f"Alocação #{rec.id}",
                        "description": (
                            "Equipamento entregue ao funcionário. "
                            f"Status da Posse: {status_str}"
                        ),
                        "user_or_employee": emp_name,
                    }
                )

                end_date = getattr(rec, "date_end", None) or getattr(
                    rec, "expiration_date", None
                )
                if end_date and not is_valid:
                    events.append(
                        {
                            "date": end_date,
                            "event_type": "Devolução / Finalizado",
                            "reference": f"Alocação #{rec.id}",
                            "description": ("Equipamento devolvido / posse encerrada."),
                            "user_or_employee": emp_name,
                        }
                    )

        # Ordenar a linha do tempo cronologicamente por data
        events.sort(key=lambda x: x["date"] or fields.Datetime.now())

        # Gerar os registros visuais na tela
        lines = []
        for ev in events:
            lines.append(
                (
                    0,
                    0,
                    {
                        "date": ev["date"],
                        "event_type": ev["event_type"],
                        "reference": ev["reference"],
                        "description": ev["description"],
                        "user_or_employee": ev["user_or_employee"],
                    },
                )
            )

        self.line_ids = lines


class EpiTimelineWizardLine(models.TransientModel):
    _name = "epi.timeline.wizard.line"
    _description = "Linha da Timeline de Rastreabilidade"
    _order = "date desc"

    wizard_id = fields.Many2one("epi.timeline.wizard", ondelete="cascade")
    date = fields.Datetime(string="Data / Hora")
    event_type = fields.Char(string="Etapa")
    reference = fields.Char(string="Documento / Origem")
    description = fields.Text(string="Histórico Auditado")
    user_or_employee = fields.Char(string="Responsável / Funcionário")
