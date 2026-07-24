# -*- coding: utf-8 -*-
{
    'name': 'Agregar Productos a Cotización desde Wizard',
    'version': '16.0.1.0.0',
    'summary': 'Botón en la cotización para seleccionar varios productos desde un wizard y añadirlos a las líneas de pedido',
    'description': """
Agiliza la elaboración de cotizaciones (sale.order):

- En el formulario de la cotización aparece el botón "Agregar Productos"
  (visible mientras la cotización está en Borrador o Enviada).
- Al hacer clic se abre un wizard con la lista completa de productos
  vendibles, donde se pueden seleccionar varios a la vez.
- Al confirmar, los productos seleccionados se agregan como nuevas
  líneas de pedido de la cotización, con cantidad 1 por defecto.
- Las cantidades, descuentos, impuestos, etc. se terminan de ajustar
  manualmente en la propia cotización.
""",
    'author': 'Custom Dev',
    'license': 'LGPL-3',
    'category': 'Sales',
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sale_order_add_products_wizard_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
}
