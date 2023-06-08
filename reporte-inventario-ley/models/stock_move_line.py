# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, api


class StockMoveLineReporteInventario(models.Model):
    _inherit = 'stock.move.line'

    currency_id = fields.Many2one('res.currency', 'Currency',
                                  default=lambda self: self.env.user.company_id.currency_id.id, required=True)

    # Campos en la vista del reporte artículo 142 A
    correlativo = fields.Char(related='picking_id.origin')

    item = fields.Char(string="Núm Item")
    item_auto = fields.Char(string="Núm Item", default=lambda self: self._get_next_sequence())
    procedencia = fields.Many2one(related="picking_partner_id.country_id")
    qty_done_in = fields.Float(string="Cantidad entrada", compute='_compute_qty_done_in')
    qty_done_out = fields.Float(string="Cantidad salida", compute='_compute_qty_done_out')
    precio_costo_entra = fields.Float(string="Costo por unidad por unidad que entra", compute='_compute_costo_entra',
                                      store=True)
    precio_costo_sale = fields.Float(string="Costo por unidad por unidad que sale", compute='_compute_costo_sale',
                                     store=True)
    saldo_unidad_precio_costo = fields.Float(string="Costo por unidades a precio de costo",
                                             compute='_compute_unidades_costo', store=True)
    mermas = fields.Char(string="Mermas")
    saldo_unidades = fields.Float(string="Saldo en unidades", compute='_compute_saldo_unidades', store=True)


    @api.depends('saldo_unidades', 'product_id.standard_price')
    def _compute_unidades_costo(self):
        for move_line in self:
            move_line.saldo_unidad_precio_costo = move_line.saldo_unidades * move_line.product_id.standard_price

    @api.depends('qty_done_in', 'product_id.lst_price')
    def _compute_costo_sale(self):
        for move_line in self:
            move_line.precio_costo_entra = move_line.qty_done_in * move_line.product_id.list_price

    @api.depends('qty_done_in', 'product_id.standard_price')
    def _compute_costo_entra(self):
        for move_line in self:
            move_line.precio_costo_sale = move_line.qty_done_in * move_line.product_id.standard_price

    @api.depends('date', 'product_id')
    def _compute_saldo_unidades(self):
        for move_line in self:
            product = move_line.product_id
            date = move_line.date
            qty_available = product.with_context(to_date=date).qty_available
            move_line.saldo_unidades = qty_available

    @api.depends('qty_done', 'location_usage', 'location_dest_usage')
    def _compute_qty_done_in(self):
        for move_line in self:
            if (move_line.location_usage in ('internal', 'transit')) and (
                    move_line.location_dest_usage not in ('internal', 'transit')):
                move_line.qty_done_in = move_line.qty_done
            else:
                move_line.qty_done_in = 0.0

    @api.depends('qty_done', 'location_usage', 'location_dest_usage')
    def _compute_qty_done_out(self):
        for move_line in self:
            if (move_line.location_usage not in ('internal', 'transit')) and (
                    move_line.location_dest_usage in ('internal', 'transit')):
                move_line.qty_done_out = move_line.qty_done
            else:
                move_line.qty_done_out = 0.0

    def _get_next_sequence(self):
        now = datetime.now()
        month = now.strftime("%m")
        day = now.strftime("%d")
        year = now.strftime("%Y")
        sequence = self.env['ir.sequence'].next_by_code('account.move.line.item.sequence')
        if not sequence:
            sequence = '1'
        return f"{day}/{sequence}"

    # Campos para informe de inventario 983 v4

    reference_product = fields.Char(related="product_id.default_code")
    uom_product = fields.Many2one(related="product_id.uom_id")

    grouped_qty_available = fields.Float(
        string='Qty Available (Grouped)',
        compute='_compute_grouped_qty_available',
        store=True,
    )
    grouped_product =  fields.Char(string="Producto", compute="_compute_grouped_product", store=True)

    def _compute_grouped_product(self):
        for move_line in self:
            domain = [
                ('product_id', '=', move_line.product_id.id),
                ('date', '<=', move_line.date),
                ('state', '=', 'done')
            ]
            product_ids = self.env['stock.move.line'].search(domain).mapped('product_id')
            grouped_product_ids = list(set(product_ids))
            grouped_product_names = ', '.join([product.display_name for product in grouped_product_ids])
            move_line.grouped_product = grouped_product_names

    def _compute_grouped_qty_available(self):
        for move_line in self:
            domain = [
                ('product_id', '=', move_line.product_id.id),
                ('date', '<=', move_line.date),
                ('state', '=', 'done')
            ]
            qty_available = self.env['stock.move.line'].search(domain).mapped('qty_done')
            move_line.grouped_qty_available = sum(qty_available)



