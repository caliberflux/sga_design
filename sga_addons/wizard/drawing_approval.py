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

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError

class DrawingApproval(models.TransientModel):
    _name = 'drawing.approval'
    _description = 'Drawing Approval'
    
    reject_reason = fields.Char(string='Reason')
    reject_approv_selc = fields.Selection([
                                            ('approve', 'Approved'),
                                            ('reject', 'Rejected'),
                                                ], string='Approval')
    timestamp_a = fields.Datetime(string='Timestamp',default=fields.Datetime.now)
    
    @api.multi
    def approve_reject(self):
        task_id = self.env.context.get('active_ids')[0]
        internal_rev_obj = self.env['approval.history']
        internal_rev_obj.create({
                                'reject_reason':self.reject_reason,
                                'timestamp_a':self.timestamp_a,
                                'approval_status':self.reject_approv_selc,
                                'approval_check':True if self.reject_approv_selc == 'approve' else False,
                                'task_id':task_id,
                                'user_id':self._uid
                                })
        
        task_brws = self.env['project.task'].search([('id','=',task_id)])
        task_stage_ids = self.env['project.task.type'].search([('id','>',0)])
        if self.reject_approv_selc == 'approve':
            if task_brws.approval_check_first == False:
                task_brws.approval_check_first = True
                for i in task_stage_ids:
                    if i.approval_check == True:
                        task_brws.stage_id = i.id
                        return True
            elif task_brws.approval_check_second == False and task_brws.approval_check_first == True:
                task_brws.approval_check_second = True
                for i in task_stage_ids:
                    if i.approval_check2 == True:
                        task_brws.stage_id = i.id
                        return True
            elif task_brws.approval_check_second == True and task_brws.approval_check_first == True and task_brws.approval_check_third == False:
                task_brws.approval_check_third == True
                for i in task_stage_ids:
                    if i.approval_check3 == True:
                        task_brws.stage_id = i.id
                        return True
        else:
            task_brws.approval_check_second == False
            task_brws.approval_check_first == False
            task_brws.approval_check_third == False
            # task_brws.stage_id = 2

class ApprovalHistory(models.Model):
    _name = 'approval.history'
    _description = 'Approval History'
    
    reject_reason = fields.Char(string='Reason')
    approval_status = fields.Selection([
                                            ('approve', 'Approved'),
                                            ('reject', 'Rejected'),
                                                ], string='Approval')
    timestamp_a = fields.Datetime(string='Timestamp')
    approval_check = fields.Boolean(string='Approval check')
    task_id = fields.Many2one('project.task',string='Task')
    user_id = fields.Many2one('res.users',string='Approved by')
    
