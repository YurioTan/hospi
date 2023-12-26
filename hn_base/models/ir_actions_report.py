from odoo import api, fields, models

class IrActionsReport(models.Model):

  _inherit = 'ir.actions.report'

  document_no = fields.Char('Document Number')

  def _get_rendering_context(self, docids, data):
    result = super(IrActionsReport, self)._get_rendering_context(docids, data)
    result['document_no'] = self.document_no
    return result