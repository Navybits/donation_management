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

class donation(models.Model):
    _name = 'test4.donation'

    sponsor_id = fields.Many2one('res.partner',string=_(u"Sponsor"),required=True,domain=[('is_sponsor','=',True)])# ADD DOMAIN
    
    total_amount = fields.Monetary(string=_(u"Total Amount"),required=True)
    #To bypass the error of (Amount should not be zero) when creating the donation
    total_amount_2 = fields.Float(string=_(u"Total Amount"))

    product_id = fields.Many2one('product.product',string=_(u"Product"))

    amount_to_transfer = fields.Float(string=_(u"Amount to transfer"),compute='_compute_amount_to_transfer')
    amount_transfered = fields.Float(string=_(u"Amount Transfered"),compute='_compute_amount_transfered',default=0)
    #To bypass some errors when creating the amount transfered and displaying it
    amount_transfered_2 = fields.Float(string=_(u"Amount Transfered"))
    money_all_received = fields.Boolean(string="MONEY",default=False)

    sp_id = fields.Many2one('test4.sponsor',string=_(u"Sponsor id"))

    account_analytic_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    currency_id = fields.Many2one('res.currency', string='Currency')

    @api.depends('donation_line_ids.beneficiary_payment_reference_id')
    def _compute_amount_transfered(self):
        # self.amount_transfered = 0
        for record in self.donation_line_ids:
            if record.beneficiary_payment_reference_id.id != False:
                self.amount_transfered += record.amount
        self.amount_transfered_2 = self.amount_transfered
        

    @api.one
    @api.depends('donation_line_ids.amount')
    def _compute_amount_to_transfer(self):
        # self.amount_to_transfer = sum(line.amount for line in self.donation_line_ids and )

        for record in self.donation_line_ids:
            if record.beneficiary_payment_reference_id.id== False:
                self.amount_to_transfer += record.amount

        if self.amount_to_transfer + self.amount_transfered > self.total_amount:
            error_msg = _(u"Amount to transfer cannot exceed the total amount\nAmount to transfer:{0} and total amount:{1}".format(self.amount_to_transfer + self.amount_transfered,self.total_amount))
            raise exceptions.ValidationError(error_msg)


    #sponsor_payment_reference_id = fields.Many2one('account.payment',string=_(u"Sponsor payment reference"),readonly=True)
    #beneficiary_payment_reference_id = fields.Many2one('account.payment',string=_(u"Beneficiary payment reference"))
    sponsor_invoice_reference_id = fields.Many2one('account.invoice',string=_(u"Sponsor invoice reference"),readonly=True)

    journal_id = fields.Many2one('account.journal', string='Payment Journal', domain=[('type', 'in', ('bank', 'cash'))]
        ,default=lambda self: self.env['account.journal'].search([('type','=',"cash")],limit=1))
    payment_method_id = fields.Many2one('account.payment.method', string='Payment Method Type', required=True
        ,default=lambda self: self.env['account.payment.method'].search([('name','=',"Manual")],limit=1))
    
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account')

    donation_line_ids = fields.One2many('test4.donation_line','donation_id',string=_(u"Donations"))


    def create_invoice_and_pay(self):
        """ When donating, this will create the invoice and pay it automatically with the total amount donated
        """

        context = {}
        ### TO PASS THE CURRENCY ID, WITHOUT IT, IT IS TAKING THE USD DOLLAR WHICH IS THE DEFAULT COMPANY CURRENCY IN THIS CASE
        context['default_currency_id'] = self.currency_id.id    
        ### TO MAKE THE DEFAULT ACCOUNT IS: ACCOUNT RECEIVABLES
        context['default_account_id'] = self.sponsor_id.property_account_receivable_id.id

        ### Creating the invoice 
        inv = self.env['account.invoice'].with_context(context)

        vals = {}
        vals['partner_id'] = self.sponsor_id.id
        vals['date_invoice'] = date.today()
        vals['account_analytic_id'] = self.account_analytic_id.id
        vals['currency_id'] = self.currency_id.id
        vals['account_id'] = self.sponsor_id.property_account_receivable_id.id
        #vals['journal_id'] = self.journal_id.id # BY DEFAULT CUSTOMER INVOICES ( USD )

        ### Invoice created
        invoice = inv.create(vals)

        ### Invoice line
        inv_line = self.env['account.invoice.line']
        ### Account
        account = self.env['account.account']

        kafele_prod_inv_line = inv_line.create(vals={'product_id':self.product_id.id
            ,'price_unit':self.total_amount,'invoice_id':invoice.id
            ,'account_id':self.product_id.property_account_income_id.id
            ,'name':self.product_id.name,'currency_id':invoice.currency_id.id})
        #PRICE UNIT MUST BE CHANGED 

        ### This line is necessary to write the invoice id and the lines of this invoice
        invoice.write({'invoice_id':invoice.id,'invoice_line_ids':kafele_prod_inv_line})

        ### Open the invoice
        invoice.action_invoice_open()

        ### Pay the invoice with the total amount and the journal id choosed 
        invoice.pay_and_reconcile(self.journal_id,self.total_amount)

        ### Link the new invoice the sponsor_invoice_reference_id to be accessible directly from the view
        self.sponsor_invoice_reference_id = invoice

        self.total_amount_2 = self.total_amount

    def transfer_and_create_journal_entries(self):
        """ This method will transfer the amount entered to the appropriate benefeciaries by creating the journal entries responsible of creating creating the credit/debit movements
        """

        journal_entry = self.env['account.move']
        journal_entry_line = self.env['account.move.line']

        for record in self.donation_line_ids:
            if record.journal_entry_id.id == False:
                journal = journal_entry.create(vals={'date':date.today(),'journal_id':record.journal_id.id})        
               
                ### Debit line
                journal.line_ids.create(vals={'name':record.label,
                    'account_id':record.dest_account_id.id,'partner_id':record.beneficiary_id.id,
                    'debit':record.amount,'date_maturity':date.today(),'move_id':journal.id
                    ,'analytic_account_id':record.analytic_account_id.id})
                ### Credit line
                journal.line_ids.create(vals={'name':record.label,
                    'account_id':record.source_account_id.id,'partner_id':record.beneficiary_id.id,
                    'credit':record.amount,'date_maturity':date.today(),'move_id':journal.id
                    ,'analytic_account_id':record.analytic_account_id.id})
                
                journal.post()
                record.journal_entry_id = journal
                
                self.amount_transfered_2 = self.amount_transfered
                if self.total_amount - self.amount_transfered <0.01 and self.total_amount !=0:
                    self.money_all_received = True

    