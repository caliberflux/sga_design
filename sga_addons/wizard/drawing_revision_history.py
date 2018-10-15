# -*- coding: utf-8 -*-

from odoo import api, fields, models

class DrawingRevisionHistory(models.TransientModel):
    _name = 'drawing.revision.history'
    _description = 'Drawing revision history'
    
    name = fields.Char(string='Reason')
    timestamp_c = fields.Datetime(string='Timestamp',default=fields.Datetime.now)
    revision_code_id = fields.Many2one('revision.code',string='Revision Code')
    revision_sub_code_id = fields.Many2one('revisionsub.code',string='Revision sub Code')
    drawing_number = fields.Char(string='Drawing number')
    drawing_name = fields.Char(string="Drawing name")
    revised_drawing_number = fields.Char(string='Revised drawing number',readonly=True,store=True)
    current_drawing = fields.Binary("Current Drawing", attachment=True,readonly=True,store=True)
    store_fname = fields.Char(string="File Name")
    
    @api.onchange('drawing_name','revision_sub_code_id','revision_code_id')
    def onchange_get_revise_no(self):
        if self.drawing_name or self.revision_code_id or self.revision_sub_code_id:
            if (self.revision_code_id.name and self.revision_sub_code_id.name) != False:
                self.revised_drawing_number = self.drawing_name + '/' + self.revision_code_id.name + self.revision_sub_code_id.name
    
    @api.multi
    def revision_internal(self):
        task_id = self.env.context.get('active_ids')[0]
        task_srch = self.env['project.task'].search([('id','=',task_id)])
        task_srch.revised_drawing_no = self.drawing_name + '/' + self.revision_code_id.name + self.revision_sub_code_id.name
        internal_rev_obj = self.env['internal.revision.history']
        print ("revised drawing number ----------------------",self.revised_drawing_number)
        internal_rev_obj.create({
                                'reason':self.name,
                                'timestamp_c':self.timestamp_c,
                                'revised_drawing_number':self.drawing_name + '/' + self.revision_code_id.name + self.revision_sub_code_id.name,
                                'task_id':task_id
                                })

class DrawingRevisionCustomer(models.TransientModel):
    _name = 'drawing.revision.customer'
    _description = 'Drawing revision history customer'
    
    name = fields.Char(string='Reason')
    timestamp_c = fields.Datetime(string='Timestamp',default=fields.Datetime.now)
    revision_code_id = fields.Many2one('revision.code',string='Revision Code')
    drawing_number = fields.Char(string='Drawing number')
    drawing_name = fields.Char(string="Drawing name")
    revised_drawing_number = fields.Char(string='Revised drawing number',readonly=True,store=True)
    current_drawing = fields.Binary("Current Drawing", attachment=True,readonly=True,store=True)
    store_fname = fields.Char(string="File Name")
    
    @api.onchange('drawing_name','revision_code_id')
    def onchange_get_revise_no_customer(self):
        if self.drawing_name or self.revision_code_id:
            if (self.revision_code_id.name) != False:
                self.revised_drawing_number = self.drawing_name + '/' + self.revision_code_id.name
    
    @api.multi
    def revision_customer(self):
        task_id = self.env.context.get('active_ids')[0]
        print("task id -------------------------",task_id)
        task_srch = self.env['project.task'].search([('id','=',task_id)])
        task_srch.revised_drawing_no = self.drawing_name + '/' + self.revision_code_id.name
        internal_rev_obj = self.env['customer.revision.history']
        print ("revised drawing number ----------------------",self.revised_drawing_number)
        internal_rev_obj.create({
                                'reason':self.name,
                                'timestamp_c':self.timestamp_c,
                                'revised_drawing_number':self.drawing_name + '/' + self.revision_code_id.name,
                                'task_id':task_id
                                })

class RevisionCode(models.Model):
    _name = 'revision.code'
    _description = 'Revision Code'
    
    name = fields.Char(string='Revision code')
    
class RevisionsubCode(models.Model):
    _name = 'revisionsub.code'
    _description = 'Revision Sub Code'
    
    name = fields.Char(string='Revison Sub code')

class InternalRevisionHistory(models.Model):
    _name = 'internal.revision.history'
    _description = 'Revision History'
    
    reason = fields.Char(string='Reason')
    timestamp_c = fields.Datetime(string='Timestamp')
    revised_drawing_number = fields.Char('Revised drawing number')
    task_id = fields.Many2one('project.task',string='Task')
   
class CustomerRevisionHistory(models.Model):
    _name = 'customer.revision.history'
    _description = 'Customer Revision History'
    
    reason = fields.Char(string='Reason')
    timestamp_c = fields.Datetime(string='Timestamp')
    revised_drawing_number = fields.Char('Revised drawing number')
    task_id = fields.Many2one('project.task',string='Task')
    