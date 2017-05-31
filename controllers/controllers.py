# -*- coding: utf-8 -*-
from odoo import http

# class Test4(http.Controller):
#     @http.route('/test4/test4/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/test4/test4/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('test4.listing', {
#             'root': '/test4/test4',
#             'objects': http.request.env['test4.test4'].search([]),
#         })

#     @http.route('/test4/test4/objects/<model("test4.test4"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('test4.object', {
#             'object': obj
#         })