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
from odoo import fields, models, api, exceptions,_

class Partner(models.Model):
    _inherit = 'res.partner'

    ### The class partner is inherited to be able work with the accounting modules
    ### Without it i can't use my classes to enter them in the Customer/Vendor fields in the acounting module

    is_beneficiary = fields.Boolean(string=_(u"Is Beneficiary"))
    is_sponsor = fields.Boolean(string=_(u"Is Sponsor"))
    is_responsible = fields.Boolean(string=_(u"Is Responsible"))