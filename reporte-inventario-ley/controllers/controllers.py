# -*- coding: utf-8 -*-
# from odoo import http


# class Reporte-inventario-ley(http.Controller):
#     @http.route('/reporte-inventario-ley/reporte-inventario-ley', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/reporte-inventario-ley/reporte-inventario-ley/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('reporte-inventario-ley.listing', {
#             'root': '/reporte-inventario-ley/reporte-inventario-ley',
#             'objects': http.request.env['reporte-inventario-ley.reporte-inventario-ley'].search([]),
#         })

#     @http.route('/reporte-inventario-ley/reporte-inventario-ley/objects/<model("reporte-inventario-ley.reporte-inventario-ley"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('reporte-inventario-ley.object', {
#             'object': obj
#         })
