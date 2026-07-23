from odoo import models, _
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def action_create_quotation(self):
        if not self:
            raise UserError(_("Debe seleccionar al menos un producto."))

        order = self.env["sale.order"].create({})

        for template in self:
            product = template.product_variant_id
            if not product:
                raise UserError(
                    _("El producto '%s' no tiene una variante disponible.") % template.display_name
                )

            self.env["sale.order.line"].create({
                "order_id": order.id,
                "product_id": product.id,
                "product_uom_qty": 1.0,
            })

        return {
            "type": "ir.actions.act_window",
            "name": _("Cotización"),
            "res_model": "sale.order",
            "res_id": order.id,
            "view_mode": "form",
            "target": "current",
        }
