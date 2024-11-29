from odoo import models, fields, api, _
from odoo.exceptions import UserError

class InheritCOntractComponent(models.Model):
    _inherit = 'hr.contract.basecomponent'

    overtime_rate = fields.Boolean(string='Overtime Rate')

    