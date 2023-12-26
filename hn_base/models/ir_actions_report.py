from odoo import api, fields, models

class IrActionsReport(models.Model):
  _inherit = 'ir.actions.report'

  document_no = fields.Char('Document Number')