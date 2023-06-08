# -*- coding: utf-8 -*-
{
    'name': "reporte de inventario art 142 A",

    'summary': """
        Modulo para el reporte de control de inventario según el articulo 142A""",

    'description': """
        Modulo para el reporte de control de inventario según el articulo 142A""",

    'author': "Kevin Portillo | Rocketters",
    'website': "https://www.rocketters.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Stock',
    'version': '16.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',

        'data/sequence.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/reporte_inventario.xml',
        'views/reporte_f983.xml',
        'wizard/inventory_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
