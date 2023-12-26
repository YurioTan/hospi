from odoo import api, fields, models

class IrActionsReport(models.Model):

  _inherit = 'ir.actions.report'

  document_no = fields.Char('Document Number')

  def _get_rendering_context(self, docids, data):
    data = data and dict(data) or {}
    data.update({'document_no': 'TEST-1234'})
    return super()._get_rendering_context(docids=docids, data=data)