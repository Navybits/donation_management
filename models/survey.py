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

class survey(models.Model):
    _name = 'test4.survey'
    _inherit = 'mail.thread'

    ##### BEGIN WORKFLOW DETAILS #####
    state = fields.Selection([
        ('draft', _(u"Draft")),
        ('review',_(u"Review")),
        ('reject',_(u"Rejected")),
        ('approved', _(u"Approved")),
    ])

    @api.multi
    def action_draft(self):
        self.state = 'draft'
        # user = self.env['res.users'].browse(self.env.uid)

    @api.multi
    def action_review(self):
        self.state = 'review'
        self.send_email_review()

    @api.multi
    def action_reject(self):
        self.state = 'reject'
        is_rejected = True
        
    @api.multi
    def action_approved(self):
        self.state = 'approved'

        #To assign who approved the survey
        self.approved_by_id = self._uid

        #Create survey as a partner
        self.create_survey_as_beneficiary()
        self.create_survey_as_partner()

        #Send email to all the users who have workflow admin access
        self.send_email_to_group_workflow_admin_2()

    @api.multi
    def send_email_review(self):
        group = self.env['res.groups'].search([('name', '=', 'Test4 / Workflow Admin')])
        recipient_partners = []
        for recipient in group.users:         
            recipient_partners.append(
                (4, recipient.partner_id.id)
            )

        mail_details = {'subject': "notification about review for partner creation",
             'body': "<p>Partner needs to be reviewed from the survey:"+self.type_survey+"</p>"
             +"<p>User created the survey:"+ self.user_id.name,
             'partner_ids': recipient_partners
             } 

        mail = self.env['mail.thread']
        mail.message_post(type="notification", subtype="mt_comment", **mail_details)
        self.message_post(type="notification", subtype="mt_comment", **mail_details) # THIS TO POST IT IN THE CHATTER BOX

    @api.multi
    def send_email_to_group_workflow_admin_2(self):
        ### This needs to be changed to be less hard coded
        group = self.env['res.groups'].search([('name', '=', 'Test4 / Workflow Admin')])
        recipient_partners = []
        for recipient in group.users:         
            recipient_partners.append(
                (4, recipient.partner_id.id)
            )
        #body = self.message_target
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')

        url_link = base_url+"/"+"web?#"+"id="+str(self.partner_id.id)+"&view_type=form&model=res.partner"

        string_button =self._create_button_email(url_link,"View Partner")

        subject = "Notification about partner creation"
        body = "<p>Partner approved</p><p>this email sent from python code</p>"+"<p>=====</p><p>Details:</p><p>Survey type: "+self.type_survey+"</p><p>Partner name:"+self.partner_id.name+"</p>"+"<p>User created the survey:"+self.user_id.name+"</p>"+"<p>User approved the survey:"+self.approved_by_id.name+"</p>"+"<p>"+string_button+"</p>"+"<p>=====</p>"

        mail_details = self._fill_email(subject,body)
        mail_details['partner_ids']= recipient_partners

        mail = self.env['mail.thread']
        mail.message_post(type="notification", subtype="mt_comment", **mail_details)
        self.message_post(type="notification", subtype="mt_comment", **mail_details)

    def _create_button_email(self,url_link,button_string):
        string_button ="<a href=\""+url_link+"\" style=\"padding: 5px 10px; font-size: 12px; line-height: 18px; color: #FFFFFF; border-color:#875A7B; text-decoration: none; display: inline-block; margin-bottom: 0px; font-weight: 400; text-align: center; vertical-align: middle; cursor: pointer; white-space: nowrap; background-image: none; background-color: #875A7B; border: 1px solid #875A7B; border-radius:3px\">"+button_string+"</a>"
        return string_button

    def _fill_email(self,subject,body):
        mail_details ={'subject':subject,'body':body}
        return mail_details

    ##### END WORKFLOW DETAILS #####

    ##### BEGIN ADDRESS DETAILS #####
    region = fields.Char(string=_(u"Region"))
    street = fields.Char(string=_(u"Street"))
    near = fields.Char(string=_(u"Near"))
    beside = fields.Char(string=_(u"Beside"))
    above = fields.Char(string=_(u"Above"))
    facing = fields.Char(string=_(u"Facing"))
    building = fields.Char(string=_(u"Building"))
    floor = fields.Char(string=_(u"Floor #"))
    ##### END ADDRESS DETAILS #####

    ##### BEGIN PERSONAL DETAILS #####
    beneficiary_name = fields.Char(string=_(u"Beneficiary Name"))
    phone = fields.Char(string=_("Phone"))
    mobile = fields.Char(string=_("Mobile"))
    serial_number = fields.Char(string=_(u"Serial Number")) # THIS SHOULD BE AUTOGENERATED
    gender = fields.Selection(string=_(u"Gender"), 
        selection=[('male',_(u'male')),('female',_(u'female'))],readonly=False)
    is_responsible = fields.Boolean(String =_(u"is responsible"),default=False)
    reasons_for_help = fields.Selection(string=_(u"reasons for help"),
        selection=[('widow',_(u'widow')),('divorced',_(u'divorced')),('special_needs',_(u'special needs')),
        ('education',_(u'education')),('schoolarship',_(u'schoolarship')),('job_review',_(u'job review')),
        ('voluneteer',_(u'voluneteer')),('acc_voc_training',_(u'accelerated vocational training'))],readonly=False)
    
    ##### END PERSONAL DETAILS #####

    ##### BEGIN survey DETAILS #####
    # name = fields.Char(string=_(u"Survey Name"),required=True)
    is_rejected = fields.Boolean(string=_(u"Rejected"),default=False)
    date_created = fields.Date(string=_(u"Date"),default=fields.Date.today)
    type_survey = fields.Selection(string=_(u"Survey Type"),selection='_get_survey_types')
    notes = fields.Text(String=_(u"Additional notes"))
    def _get_survey_types(self):
        survey_types = [('site_survey',"Site survey")]
        return survey_types

    #To represet the user who created the istimara:
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user
        ,readonly=True,string=_(u"User filled the istimara"))
    #To represent who approved the istimara:
    approved_by_id = fields.Many2one('res.users',string=_(u"User approved the istimara"),readonly=True)
    
    #To represent the beneficiary that this survey belongs to
    beneficiary_id = fields.Many2one('test4.beneficiary',string=_(u"Beneficiary")) 

    ##### END survey DETAILS #####

    def create_survey_as_beneficiary(self):
        ### Get reference on the partner object
        beneficiary_object = self.env['test4.beneficiary']

        ### Values to pass
        vals = {'region':self.region,'street':self.street,
        'near':self.near,'beside':self.beside,'above':self.above,
        'facing':self.facing,'building':self.building,'floor':self.floor,
        'serial_number':self.serial_number,'name':self.beneficiary_name,'is_responsible':self.is_responsible,
        'gender':self.gender,'phone':self.phone,'mobile':self.mobile,'notes':self.notes}

        ### Create the beneficiary
        beneficiary_approved = beneficiary_object.create(vals)

        ### Point the beneficiary id to the beneficiary approved
        self.beneficiary_id = beneficiary_approved
        self.beneficiary_id.main_survey_id=self.id

    def create_survey_as_partner(self):
        ### Get reference on the partner object
        partner_object = self.env['res.partner']

        ### Values to pass
        vals = {
        'name':self.beneficiary_name,
        'phone':self.phone,'mobile':self.mobile,'notes':self.notes,'is_beneficiary':True
        }

        ### Create the beneficiary
        partner_created = partner_object.create(vals)
        
        self.beneficiary_id.partner_id = partner_created

    @api.model
    def create(self, vals):
        rec = super(survey, self).create(vals)

        rec.serial_number = rec.id

        return rec
