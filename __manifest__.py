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
{
    'name': "Donation management",

    'summary': """
        A module to handle the donation management between sponsors and beneficiaries""",

    'description': """
        This module takes into consideration between the sponsors and beneficiaries. 
        This works by creating beneficiaries that go trough supervision and either be accepted or rejected, then creation of sponsors who can guarantee one or many beneficiaries by createing a kafele(warranty) and pay this warranty in the kafele invoice. 
        The goal of this module is to try to make a simpler interface to handle all the accounting works behind the curtains. 
    """,

    'author': "Abdelrahman Sanjekdar - NavyBits",
    'website': "http://www.navybits.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Tools',
    'version': '0.9',

    # any module necessary for this one to work correctly
    'depends': ['base','account','account_accountant'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/survey.xml',
        'views/survey_workflow.xml',
        'views/beneficiary.xml',
        'views/sponsor.xml',
        'views/donation.xml',
        'views/kafele.xml',
        'views/kafele_invoice.xml',
        'views/menu.xml',
        'views/donation_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}