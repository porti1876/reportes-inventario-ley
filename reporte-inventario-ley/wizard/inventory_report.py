from odoo import models, fields, api


class InformeReportWiz(models.TransientModel):
    _name = 'informe.report.wiz'
    _description = 'Wizard para las fechas y métodos para crear el reporte F983 v4'

    date_from = fields.Datetime(string='Desde', required=True, default=fields.Datetime.now)
    date_to = fields.Datetime(string='A', required=True, default=fields.Datetime.now)

    def open_table(self):
        # Obtener el intervalo de fechas
        date_from = self.date_from
        date_to = self.date_to

        # Eliminar los registros existentes en inventory.reportf
        self.env['inventory.reportf'].search([]).unlink()

        # Consultar los datos requeridos en base de datos
        query = '''
            INSERT INTO inventory_reportf (product_id, referencia_interna, product_uom_id, category_id, date, inventory_total, cost, journal_cat, costo_total)
            SELECT
                pp.id AS product_id,
                pp.default_code AS referencia_interna,
                pt.uom_id AS product_uom_id,
                pt.categ_id AS category_id,
                %s AS date,
                COALESCE(inv_sum.inventory_total, 0) AS inventory_total,
                pt.list_price AS cost,
                pt.categ_id AS journal_cat,
                COALESCE(inv_sum.inventory_total, 0) * pt.list_price AS costo_total
            FROM
                product_product pp
            INNER JOIN
                product_template pt ON pp.product_tmpl_id = pt.id
            LEFT JOIN (
                SELECT
                    sm.product_id AS product_id,
                    SUM(CASE WHEN sm.date <= %s THEN sm.product_qty ELSE 0 END) AS inventory_total
                FROM
                    stock_move sm
                GROUP BY
                    sm.product_id
            ) inv_sum ON pp.id = inv_sum.product_id
        '''

        self._cr.execute(query, (date_to, date_to))

        # Abrir la vista tree inventory.reportf
        tree_view_id = self.env.ref('reporte-inventario-ley.stock_reporte_inventario_983_view').id
        action = {
            'type': 'ir.actions.act_window',
            'views': [(tree_view_id, 'tree')],
            'view_id': tree_view_id,
            'view_mode': 'tree',
            'name': ('Reporte de inventario F983 V4'),
            'res_model': 'inventory.reportf',
        }
        return action
