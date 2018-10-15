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

class BuildingType(models.Model):
    _name = 'building.type'
    _description = 'Building Type'
    
    name = fields.Char(string='Building type')
    building_code = fields.Char(string='Building code')
    
class BuildingTypeLine(models.Model):
    _name = 'building.type.line'
    _description = 'Building Type Line'
    
    building_id = fields.Many2one('building.type',string='Building name')
    department_ids = fields.Many2many('department',string='Department')
    project_id = fields.Many2one('project.project',string='Project')
    building_code = fields.Char(string='Building code')
        