# Copyright 2020, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class InventoryReportF(models.Model):
    _name = 'inventory.reportf'
    _description = 'Modelo para datos de reporte de inventario F983 v4'
    _order = 'date desc'

    # currency_id = fields.Many2one('res.currency', 'Currency',
    #                               default=lambda self: self.env.user.company_id.currency_id.id, required=True)
    product_id = fields.Many2one('product.product', readonly=True)
    referencia_interna = fields.Char('Referencia interna', readonly=True)
    product_uom_id = fields.Many2one('uom.uom', readonly=True)
    category_id = fields.Many2one('product.category', readonly=True)
    date = fields.Datetime(readonly=True)
    inventory_total = fields.Float(readonly=True)
    cost = fields.Float(readonly=True)
    journal_cat = fields.Many2one('account.account', readonly=True)
    costo_total = fields.Float(readonly=True)
