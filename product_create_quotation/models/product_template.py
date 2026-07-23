from odoo import models, _

class ProductTemplate(models.Model):
    _inherit = "product.template"

    def action_create_quotation(self):
        lines = []
        for template in self:
            product = template.product_variant_id
            if product:
                lines.append((0, 0, {
                    "product_id": product.id,
                    "product_uom_qty": 1.0,
                    "product_uom": product.uom_id.id,
                }))
        return {
            "type": "ir.actions.act_window",
            "name": _("Nueva cotización"),
            "res_model": "sale.order",
            "view_mode": "form",
            "target": "current",
            "context": {"default_order_line": lines},
        }
