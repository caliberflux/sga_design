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

{
    'name': "SGA Design labs custom",

    'summary': """
                    Customization done specifically for SGA labs.""",

    'description': """
        
    """,
    'author': "Caliberflux",
    'website': "http://www.caliberflux.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'project', 'hr_timesheet','contacts'],
    'data': [
        
        'wizard/drawing_revision_history_view.xml',
        'wizard/drawing_approval_view.xml',
        'views/project_views.xml',
        'views/project_task_timer_view.xml',
        'views/project_timer_static.xml',
        'views/department_views.xml',
        'views/building_type_views.xml',
        'views/res_partner.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        
        'data/email_template.xml',
        'data/template_report.xml',
        'data/transmittal_report.xml'
        
    ],
}
