# -*- coding: utf-8 -*-
##############################################################################
#   
#    Copyright (C) 2017 Navybits (<http://www.navybits.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import fields, models, api, exceptions, _
from datetime import date
from dateutil.relativedelta import relativedelta

class kafele(models.Model):
    _name = 'test4.kafele'

    beneficiary_id = fields.Many2one('test4.beneficiary',string=_(u"Beneficiary"),required=True)
    sponsor_id = fields.Many2one('res.partner',string=_(u"Sponsor"),required=True,domain=[('is_sponsor','=',True)])
    kafele_type = fields.Selection([
        ('orphan','Orphan'),('medical','Medical')],string=_(u"Kafele type"),required=True)
    start_date = fields.Date(string=_(u"Start date"),required=True,default=fields.Date.today)
    end_date = fields.Date(string=_(u"End date"))

    def create_invoices(self):
        """ This will create the invoices of the warranty from the next month till the end of the year with all of them in a draft state
        """
        inv = self.env['account.invoice']

        monthes_remaining = abs(date.today().month -12) 
        first_d_month = date(date.today().year,date.today().month,1)
        i =1

        while i <= monthes_remaining:
            vals = {}
            vals['partner_id'] = self.sponsor_id.id
            vals['date_invoice'] = first_d_month + relativedelta(months=+i)

            invoice = inv.create(vals)

            inv_line = self.env['account.invoice.line']
            product = self.env['product.product']
            account = self.env['account.account']
            ### THIS NEEDS TO BE CHANGED
            ### THIS IS THE OLD VERSION, IT IS HARD CODED
            ### NEXT VERSION TO IMPLEMENT NEW VERSION
            account_ac = account.search([('name','=',"Product Sales")],limit=1)
            kaf_prod = product.search([('name','=',"kafele")],limit=1)

            kafele_prod_inv_line = inv_line.create(vals={'product_id':kaf_prod.id
                ,'price_unit':kaf_prod.lst_price,'invoice_id':invoice.id
                ,'account_id':account_ac.id,'name':kaf_prod.name})

            invoice.write({'invoice_id':invoice.id,'invoice_line_ids':kafele_prod_inv_line})

            i+=1
    