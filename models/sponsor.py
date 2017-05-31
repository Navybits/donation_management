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

class sponsor(models.Model):
    _name = 'test4.sponsor'

    ##### BEGIN PERSONAL DETAILS #####
    name = fields.Char(string=_(u"Name"))
    serial_number = fields.Char(string=_(u"Serial Number"))
    phone_number = fields.Char(string=_(u"Phone Number"))
    home_number = fields.Char(string=_(u"Home Number"))
    email = fields.Char(string=_(u"Email"))
    address = fields.Char(string=_(u"Address"))
    job = fields.Char(string=_(u"Job"))
    notes = fields.Text(string=_(u"Notes"))
    ##### END PERSONAL DETAILS #####

    ##### BEGIN BENEFICIARY DETAILS #####
    beneficiary_ids = fields.Many2many('test4.beneficiary',string=_(u"Beneficiaries"))

    ### The link to the partner associated with
    ### It may benefit us in some way, i guess ?
    partner_id = fields.Many2one('res.partner',string=_(u"Partner id"))
    ##### BEGIN BENEFICIARY DETAILS #####

    @api.model
    def create(self,vals):
        ### Create sponsor
        sp = super(sponsor,self).create(vals)

        vals['is_sponsor']=True

        partner_id = self.env['res.partner'].create(vals)

        return sp