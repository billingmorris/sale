# -*- coding: utf-8 -*-
{
    'name': 'Crear Cotización desde Productos',
    'version': '16.0.1.0.0',
    'summary': 'Crea una cotización borrador seleccionando varios productos desde la vista lista',
    'description': """
Este módulo agrega una acción en el menú "Acciones" de la vista de lista
(tree) de Productos que permite:

- Seleccionar varios productos (checkbox de la lista).
- Escoger la opción "Crear Cotización" en el menú de Acciones.
- Se abre un wizard que pregunta el Cliente.
- Al confirmar, se crea una cotización (sale.order) en estado borrador
  con los productos seleccionados como líneas de la orden.
- El resto de la información (cantidades, cliente adicional, etc.) se
  completa manualmente dentro de la cotización creada.
""",
    'author': 'Custom Dev',
    'license': 'LGPL-3',
    'category': 'Sales',
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/create_quotation_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
}
