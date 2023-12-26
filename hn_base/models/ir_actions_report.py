from odoo import api, fields, models

class IrActionsReport(models.Model):

  _inherit = 'ir.actions.report'

  document_no = fields.Char('Document Number')

  def _get_rendering_context(self, report, docids, data):
    result = super(IrActionsReport, self)._get_rendering_context(report, docids, data)
    result['document_no'] = report.document_id
    return result