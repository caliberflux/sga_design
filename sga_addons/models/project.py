# -*- coding: utf-8 -*-

###########################################################################################
#
#  Caliberflux (<http://www.caliberflux.com>).
#
#  This license applies only to the part of this software that is
#  not distributed as part of Odoo Community or Enterprise Edition.
#
#  This software and associated files (the "Software") can only be used
#  (executed, modified, executed after modifications) with a valid purchase
#  agreement from Caliberflux.
#
#  It is forbidden to publish, distribute, sublicense, or sell copies of the
#  Software or modified copies of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#  ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#
###########################################################################################

from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, AccessError
from lxml import etree

class Project(models.Model):
    _inherit = "project.project"
    
    def _get_default_type_common(self):
        ids = self.env['project.task.type'].search([
            ('case_default', '=', True)])
        return ids

    type_ids = fields.Many2many(
        default=lambda self: self._get_default_type_common())
    
    project_code = fields.Char(string='Project code')
    project_user = fields.Many2many('res.users')
    first_approvee = fields.Many2one('res.users',string='Team Leader')
    second_approvee = fields.Many2one('res.users',string='QC')
    third_approvee = fields.Many2one('res.users',string='Dispatch')
    state = fields.Selection([('s0',('Competition')),
                                ('s1',('Concept Design')),
                                ('s2',('Design Finalization')),
                                ('s3',('Submission')),
                                ('s4',('Estimation')),
                                ('s5',('Tender')),
                                ('s6',('Working Drawing')),
                                ('s7',('As Built'))
                              ],string='Milestones', default= 's0')
    sector_id = fields.Many2one('sector',string='Sector')
    # department_ids = fields.One2many('department','project_id',string='Departments')
    department_ids = fields.Many2many('department')
    building_type_ids = fields.One2many('building.type.line','project_id',string='Building Type')

