from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    standalone = fields.Float(store=True)