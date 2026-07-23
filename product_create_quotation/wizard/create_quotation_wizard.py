# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import UserError


class ProductCreateQuotationWizard(models.TransientModel):
    _name = 'product.create.quotation.wizard'
    _description = 'Crear Cotización desde Productos Seleccionados'

    partner_id = fields.Many2one(
        'res.partner',
        string='Cliente',
        required=True,
        help='Cliente para el cual se creará la cotización.',
    )
    product_ids = fields.Many2many(
        'product.product',
        string='Productos Seleccionados',
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids') or []

        if not active_ids:
            return res

        products = self.env['product.product']

        if active_model == 'product.template':
            templates = self.env['product.template'].browse(active_ids)
            # Toma la variante principal de cada plantilla seleccionada
            products = templates.mapped('product_variant_id')
        elif active_model == 'product.product':
            products = self.env['product.product'].browse(active_ids)

        if 'product_ids' in fields_list:
            res['product_ids'] = [(6, 0, products.ids)]

        return res

    def action_create_quotation(self):
        """Crea una cotización (sale.order) en borrador con los
        productos seleccionados como líneas de la orden."""
        self.ensure_one()

        if not self.product_ids:
            raise UserError('Debe haber al menos un producto seleccionado.')

        order_line_vals = []
        for product in self.product_ids:
            order_line_vals.append((0, 0, {
                'product_id': product.id,
                'product_uom_qty': 1.0,
                'product_uom': product.uom_id.id,
                'name': product.get_product_multiline_description_sale(),
                'price_unit': product.lst_price,
            }))

        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
            'order_line': order_line_vals,
        })

        return {
            'type': 'ir.actions.act_window',
            'name': 'Cotización',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': sale_order.id,
            'target': 'current',
        }
