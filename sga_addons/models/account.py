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
from odoo import models, fields, api

class ProjectTaskTimeSheet(models.Model):
    _inherit = 'account.analytic.line'

    date_start = fields.Datetime(string='Start Date')
    date_end = fields.Datetime(string='End Date', readonly=1)
    timer_duration = fields.Float(invisible=1)
    