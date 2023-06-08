from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    standard_price = fields.Float(store=True)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    my_qty_available = fields.Float(compute='_compute_my_qty_available', store=True)

    @api.depends('qty_available')
    def _compute_my_qty_available(self):
        for product in self:
            product.my_qty_available = product.qty_available
