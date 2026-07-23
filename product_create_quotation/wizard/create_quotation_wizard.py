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
    line_ids = fields.One2many(
        'product.create.quotation.wizard.line',
        'wizard_id',
        string='Productos',
    )
    amount_total = fields.Float(
        string='Total',
        compute='_compute_amount_total',
    )

    @api.depends('line_ids.subtotal')
    def _compute_amount_total(self):
        for wizard in self:
            wizard.amount_total = sum(wizard.line_ids.mapped('subtotal'))

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

        if 'line_ids' in fields_list:
            res['line_ids'] = [(0, 0, {
                'product_id': product.id,
                'quantity': 1.0,
                'price_unit': product.lst_price,
            }) for product in products]

        return res

    def action_create_quotation(self):
        """Crea una cotización (sale.order) en borrador con los
        productos, cantidades y precios definidos en el wizard."""
        self.ensure_one()

        if not self.line_ids:
            raise UserError('Debe haber al menos un producto seleccionado.')

        order_line_vals = []
        for line in self.line_ids:
            product = line.product_id
            order_line_vals.append((0, 0, {
                'product_id': product.id,
                'product_uom_qty': line.quantity,
                'product_uom': product.uom_id.id,
                'name': product.get_product_multiline_description_sale(),
                'price_unit': line.price_unit,
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


class ProductCreateQuotationWizardLine(models.TransientModel):
    _name = 'product.create.quotation.wizard.line'
    _description = 'Línea de Producto del Wizard de Cotización'

    wizard_id = fields.Many2one(
        'product.create.quotation.wizard',
        string='Wizard',
        required=True,
        ondelete='cascade',
    )
    product_id = fields.Many2one(
        'product.product',
        string='Producto',
        required=True,
    )
    uom_id = fields.Many2one(
        related='product_id.uom_id',
        string='UdM',
        readonly=True,
    )
    quantity = fields.Float(
        string='Cantidad',
        default=1.0,
        required=True,
    )
    price_unit = fields.Float(
        string='Precio Unitario',
    )
    subtotal = fields.Float(
        string='Subtotal',
        compute='_compute_subtotal',
        store=True,
    )

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for line in self:
            if line.product_id:
                line.price_unit = line.product_id.lst_price