class ProjectTaskTimer(models.Model):
    _inherit = 'project.task'

    def _compute_is_user_working(self):
        """ Checks whether the current user is working """
        for order in self:
            if order.timesheet_ids.filtered(lambda x: (x.user_id.id == self.env.user.id) and (not x.date_end)):
                order.is_user_working = True
            else:
                order.is_user_working = False

    @api.multi
    @api.depends('timesheet_ids.timer_duration')
    def _compute_duration(self):
        for each in self:
            each.duration = 0
            each.duration = sum(each.timesheet_ids.mapped('timer_duration'))

    @api.multi
    def toggle_start(self):
        for record in self:
            record.task_timer = not record.task_timer
        if self.task_timer:
            self.write({'is_user_working': True})
            time_line = self.env['account.analytic.line']
            for time_sheet in self:
                time_line.create({
                    'name': self.env.user.name + ': ' + time_sheet.name,
                    'task_id': time_sheet.id,
                    'user_id': self.env.user.id,
                    'project_id': time_sheet.project_id.id,
                    'date_start': datetime.now(),
                })
        else:
            self.write({'is_user_working': False})
            time_line_obj = self.env['account.analytic.line']
            domain = [('task_id', 'in', self.ids), ('date_end', '=', False)]
            for time_line in time_line_obj.search(domain):
                time_line.write({'date_end': fields.Datetime.now()})
                if time_line.date_end:
                    diff = fields.Datetime.from_string(time_line.date_end) - fields.Datetime.from_string(
                        time_line.date_start)
                    time_line.timer_duration = round(diff.total_seconds() / 60.0, 2)
                    time_line.unit_amount = round(diff.total_seconds() / (60.0 * 60.0), 2)
                else:
                    time_line.unit_amount = 0.0
                    time_line.timer_duration = 0.0

    task_timer = fields.Boolean()
    is_user_working = fields.Boolean(
        'Is Current User Working', compute='_compute_is_user_working',
        help="Technical field indicating whether the current user is working. ")
    duration = fields.Float(
        'Real Duration', compute='_compute_duration',
        readonly=True, store=True)
    project_code = fields.Char(related='project_id.project_code', store=True, string='Project code', readonly=True)
    
    approval_check_first = fields.Boolean(string='First approval')
    approval_check_second = fields.Boolean(string='Second approval')
    approval_check_third = fields.Boolean(string='Third approval')
    internal_rev_hist_ids = fields.One2many('internal.revision.history','task_id',string='Internal Revision History')
    customer_rev_hist_ids = fields.One2many('customer.revision.history','task_id',string='Customer Revision History')
    approval_history_ids = fields.One2many('approval.history','task_id',string='Approval History')
    first_approvee = fields.Many2one(related='project_id.first_approvee', store=True, readonly=True, string='First Approvee')
    second_approvee = fields.Many2one(related='project_id.second_approvee', store=True, readonly=True, string='Second Approvee')
    third_approvee = fields.Many2one(related='project_id.third_approvee', store=True, readonly=True, string='Third Approvee')
    building_type_id = fields.Many2one('building.type',string='Building Type')
    building_code = fields.Char(string='Building Code')
    stage_project = fields.Char(string='Project Stage')
    drawing_type_id = fields.Many2one('drawing.type',string='Drawing Type')
    drawing_number = fields.Char(string='Drawing Code')
    drawing_name = fields.Char(string='Drawing Number')
    current_drawing = fields.Binary("Current Drawing", attachment=True)
    store_fname = fields.Char(string="File Name")
    
    transmital_draw_size = fields.Char(string='Size')
    transmital_draw_scale = fields.Char(string='Scale')
    transmital_draw_no_sheet = fields.Integer(string='No of sheets')
    transmital_draw_no_print = fields.Integer(string='No of prints/copies')
    transmital_draw_total_prints = fields.Integer(string='Total prints')
    transmital_draw_soft_copy = fields.Selection([('yes','Yes'),
                                                    ('no','No')],string='Softcopy(PDF)')
    total_hard_copy = fields.Integer(string='Total Hardcopies')
    total_soft_copy = fields.Integer(string='Total oftscopies(In PDF)')
    
    milestone_id = fields.Many2one('milestone',string='Milestones')
    mode_of_transmission = fields.Many2one('mode.transmission',string='VIA')
    subject = fields.Char(string='Subject')
    purpose_ids = fields.Many2many('purpose',string='Purpose')
    transmital_date = fields.Date(string='Transmital Date')
    issued_place = fields.Char(string='Issued at')
    
    revised_drawing_no = fields.Char(string='Drawing number rev')
    revision_code_id = fields.Many2one('revision.code',string='Client')
    revision_sub_code_id = fields.Many2one('revisionsub.code',string='Internal')
    rev_reason = fields.Char(string="Reason")
    
    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(ProjectTaskTimer, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        print("==================================",self.user_has_groups('sga_addons.group_sga_readonly'),self.user_has_groups('sga_addons.group_sga_no_create'))
        if view_type == 'form':
            doc = etree.XML(res['arch'])
        
            if self.user_has_groups('sga_addons.group_sga_readonly'):
                
                for node in doc.xpath("//form"):
                    node.attrib['edit'] = 'false'
                    node.attrib['create'] = 'false'
                res['arch'] = etree.tostring(doc)
            elif self.user_has_groups('sga_addons.group_sga_no_create'):
                
                for node in doc.xpath("//form"):
                    
                    node.attrib['create'] = 'false'
                res['arch'] = etree.tostring(doc)
            
        return res
    
    @api.multi
    def func_revision(self):
        if self.revision_code_id and self.revision_sub_code_id:
            self.revised_drawing_no = self.drawing_name + '/' + self.revision_code_id.name + self.revision_sub_code_id.name
            internal_rev_obj = self.env['internal.revision.history']
            internal_rev_obj.create({
                                    'reason':self.rev_reason,
                                    'timestamp_c':fields.Datetime.now(),
                                    'revised_drawing_number':self.drawing_name + '/' + self.revision_code_id.name + self.revision_sub_code_id.name,
                                    'task_id':self.id
                                    })
        else:
            self.revised_drawing_no = self.drawing_name + '/' + self.revision_code_id.name
            internal_rev_obj = self.env['customer.revision.history']
            internal_rev_obj.create({
                                    'reason':self.rev_reason,
                                    'timestamp_c':fields.Datetime.now(),
                                    'revised_drawing_number':self.drawing_name + '/' + self.revision_code_id.name,
                                    'task_id':self.id
                                    })
    
    @api.onchange('project_id')
    def onchange_projectid(self):
        if self.project_id:
            project_stage = self.project_id.state
            self.stage_project = project_stage
    
    @api.onchange('building_type_id')
    def onchange_buildingtype(self):
        if self.building_type_id:
            building_type = self.building_type_id.id
            for i in self.project_id.building_type_ids:
                if building_type == i.building_id.id:
                    self.building_code = i.building_code
                    
                
    @api.onchange('building_type_id','building_code','stage_project','drawing_type_id','drawing_number')
    def onachange_drawing_name(self):
        print ("values -------------------",self.building_type_id,self.building_code,self.stage_project,self.drawing_type_id,self.drawing_number)
        building_type = ''
        building_code = ''
        stage_project = ''
        drawing_number = ''
        drawing_name = ''
        project_code = ''
        drawing_type = ''
        
        project_code = self.project_code
        if self.building_type_id:
            building_type = self.building_type_id.name
        if self.building_code:
            building_code = self.building_code
        if self.stage_project :
            stage_project = self.stage_project
        if self.drawing_type_id:
            drawing_type = self.drawing_type_id.code
        
        if self.stage_project and self.building_code:
            project_task_srch = self.env['project.task'].search([('stage_project','=',stage_project),
                                                                ('project_id','=',self.project_id.id),
                                                                ('building_type_id','=',building_type)])
            print("project task search ---------------------",project_task_srch)
            if not project_task_srch:
                self.drawing_number = "001"
            else:
                drawing_nos = [int(i.drawing_number) for i in project_task_srch]
                print("drawing numbers -----------------------------",drawing_nos)
                last_drawing_no = max(drawing_nos)
                next_drawing_no = last_drawing_no + 1
                self.drawing_number = str(next_drawing_no).zfill(3)
        
        drawing_number = self.drawing_number
        if (building_type and building_code and stage_project and  drawing_number) != '':
            drawing_name = project_code + building_code + '-' + stage_project + '-' + drawing_type + '-' + drawing_number
            self.drawing_name = drawing_name
            
    @api.model
    def create(self, vals):
        self.onchange_projectid()
        self.onchange_buildingtype()
        self.onachange_drawing_name()
        res_task = super(ProjectTaskTimer,self).create(vals)
        
        
        return res_task
    
    # @api.model
    # def create(self, vals):
    #     res_project = super(ProjectTaskTimer,self).create(vals)
    #     print("RES project ---------------------",res_project)
    #     print("vals -------------------------------",vals)
    #     project_id = vals.get('project_id')
    #     building_type = vals.get('building_type_id')
    #     project_srch = self.env['project.project'].search([('id','=',project_id)])
    #     
    #     project_task_srch = self.env['project.task'].search([('stage_project','=',vals.get('stage_project')),
    #                                                             ('project_id','=',project_id),
    #                                                             ('building_type_id','=',building_type)])
    #     if not project_task_srch:
    #         res_project.drawing_number = "001"
    #     else:
    #         drawing_nos = [int(i.drawing_number) for i in project_task_srch]
    #         print("drawing numbers -----------------------------",drawing_nos)
    #         last_drawing_no = max(drawing_nos)
    #         next_drawing_no = last_drawing_no + 1
    #         res_project.drawing_number = str(next_drawing_no).zfill(3)
    #     
    #     print("vals ----------------------------------- final",vals)
    #     return res_project   
    
    @api.multi
    def write(self, vals):
        print ("Vals--------------------------------",vals)
        result = super(ProjectTaskTimer, self).write(vals)
        print ("Result =========================",result,vals)
        stage_id = vals.get('stage_id')
        stage_brws = self.env['project.task.type'].search([('id','=',stage_id)])
        
        if (self.first_approvee.id or self.second_approvee.id or self.third_approvee.id) != self._uid:
            if stage_brws.approval_check == True  or stage_brws.approval_check2 == True or stage_brws.approval_check3 == True:
                raise UserError(_('You are not authorized to approve this task.'))
        
        return result
    
    @api.multi
    def print_transmittal(self):
        return self.env.ref('sga_addons.report_transmittal_template').report_action(self)

class Milestone(models.Model):
    _name = 'milestone'
    _description = 'Milestones'
    
    name = fields.Char(string='Milestone')
    
class mode_transmission(models.Model):
    _name = 'mode.transmission'
    _description = 'Mode Transmission'

    name = fields.Char(string='name')

class Purpose(models.Model):
    _name = 'purpose'
    _desscription = 'Purpose'
    
    name = fields.Char(string='Purpose')