from odoo import models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def action_create_quotation(self):
        self.ensure_one() if len(self) == 1 else None

        order_lines = []

        for template in self:
            # Obtener la variante correspondiente
            product = template.product_variant_id

            if product:
                order_lines.append((0, 0, {
                    "product_id": product.id,
                    "name": product.get_product_multiline_description_sale(),
                    "product_uom_qty": 1.0,
                    "product_uom": product.uom_id.id,
                    "price_unit": product.lst_price,
                }))

        context = dict(self.env.context)
        context.update({
            "default_order_line": order_lines,
        })

        return {
            "type": "ir.actions.act_window",
            "name": _("Nueva cotización"),
            "res_model": "sale.order",
            "view_mode": "form",
            "views": [(False, "form")],
            "target": "current",
            "context": context,
        }
