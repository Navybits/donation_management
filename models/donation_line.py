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

class donation_line(models.Model):
    _name = 'test4.donation_line'

    beneficiary_id = fields.Many2one('res.partner',string=_(u"Beneficiary"),default='_benef',domain=['|',('is_responsible','=',True),('is_beneficiary','=',True)])# ADD DOMAIN
    amount = fields.Float(string=_(u"Amount"),required=True)
    beneficiary_payment_reference_id = fields.Many2one('account.payment',string=_(u"Beneficiary payment reference"),readonly=True)
    payment_method_id = fields.Many2one('account.payment.method', string='Payment Method Type', required=True, oldname='payment_method'
        ,default=lambda self: self.env['account.payment.method'].search([('name','=',"Manual")],limit=1))
    
    donation_id = fields.Many2one('test4.donation',string=_(u"Donation"))

    journal_entry_id = fields.Many2one('account.move',string=_(u"Journal Entry"))

    #Those fields are used in the method donation.transfer_and_create_journal_entries
    #those are needed when creating the journal entries
    source_account_id = fields.Many2one('account.account', string='Source Account',help="To credit")
    dest_account_id = fields.Many2one('account.account', string='Destination Account',help="To debit")
    journal_id = fields.Many2one('account.journal', string='Journal')
    label = fields.Char(string=_(u"Label"))
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account')