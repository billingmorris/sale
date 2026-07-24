# -*- coding: utf-8 -*-
from odoo import fields, models
from odoo.exceptions import UserError


class SaleOrderAddProductsWizard(models.TransientModel):
    _name = 'sale.order.add.products.wizard'
    _description = 'Agregar Productos a la Cotización'

    sale_order_id = fields.Many2one(
        'sale.order',
        string='Cotización',
        required=True,
        readonly=True,
    )
    product_ids = fields.Many2many(
        'product.product',
        string='Productos',
        domain=[('sale_ok', '=', True)],
        help='Selecciona uno o varios productos para agregarlos como '
             'nuevas líneas de la cotización.',
    )

    def action_add_products(self):
        """Crea una línea de pedido por cada producto seleccionado que
        aún no esté en la cotización."""
        self.ensure_one()

        if not self.product_ids:
            raise UserError('Debe seleccionar al menos un producto.')

        order = self.sale_order_id
        existing_products = order.order_line.mapped('product_id')

        order_line_vals = []
        for product in self.product_ids:
            if product in existing_products:
                # Evita duplicar una línea si el producto ya está en el pedido
                continue
            order_line_vals.append((0, 0, {
                'product_id': product.id,
                'product_uom_qty': 1.0,
                'product_uom': product.uom_id.id,
                'name': product.get_product_multiline_description_sale(),
                'price_unit': product.lst_price,
            }))

        if order_line_vals:
            order.write({'order_line': order_line_vals})

        return {'type': 'ir.actions.act_window_close'}
