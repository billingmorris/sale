# -*- coding: utf-8 -*-
from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_open_add_products_wizard(self):
        """Abre el wizard de selección de productos para esta cotización."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Agregar Productos',
            'res_model': 'sale.order.add.products.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_sale_order_id': self.id,
            },
        }
