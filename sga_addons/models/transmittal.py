# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError

class Transmittal(models.TransientModel):
    _name = 'transmittal'
    _description = 'Transmittal'
    
    emp_name = fields.Many2one('res.users',string='Employee name')
    project_id = fields.Many2one('project.project',string='Project Name')
    drawing_no = fields.Many2one('project.task',string='Drawing Number')
    
    
